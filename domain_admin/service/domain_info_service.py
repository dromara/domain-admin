# -*- coding: utf-8 -*-
"""
domain_info_service.py
"""
import traceback
from typing import List

from peewee import chunked
from playhouse.shortcuts import model_to_dict

from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.user_model import UserModel
from domain_admin.service import render_service, email_service, notify_service, system_service, file_service
from domain_admin.utils import whois_util, datetime_util, domain_util, file_util
from domain_admin.utils.flask_ext.app_exception import AppException


def update_domain_info_row(row: DomainInfoModel) -> [str, None]:
    """
    更新一行数据
    :param row:
    :return:
    """
    domain_whois = None

    try:
        domain_whois = whois_util.get_domain_info(row.domain)
    except Exception as e:
        pass

    update_row = DomainInfoModel()

    if domain_whois:
        update_row.domain_start_time = domain_whois['start_time']
        update_row.domain_expire_time = domain_whois['expire_time']

    DomainInfoModel.update(
        domain_start_time=update_row.domain_start_time,
        domain_expire_time=update_row.domain_expire_time,
        domain_expire_days=update_row.real_domain_expire_days,
        update_time=datetime_util.get_datetime()
    ).where(
        DomainInfoModel.id == row.id
    ).execute()


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


def update_all_domain_info():
    """
    更新所有的域名信息
    :return:
    """
    rows = DomainInfoModel.select().where(
        DomainInfoModel.is_auto_update == True
    ).order_by(DomainInfoModel.domain_expire_days.asc())

    for row in rows:
        update_domain_info_row(row)


def send_domain_list_email(user_id, rows: List[DomainInfoModel]):
    """
    发送域名信息
    :param rows:
    :param user_id:
    :return:
    """

    # 配置检查
    config = system_service.get_system_config()

    system_service.check_email_config(config)

    email_list = notify_service.get_notify_email_list_of_user(user_id)

    if not email_list:
        raise AppException('收件邮箱未设置')

    # lst = get_domain_info_list(user_id)

    content = render_service.render_template('domain-email.html', {'list': rows})

    email_service.send_email(
        subject='[Domain Admin]域名过期提醒',
        content=content,
        to_addresses=email_list,
        content_type='html'
    )


def add_domain_from_file(filename, user_id):
    # logger.info('user_id: %s, filename: %s', user_id, filename)

    lst = domain_util.parse_domain_from_file(filename)

    lst = [
        {
            'domain': item.root_domain,
            'comment': item.alias,
            'user_id': user_id,
        } for item in lst
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
        DomainInfoModel.domain_expire_days.asc(),
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

    filename = file_util.get_random_filename('csv')
    temp_filename = file_service.resolve_temp_file(filename)
    # print(temp_filename)
    with open(temp_filename, 'w') as f:
        f.write(content)

    return filename


def check_domain_expire(user_id):
    """
    查询域名证书到期情况
    :return:
    """
    user_row = UserModel.get_by_id(user_id)

    # lst = get_domain_info_list(user_id)

    rows = DomainInfoModel.select().where(
        DomainInfoModel.user_id == user_id,
        DomainInfoModel.is_expire_monitor == True,
        DomainInfoModel.domain_expire_days <= user_row.before_expire_days
    ).order_by(
        DomainInfoModel.domain_expire_days.asc(),
        DomainInfoModel.id.desc()
    )

    lst = [model_to_dict(
        model=row,
        extra_attrs=[
            'domain_start_date',
            'domain_expire_date',
            'real_domain_expire_days',
        ]
    ) for row in rows]

    if len(lst) > 0:
        notify_user(user_id, lst)
        # send_domain_list_email(user_id)


def notify_user(user_id, rows: List[DomainInfoModel]):
    """
    尝试通知用户
    :param rows:
    :param user_id:
    :return:
    """
    try:
        send_domain_list_email(user_id, rows)
    except Exception as e:
        logger.error(traceback.format_exc())

    try:
        notify_service.notify_webhook_of_user(user_id)
    except Exception as e:
        logger.error(traceback.format_exc())


def update_and_check_all_domain():
    """
    更新并检查所域名信息和证书信息
    :return:
    """

    # 更新全部域名证书信息
    update_all_domain_info()

    # 全员检查并发送用户通知
    # if status:
    user_rows = UserModel.select()

    for row in user_rows:
        # 内层捕获单个用户发送错误
        check_domain_expire(row.id)
