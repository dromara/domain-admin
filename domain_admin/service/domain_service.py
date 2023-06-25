# -*- coding: utf-8 -*-
"""
domain_service.py
"""
import traceback
import warnings
from datetime import datetime
from typing import List

from peewee import chunked, fn
from playhouse.shortcuts import model_to_dict

from domain_admin.log import logger
from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.user_model import UserModel
from domain_admin.service import email_service, render_service
from domain_admin.service import file_service
from domain_admin.service import notify_service
from domain_admin.service import system_service
from domain_admin.utils import datetime_util, cert_util, whois_util
from domain_admin.utils import domain_util
from domain_admin.utils.cert_util import cert_common, cert_socket_v2, cert_openssl_v2
from domain_admin.utils.flask_ext.app_exception import AppException, ForbiddenAppException


def update_domain_host_list(domain_row: DomainModel):
    """
    更新ip信息
    :param row:
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
        pass

    lst = [
        {
            'domain_id': domain_row.id,
            'host': domain_host
        } for domain_host in domain_host_list]

    logger.info(lst)

    AddressModel.insert_many(lst).on_conflict_ignore().execute()


def update_domain_address_list_cert(domain_row: DomainModel):
    """
    更新证书信息
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


def update_address_row_info_with_sync_domain_row(address_id: int):
    """
    更新主机信息并同步到与名表
    :param address_id:
    :return:
    """
    address_row = AddressModel.get_by_id(address_id)

    domain_row = DomainModel.get_by_id(address_row.domain_id)

    update_address_row_info(address_row, domain_row)

    sync_address_info_to_domain_info(domain_row)


def sync_address_info_to_domain_info(domain_row: DomainModel):
    """
    同步主机信息到域名信息表
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


def update_cert_info(row: DomainModel):
    """
    更新证书信息
    :param row:
    :return:
    """
    # 获取证书信息
    cert_info = {}

    try:
        cert_info = get_cert_info(row.domain)
    except Exception as e:
        pass

    DomainModel.update(
        start_time=cert_info.get('start_date'),
        expire_time=cert_info.get('expire_date'),
        expire_days=cert_info.get('expire_days', 0),
        total_days=cert_info.get('total_days', 0),
        # ip=cert_info.get('ip', ''),
        connect_status=cert_info.get('connect_status'),
        # detail_raw="",
        check_time=datetime_util.get_datetime(),
        update_time=datetime_util.get_datetime(),
    ).where(
        DomainModel.id == row.id
    ).execute()


def update_domain_row(domain_row: DomainModel):
    """
    更新域名相关数据
    :param domain_row:
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
        # 'ip': info.get('ip', ''),
        'info': info,
    }


def get_domain_info(domain: str):
    """
    获取域名注册信息
    :param domain: 域名
    :param cache: 查询缓存字典
    :return:
    """
    warnings.warn("use cache_domain_info_service.get_domain_info", DeprecationWarning)

    # cache = global_data_service.get_value('update_domain_list_info_cache')

    now = datetime.now()

    # 获取域名信息
    domain_info = {}
    domain_expire_days = 0

    # 解析出域名和顶级后缀
    extract_result = domain_util.extract_domain(domain)
    domain_and_suffix = '.'.join([extract_result.domain, extract_result.suffix])

    # if cache:
    #     domain_info = cache.get(domain_and_suffix)

    if not domain_info:
        try:
            domain_info = whois_util.get_domain_info(domain_and_suffix)
            # if cache:
            #     cache[domain_and_suffix] = domain_info

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
    rows = DomainModel.select().where(
        DomainModel.auto_update == True
    ).order_by(DomainModel.expire_days.asc())

    for row in rows:
        update_domain_row(row)


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


def add_domain_from_file(filename, user_id):
    logger.info('user_id: %s, filename: %s', user_id, filename)

    lst = domain_util.parse_domain_from_file(filename)

    lst = [
        {
            'domain': item.domain,
            'root_domain': item.root_domain,
            'port': item.port,
            'alias': item.alias,
            'user_id': user_id,
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
    with open(temp_filename, 'w') as f:
        f.write(content)

    return filename


def load_domain_expire_days(lst: List):
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


def load_address_count(lst: List):
    """
    加载主机数量字段
    :param lst:
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
