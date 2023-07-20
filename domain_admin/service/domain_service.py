# -*- coding: utf-8 -*-
"""
domain_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import io
import traceback
from datetime import datetime

from peewee import chunked, fn
from playhouse.shortcuts import model_to_dict

from domain_admin.log import logger
from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.user_model import UserModel
from domain_admin.service import file_service, async_task_service
from domain_admin.service import render_service, group_service
from domain_admin.utils import datetime_util, cert_util
from domain_admin.utils import domain_util
from domain_admin.utils.cert_util import cert_socket_v2, cert_openssl_v2
from domain_admin.utils.flask_ext.app_exception import ForbiddenAppException
from domain_admin.utils.open_api import crtsh_api


def update_domain_host_list(domain_row):
    """
    更新ip信息
    :param domain_row: DomainModel
    :return:
    @since v1.2.24
    """
    domain_host_list = []

    try:
        domain_host_list = cert_socket_v2.get_domain_host_list(
            domain=domain_row.domain,
            port=domain_row.port
        )
    except Exception as e:
        logger.error(traceback.format_exc())

    lst = [
        {
            'domain_id': domain_row.id,
            'host': domain_host
        } for domain_host in domain_host_list]

    logger.info(lst)

    AddressModel.insert_many(lst).on_conflict_ignore().execute()


def update_domain_address_list_cert(domain_row):
    """
    更新证书信息
    :param domain_row: DomainModel
    :return:
    """
    # logger.info("%s", model_to_dict(domain_row))

    lst = AddressModel.select().where(
        AddressModel.domain_id == domain_row.id
    )

    err = ''
    for address_row in lst:
        err = update_address_row_info(address_row, domain_row)

    sync_address_info_to_domain_info(domain_row)
    return err


def update_address_row_info(address_row, domain_row):
    """
    更新单个地址信息
    :param domain_row:
    :param address_row:
    :return:
    """

    # 获取证书信息
    cert_info = {}

    err = ''
    try:
        cert_info = cert_openssl_v2.get_ssl_cert_by_openssl(
            domain=domain_row.domain,
            host=address_row.host,
            port=domain_row.port
        )
    except Exception as e:
        err = e.__str__()
        logger.error(traceback.format_exc())

    logger.info(cert_info)

    address = AddressModel()
    address.ssl_start_time = cert_info.get('start_date')
    address.ssl_expire_time = cert_info.get('expire_date')

    AddressModel.update(
        ssl_start_time=address.ssl_start_time,
        ssl_expire_time=address.ssl_expire_time,
        ssl_expire_days=address.real_time_ssl_expire_days,
        # ssl_check_time=datetime_util.get_datetime(),
        update_time=datetime_util.get_datetime(),
    ).where(
        AddressModel.id == address_row.id
    ).execute()

    return err


def update_address_row_info_with_sync_domain_row(address_id):
    """
    更新主机信息并同步到与名表
    :param address_id: int
    :return:
    """
    address_row = AddressModel.get_by_id(address_id)

    domain_row = DomainModel.get_by_id(address_row.domain_id)

    update_address_row_info(address_row, domain_row)

    sync_address_info_to_domain_info(domain_row)


def sync_address_info_to_domain_info(domain_row):
    """
    同步主机信息到域名信息表
    :param domain_row: DomainModel
    :return:
    """
    first_address_row = AddressModel.select().where(
        AddressModel.domain_id == domain_row.id
    ).order_by(
        AddressModel.ssl_expire_days.asc()
    ).first()

    connect_status = False

    if first_address_row is None:
        first_address_row = AddressModel()
        first_address_row.ssl_start_time = None
        first_address_row.ssl_expire_time = None

    elif first_address_row.real_time_ssl_expire_days > 0:
        connect_status = True

    DomainModel.update(
        start_time=first_address_row.ssl_start_time,
        expire_time=first_address_row.ssl_expire_time,
        expire_days=first_address_row.real_time_ssl_expire_days,
        connect_status=connect_status,
        update_time=datetime_util.get_datetime(),
    ).where(
        DomainModel.id == domain_row.id
    ).execute()


def update_domain_row(domain_row):
    """
    更新域名相关数据
    :param domain_row: DomainModel
    :return:
    """
    # fix old data update root domain
    if not domain_row.root_domain:
        DomainModel.update(
            root_domain=domain_util.get_root_domain(domain_row.domain)
        ).where(
            DomainModel.id == domain_row.id
        ).execute()

    # 动态主机ip，需要先删除所有主机地址
    if domain_row.is_dynamic_host:
        AddressModel.delete().where(
            AddressModel.domain_id == domain_row.id
        ).execute()

    # 主机ip信息
    update_domain_host_list(domain_row)

    # 证书信息
    update_domain_address_list_cert(domain_row)


def get_cert_info(domain):
    """
    :param domain: str
    :return:
    """
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
        # 'ip': info.get('ip', ''),
        'info': info,
    }


def update_all_domain_cert_info():
    """
    更新所有域名信息
    :return:
    """
    rows = DomainModel.select().where(
        DomainModel.auto_update == True
    ).order_by(DomainModel.expire_days.asc())

    for row in rows:
        update_domain_row(row)


@async_task_service.async_task_decorator("更新证书信息")
def update_all_domain_cert_info_of_user(user_id):
    """
    更新用户的所有证书信息
    :return:
    """
    rows = DomainModel.select().where(
        DomainModel.user_id == user_id,
        DomainModel.auto_update == True
    )

    for row in rows:
        update_domain_row(row)

    # key = f'update_domain_status:{user_id}'
    # global_data_service.set_value(key, False)


def get_domain_info_list(user_id=None):
    query = DomainModel.select()

    user_row = UserModel.get_by_id(user_id)

    query = query.where(
        DomainModel.user_id == user_id,
        DomainModel.is_monitor == True,
        DomainModel.expire_days < user_row.before_expire_days
    )

    query = query.order_by(
        DomainModel.expire_days.asc(),
        DomainModel.id.desc()
    )

    lst = list(map(lambda m: model_to_dict(
        model=m,
        # exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'start_date',
            'expire_date',
            # 'real_time_domain_expire_days',
            'real_time_expire_days',
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


@async_task_service.async_task_decorator("自动导入子域名证书")
def auto_import_from_domain(root_domain, group_id=0, user_id=0):
    """
    自动导入顶级域名下包含的子域名到证书列表
    :param root_domain: str
    :param group_id: int
    :param user_id: int
    :return:
    """
    lst = crtsh_api.search(root_domain)

    domain_set = list(set([domain['common_name'] for domain in lst]))

    data = [
        {
            'domain': domain,
            'root_domain': root_domain,
            'port': 443,
            'alias': '',
            'user_id': user_id,
            'group_id': group_id,
        } for domain in domain_set
    ]

    for batch in chunked(data, 500):
        DomainModel.insert_many(batch).on_conflict_ignore().execute()

    # 更新插入的证书
    rows = DomainModel.select().where(
        DomainModel.domain.in_(domain_set)
    )

    for row in rows:
        update_domain_row(row)


def add_domain_from_file(filename, user_id):
    logger.info('user_id: %s, filename: %s', user_id, filename)

    lst = list(domain_util.parse_domain_from_file(filename))

    # 导入分组
    group_name_list = [item.group_name for item in lst]
    group_map = group_service.get_or_create_group_map(group_name_list, user_id)

    lst = [
        {
            'domain': item.domain,
            'root_domain': item.root_domain,
            'port': item.port,
            'alias': item.alias,
            'user_id': user_id,
            'group_id': group_map.get(item.group_name, 0),
        } for item in lst
    ]

    for batch in chunked(lst, 500):
        DomainModel.insert_many(batch).on_conflict_ignore().execute()


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

    content = render_service.render_template('cert-export.csv', {'list': lst})

    filename = datetime.now().strftime("cert_%Y%m%d%H%M%S") + '.csv'

    temp_filename = file_service.resolve_temp_file(filename)
    # print(temp_filename)
    with io.open(temp_filename, 'w', encoding='utf-8') as f:
        f.write(content)

    return filename


def load_domain_expire_days(lst):
    """
    加载域名过期时间字段 Number or None
    :param lst: List[DomainModel dict]
    :return:
    """

    root_domains = [row['root_domain'] for row in lst]

    domain_info_rows = DomainInfoModel.select().where(
        DomainInfoModel.domain.in_(root_domains)
    )

    domain_info_map = {
        row.domain: row.real_domain_expire_days
        for row in domain_info_rows
    }

    for row in lst:
        row['domain_expire_days'] = domain_info_map.get(row['root_domain'])

    return lst


def load_address_count(lst):
    """
    加载主机数量字段
    :param lst: List
    :return:
    """
    row_ids = [row['id'] for row in lst]

    # 主机数量
    address_groups = AddressModel.select(
        AddressModel.domain_id,
        fn.COUNT(AddressModel.id).alias('count')
    ).where(
        AddressModel.domain_id.in_(row_ids)
    ).group_by(AddressModel.domain_id)

    address_group_map = {
        str(row.domain_id): row.count
        for row in address_groups
    }

    for row in lst:
        row['address_count'] = address_group_map.get(str(row['id']), 0)

    return lst
