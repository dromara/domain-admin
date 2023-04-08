# -*- coding: utf-8 -*-
import json
import os
import time
import traceback
from datetime import datetime

from playhouse.shortcuts import model_to_dict
from peewee import chunked
from domain_admin.log import logger
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.log_scheduler_model import LogSchedulerModel
from domain_admin.model.user_model import UserModel
from domain_admin.service import email_service, render_service, global_data_service
from domain_admin.service import file_service
from domain_admin.service import notify_service
from domain_admin.service import system_service
from domain_admin.utils import datetime_util, cert_util, whois_util, file_util
from domain_admin.utils import domain_util
from domain_admin.utils.flask_ext.app_exception import AppException, ForbiddenAppException
from concurrent.futures import ThreadPoolExecutor


def add_domain(data):
    """
    添加域名
    :param data: {
        'domain': '必传',
        'user_id': '必传',
        'alias': '可选，默认 ""'
        'group_id': '可选，默认 0'
     }
    :return:
    """
    user_id = data['user_id']
    domain = data['domain']
    alias = data.get('alias', '')
    group_id = data.get('group_id', 0)

    row = DomainModel.create(
        user_id=user_id,
        domain=domain,
        alias=alias,
        group_id=group_id
    )

    return row


def update_domain_cert_info(row):
    """
    更新域名和证书信息
    :param cache:
    :param row:
    :return:
    """
    logger.info('update_domain_cert_info: %s', row.domain)

    # 获取域名信息
    domain_info = get_domain_info(row.domain)

    # 获取证书信息
    cert_info = get_cert_info(row.domain)

    DomainModel.update(
        start_time=cert_info.get('start_date'),
        expire_time=cert_info.get('expire_date'),
        expire_days=cert_info.get('expire_days'),
        domain_start_time=domain_info['start_time'],
        domain_expire_time=domain_info['expire_time'],
        domain_expire_days=domain_info['expire_days'],
        total_days=cert_info.get('total_days'),
        ip=cert_info.get('ip', ''),
        connect_status=cert_info.get('connect_status'),
        detail_raw=json.dumps(cert_info.get('info'), ensure_ascii=False),
        check_time=datetime_util.get_datetime(),
    ).where(
        DomainModel.id == row.id
    ).execute()


def get_cert_info(domain: str):
    now = datetime.now()
    info = {}
    expire_days = 0
    total_days = 0
    connect_status = True

    try:
        info = cert_util.get_cert_info(domain)

    except Exception:
        logger.error(traceback.format_exc())
        connect_status = False

    start_date = info.get('start_date')
    expire_date = info.get('expire_date')

    if start_date and expire_date:
        start_time = datetime_util.parse_datetime(start_date)
        expire_time = datetime_util.parse_datetime(expire_date)

        expire_days = (expire_time - now).days
        total_days = (expire_time - start_time).days

    return {
        'start_date': start_date,
        'expire_date': expire_date,
        'expire_days': expire_days,
        'total_days': total_days,
        'connect_status': connect_status,
        'ip': info.get('ip', ''),
        'info': info,
    }


def get_domain_info(domain: str):
    """
    获取域名注册信息
    :param domain: 域名
    :param cache: 查询缓存字典
    :return:
    """

    cache = global_data_service.get_value('update_domain_list_info_cache')

    now = datetime.now()

    # 获取域名信息
    domain_info = {}
    domain_expire_days = 0

    # 解析出域名和顶级后缀
    extract_result = domain_util.extract_domain(domain)
    domain_and_suffix = '.'.join([extract_result.domain, extract_result.suffix])

    if cache:
        domain_info = cache.get(domain_and_suffix)

    if not domain_info:
        try:
            domain_info = whois_util.get_domain_info(domain_and_suffix)
            if cache:
                cache[domain_and_suffix] = domain_info

        except Exception:
            logger.error(traceback.format_exc())

    domain_start_time = domain_info.get('start_time')
    domain_expire_time = domain_info.get('expire_time')

    if domain_expire_time:
        domain_expire_days = (domain_expire_time - now).days

    return {
        'start_time': domain_start_time,
        'expire_time': domain_expire_time,
        'expire_days': domain_expire_days
    }


def update_all_domain_cert_info():
    """
    更新所有域名信息
    :return:
    """
    lst = DomainModel.select()
    update_domain_list_info(lst)


def update_domain_list_info(rows):
    """
    更新列表数据
    :param rows:
    :return:
    """
    # 增加缓存，提升查询效率
    cache = {}
    global_data_service.set_value('update_domain_list_info_cache', cache)

    for row in rows:
        update_domain_cert_info(row)
        # bugfix: ConnectionResetError: [Errno 104] Connection reset by peer
        # 请求过于频繁
        time.sleep(0.5)

    global_data_service.remove_value('update_domain_list_info_cache')


def update_all_domain_cert_info_of_user(user_id):
    """
    更新用户的所有域名信息
    :return:
    """
    lst = DomainModel.select().where(
        DomainModel.user_id == user_id
    )

    update_domain_list_info(lst)

    key = f'update_domain_status:{user_id}'
    global_data_service.set_value(key, False)


def get_domain_info_list(user_id=None):
    query = DomainModel.select()

    if user_id:
        query = query.where(
            DomainModel.user_id == user_id
        )

    query = query.order_by(
        DomainModel.expire_days.asc(),
        DomainModel.domain_expire_days.asc(),
        DomainModel.id.desc()
    )

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'start_date',
            'expire_date',
            # 'expire_days',
        ]
    ), query))

    # def compare(a, b):
    #     if a['expire_days'] and b['expire_days']:
    #         return a['expire_days'] - b['expire_days']
    #     else:
    #         if a['expire_days']:
    #             return a['expire_days']
    #         else:
    #             return -b['expire_days']

    # lst = sorted(lst, key=cmp_to_key(compare))

    return lst


def check_domain_cert(user_id):
    """
    查询域名证书到期情况
    :return:
    """
    user_row = UserModel.get_by_id(user_id)

    lst = get_domain_info_list(user_id)

    has_expired_domain = False

    for item in lst:
        # 2023-02-06 如果不检测就跳过
        if not item['is_monitor']:
            continue

        if not item['expire_days'] or item['expire_days'] <= user_row.before_expire_days:
            has_expired_domain = True
            break

        if not item['domain_expire_days'] or item['domain_expire_days'] <= user_row.before_expire_days:
            has_expired_domain = True
            break

    if has_expired_domain:
        notify_user(user_id)
        # send_domain_list_email(user_id)


def update_and_check_all_domain_cert():
    log_row = LogSchedulerModel.create()

    error_message = ''

    status = True

    # 更新全部域名证书信息
    update_all_domain_cert_info()

    # 配置检查
    config = system_service.get_system_config()
    try:
        system_service.check_email_config(config)
    except Exception as e:
        logger.error(traceback.format_exc())

        status = False

        if isinstance(e, AppException):
            error_message = e.message
        else:
            error_message = str(e)

    # 全员发送
    if status:
        rows = UserModel.select()

        for row in rows:

            # 内层捕获单个用户发送错误
            try:
                check_domain_cert(row.id)
            except Exception as e:
                # traceback.print_exc()
                logger.error(traceback.format_exc())

                status = False

                if isinstance(e, AppException):
                    error_message = e.message
                else:
                    error_message = str(e)

    LogSchedulerModel.update({
        'status': status,
        'error_message': error_message,
        'update_time': datetime_util.get_datetime(),
    }).where(
        LogSchedulerModel.id == log_row
    ).execute()


def send_domain_list_email(user_id):
    """
    发送域名信息
    :param user_id:
    :return:
    """

    email_list = notify_service.get_notify_email_list_of_user(user_id)

    if not email_list:
        raise AppException('收件邮箱未设置')

    lst = get_domain_info_list(user_id)

    content = render_service.render_template('domain-cert-email.html', {'list': lst})

    email_service.send_email(
        content=content,
        to_addresses=email_list,
        content_type='html'
    )


def check_permission_and_get_row(domain_id, user_id):
    """
    权限检查
    :param domain_id:
    :param user_id:
    :return:
    """
    row = DomainModel.get_by_id(domain_id)
    if row.user_id != user_id:
        raise ForbiddenAppException()

    return row


def add_domain_from_file(filename, user_id):
    logger.info('add_domain_from_file')

    lst = domain_util.parse_domain_from_file(filename)
    lst = [
        {
            'domain': item['domain'],
            'alias': item.get('alias', ''),
            'user_id': user_id,
        } for item in lst
    ]

    for batch in chunked(lst, 500):
        DomainModel.insert_many(batch).on_conflict_ignore().execute()

    # count = 0
    # for domain in lst:
    #     try:
    #         row = add_domain({
    #             'domain': domain,
    #             'user_id': user_id,
    #         })
    #
    #         # 导入后统一查询，避免太过耗时
    #         # update_domain_cert_info(row)
    #
    #         count += 1
    #     except Exception as e:
    #         # traceback.print_exc()
    #         logger.error(traceback.format_exc())

    # 查询
    update_all_domain_cert_info_of_user(user_id=user_id)

    # return count


def export_domain_to_file(user_id):
    """
    导出域名到文件
    :param user_id:
    :return:
    """
    # 域名数据
    rows = DomainModel.select().where(
        DomainModel.user_id == user_id
    ).order_by(
        DomainModel.expire_days.asc(),
        DomainModel.id.desc(),
    )

    #  分组数据
    group_rows = GroupModel.select().where(
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


def notify_user(user_id):
    """
    尝试通知用户
    :param user_id:
    :return:
    """
    try:
        send_domain_list_email(user_id)
    except:
        pass

    try:
        notify_service.notify_webhook_of_user(user_id)
    except Exception as e:
        logger.error(traceback.format_exc())


def update_and_check_domain_cert(user_id):
    # 先更新，再检查
    update_all_domain_cert_info_of_user(user_id)

    check_domain_cert(user_id)

    key = f'check_domain_status:{user_id}'
    global_data_service.set_value(key, False)
