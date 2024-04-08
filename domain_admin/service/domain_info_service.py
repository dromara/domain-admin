# -*- coding: utf-8 -*-
"""
domain_info_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import io
import json
import time
import traceback
from datetime import datetime, timedelta
import random

from domain_admin.model import domain_info_model
from peewee import chunked

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.service import render_service, file_service, group_service, async_task_service, domain_service, \
    domain_icp_service
from domain_admin.utils import whois_util, datetime_util, domain_util, icp_util, file_util


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


def update_domain_info_row(row):
    """
    更新一行数据
    :param row: DomainInfoModel
    :return: [str, None]
    """
    logger.info("domain: %s", row.domain)

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
        update_time=datetime_util.get_datetime(),
        version=DomainInfoModel.version + 1
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

        # 防止过于频繁
        time.sleep(random.randint(3, 10))


def update_domain_row_icp(row):
    """
    更新icp信息
    :param row:
    :return:
    """
    logger.info("domain: %s", row.domain)

    item = domain_icp_service.get_domain_icp(domain=row.domain)

    if not item:
        return

    data = {}

    if not row.icp_company:
        data['icp_company'] = item.name

    if not row.icp_licence:
        data['icp_licence'] = item.icp

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

    lst = list(domain_util.parse_domain_from_file(filename, domain_info_model.FIELD_MAPPING))

    # 导入分组
    group_name_list = [item.get('group_name') for item in lst if item.get('group_name')]
    if group_name_list:
        group_map = group_service.get_or_create_group_map(group_name_list, user_id)
    else:
        group_map = {}

    lst = [
        {
            'domain': item['domain'],
            'comment': item.get('comment'),
            'group_id': group_map.get(item.get('group_name'), 0),
            'tags_raw': json.dumps(item.get('tags'), ensure_ascii=False),
            'domain_start_time': item.get('domain_start_date'),
            'domain_expire_time': item.get('domain_expire_date'),
            'domain_expire_days': item.get('real_domain_expire_days') or 0,
            'icp_company': item.get('icp_company'),
            'icp_licence': item.get('icp_licence'),
            'user_id': user_id,
        } for item in lst if item.get('root_domain')
    ]

    for batch in chunked(lst, 500):
        DomainInfoModel.insert_many(batch).on_conflict_ignore().execute()


def export_domain_to_file(rows, ext):
    """
    导出域名到文件
    :param ext: 导出格式
    :param rows:
    :return:
    """

    filename = datetime.now().strftime("domain_%Y%m%d%H%M%S") + '.' + ext
    temp_filename = file_service.resolve_temp_file(filename)

    if ext == 'txt':
        lst = [row['domain'] for row in rows]
    else:
        lst = file_util.convert_to_export(rows, domain_info_model.FIELD_MAPPING)

    # content = render_service.render_template('domain-export.csv', {'list': rows})
    file_util.write_data_to_file(temp_filename, lst)

    return filename


def get_domain_info_query(keyword, group_ids, domain_expire_days, role, user_id):
    user_group_ids = None

    if role == RoleEnum.ADMIN:
        pass

    else:
        # 所在分组
        group_user_rows = GroupUserModel.select().where(
            GroupUserModel.user_id == user_id
        )

        group_user_list = list(group_user_rows)
        user_group_ids = [row.group_id for row in group_user_list]

    # 列表数据
    query = DomainInfoModel.select()

    if keyword:
        query = query.where(
            (DomainInfoModel.domain.contains(keyword))
            | (DomainInfoModel.tags_raw.contains(keyword))
        )

    if group_ids:
        query = query.where(DomainInfoModel.group_id.in_(group_ids))
    else:

        if role == RoleEnum.ADMIN:
            pass

        elif user_group_ids:
            query = query.where(
                (DomainInfoModel.user_id == user_id)
                | (DomainInfoModel.group_id.in_(user_group_ids))
            )
        else:
            query = query.where(DomainInfoModel.user_id == user_id)

    if domain_expire_days is not None and len(domain_expire_days) == 2:
        if domain_expire_days[0] is None:
            max_expire_time = datetime.now() + timedelta(days=domain_expire_days[1])
            query = query.where(
                (DomainInfoModel.domain_expire_time <= max_expire_time)
                | (DomainInfoModel.domain_expire_time.is_null(True))
            )
        elif domain_expire_days[1] is None:
            min_expire_time = datetime.now() + timedelta(days=domain_expire_days[0])
            query = query.where(DomainInfoModel.domain_expire_time >= min_expire_time)
        else:
            min_expire_time = datetime.now() + timedelta(days=domain_expire_days[0])
            max_expire_time = datetime.now() + timedelta(days=domain_expire_days[1])

            query = query.where(
                DomainInfoModel.domain_expire_time.between(min_expire_time, max_expire_time))

    return query


def get_ordering(order_prop='expire_days', order_type='ascending'):
    ordering = []

    # order by domain_expire_days
    if order_prop == 'domain_expire_days':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.domain_expire_time.desc())
        else:
            ordering.append(DomainInfoModel.domain_expire_time.asc())

    # order by domain
    elif order_prop == 'domain':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.domain.desc())
        else:
            ordering.append(DomainInfoModel.domain.asc())

    # order by group_id
    elif order_prop == 'group_name':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.group_id.desc())
        else:
            ordering.append(DomainInfoModel.group_id.asc())

    # order by update_time
    elif order_prop == 'update_time':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.update_time.desc())
        else:
            ordering.append(DomainInfoModel.update_time.asc())

    # order by is_expire_monitor
    elif order_prop == 'is_expire_monitor':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.is_expire_monitor.desc())
        else:
            ordering.append(DomainInfoModel.is_expire_monitor.asc())

    # fix: order by is_auto_update
    elif order_prop == 'is_auto_update':
        if order_type == 'descending':
            ordering.append(DomainInfoModel.is_auto_update.desc())
        else:
            ordering.append(DomainInfoModel.is_auto_update.asc())

    ordering.append(DomainInfoModel.id.desc())

    return ordering


@async_task_service.async_task_decorator("从文件导入域名")
def handle_auto_import_domain_info(current_user_id):
    rows = DomainInfoModel.select().where(
        DomainInfoModel.user_id == current_user_id,
        DomainInfoModel.is_auto_update == True,
        DomainInfoModel.version == 0
    )

    lst = list(rows)

    # 注册信息
    for row in lst:
        update_domain_info_row(row)

    # icp信息
    for row in lst:
        if not row.icp_company:
            update_domain_row_icp(row)

    # 导入子域名
    for row in lst:
        try:
            domain_service.auto_import_from_domain(
                root_domain=row.domain,
                group_id=row.group_id,
                user_id=current_user_id
            )
        except Exception as e:
            logger.error(traceback.format_exc())

    # 获取证书信息
    domain_service.init_domain_cert_info_of_user(user_id=current_user_id)
