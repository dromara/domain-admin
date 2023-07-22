# -*- coding: utf-8 -*-
"""
domain_info_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import io
import time
import traceback
from datetime import datetime, timedelta

from peewee import chunked

from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import render_service, file_service, group_service, async_task_service
from domain_admin.utils import whois_util, datetime_util, domain_util, icp_util


def add_domain_info(
        domain,
        user_id,
        comment='',
        group_id=0,
        domain_start_time=None,
        domain_expire_time=None,
        is_auto_update=True,
        icp_company='',
        icp_licence='',
        tags=None
):
    """
    添加域名监测

    :param icp_licence:
    :param icp_company:
    :param is_auto_update:
    :param domain:
    :param user_id:
    :param comment:
    :param group_id:
    :param domain_start_time:
    :param domain_expire_time:
    :param tags:

    :return: DomainInfoModel
    """
    row = DomainInfoModel.create(
        domain=domain,
        domain_start_time=domain_start_time,
        domain_expire_time=domain_expire_time,
        comment=comment,
        group_id=group_id,
        user_id=user_id,
        is_auto_update=is_auto_update,
        icp_company=icp_company,
        icp_licence=icp_licence,
        tags=tags
    )

    # 添加的时候需要自动更新
    if is_auto_update is True:
        update_domain_info_row(row)

    # 添加的时候顺便添加icp备案信息
    # update_domain_info_icp(row)

    return row


def update_domain_info_icp(row):
    """
    更新域名icp备案信息
    :param row: DomainInfoModel
    :return:
    """

    icp_info = None

    try:
        ret = icp_util.get_icp(row.domain)
        icp_info = ret['info']
    except Exception:
        logger.error(traceback.format_exc())

    if icp_info:
        DomainInfoModel.update(
            icp_company=icp_info['name'],
            icp_licence=icp_info['icp']
        ).where(
            DomainInfoModel.id == row.id
        ).execute()


def update_domain_info_row(row):
    """
    更新一行数据
    :param row: DomainInfoModel
    :return: [str, None]
    """
    domain_whois = None

    try:
        domain_whois = whois_util.get_domain_info(row.domain)
    except Exception as e:
        # 增加容错
        try:
            time.sleep(3)
            domain_whois = whois_util.get_domain_info(row.domain)
        except Exception as e:
            pass

    update_row = DomainInfoModel()

    if domain_whois:
        update_row.domain_start_time = domain_whois['start_time']
        update_row.domain_expire_time = domain_whois['expire_time']
        update_row.domain_registrar = domain_whois['registrar']
        update_row.domain_registrar_url = domain_whois['registrar_url']

    DomainInfoModel.update(
        domain_start_time=update_row.domain_start_time,
        domain_expire_time=update_row.domain_expire_time,
        domain_expire_days=update_row.real_domain_expire_days,
        domain_registrar=update_row.domain_registrar,
        domain_registrar_url=update_row.domain_registrar_url,
        update_time=datetime_util.get_datetime()
    ).where(
        DomainInfoModel.id == row.id
    ).execute()


@async_task_service.async_task_decorator("更新域名信息")
def update_all_domain_info_of_user(user_id):
    """
    更新单个用户的所有域名信息
    :param user_id:
    :return:
    """
    rows = DomainInfoModel.select().where(
        DomainInfoModel.user_id == user_id,
        DomainInfoModel.is_auto_update == True
    )

    for row in rows:
        update_domain_info_row(row)


@async_task_service.async_task_decorator("补全域名ICP信息")
def update_all_domain_icp_of_user(user_id):
    """
    补全域名ICP信息
    :param user_id:
    :return:
    """
    rows = DomainInfoModel.select().where(
        (DomainInfoModel.user_id == user_id)
        & (
                (DomainInfoModel.icp_company == None)
                | (DomainInfoModel.icp_company == '')
                | (DomainInfoModel.icp_licence == '')
                | (DomainInfoModel.icp_licence == '')
        )
    )

    for row in rows:
        update_domain_row_icp(row)


def update_domain_row_icp(row):
    """
    更新icp信息
    :param row:
    :return:
    """
    res = None

    try:
        res = icp_util.get_icp(row.domain)
    except Exception as e:
        logger.debug(traceback.format_exc())

    if not res:
        return

    data = {}

    if not row.icp_company:
        data['icp_company'] = res.get('name')

    if not row.icp_licence:
        data['icp_licence'] = res.get('icp')

    if len(data) == 0:
        return

    DomainInfoModel.update(data).where(
        DomainInfoModel.id == row.id
    ).execute()


def update_all_domain_info():
    """
    更新所有的域名信息
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=30)

    rows = DomainInfoModel.select().where(
        DomainInfoModel.is_auto_update == True,
        # 域名注册完后，过期时间比较固定，基本上不会改变，不用每次都全量更新
        DomainInfoModel.domain_expire_time <= notify_expire_time
    ).order_by(DomainInfoModel.domain_expire_days.asc())

    for row in rows:
        update_domain_info_row(row)


def add_domain_from_file(filename, user_id):
    """
    从文件导入域名列表
    :param filename:
    :param user_id:
    :return:
    """
    # logger.info('user_id: %s, filename: %s', user_id, filename)

    lst = list(domain_util.parse_domain_from_file(filename))

    # 导入分组
    group_name_list = [item.group_name for item in lst]
    group_map = group_service.get_or_create_group_map(group_name_list, user_id)

    lst = [
        {
            'domain': item.root_domain,
            'comment': item.alias,
            'user_id': user_id,
            'group_id': group_map.get(item.group_name, 0),
        } for item in lst if item.root_domain
    ]

    for batch in chunked(lst, 500):
        DomainInfoModel.insert_many(batch).on_conflict_ignore().execute()


def export_domain_to_file(user_id):
    """
    导出域名到文件
    :param user_id:
    :return:
    """
    # 域名数据
    rows = DomainInfoModel.select().where(
        DomainInfoModel.user_id == user_id
    ).order_by(
        DomainInfoModel.domain_expire_time.asc(),
        DomainInfoModel.id.desc(),
    )

    # 分组数据
    group_rows = GroupModel.select(
        GroupModel.id,
        GroupModel.name,
    ).where(
        GroupModel.user_id == user_id
    )

    group_map = {row.id: row.name for row in group_rows}

    lst = []
    for row in list(rows):
        row.group_name = group_map.get(row.group_id, '')
        lst.append(row)

    content = render_service.render_template('domain-export.csv', {'list': lst})

    filename = datetime.now().strftime("domain_%Y%m%d%H%M%S") + '.csv'

    temp_filename = file_service.resolve_temp_file(filename)
    # print(temp_filename)
    with io.open(temp_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    return filename
