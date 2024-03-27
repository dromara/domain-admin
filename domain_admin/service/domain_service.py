# -*- coding: utf-8 -*-
"""
domain_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import io
import time
import traceback
from datetime import datetime, timedelta

from peewee import chunked, fn
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.enums.source_enum import SourceEnum
from domain_admin.log import logger
from domain_admin.model import domain_model
from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.model.user_model import UserModel
from domain_admin.service import file_service, async_task_service
from domain_admin.service import render_service, group_service
from domain_admin.utils import datetime_util, cert_util, file_util, json_util
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
        err = update_address_row_info_wrap(address_row, domain_row)

    sync_address_info_to_domain_info(domain_row)
    return err


def update_address_row_info_wrap(address_row, domain_row):
    """
    更新单个地址信息 的代理方法 增加重试次数
    :param address_row:
    :param domain_row:
    :return: error
    """
    # 最大重试次数
    MAX_RETRY_COUNT = 3
    retry_count = 0
    err = ''

    while True:
        retry_count += 1
        logger.info("retry_count: %s", retry_count)

        err = update_address_row_info(address_row, domain_row)

        if not err or retry_count >= MAX_RETRY_COUNT:
            break

        # sleep
        time.sleep(0.5)

    return err


def update_address_row_info(address_row, domain_row):
    """
    更新单个地址信息
    :param domain_row:
    :param address_row:
    :return: error
    """

    # 获取证书信息
    cert_info = {}

    err = ''
    try:
        cert_info = cert_openssl_v2.get_ssl_cert_by_openssl(
            domain=domain_row.domain,
            host=address_row.host,
            port=domain_row.port,
            ssl_type=domain_row.ssl_type
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

    update_address_row_info_wrap(address_row, domain_row)

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
        pass

    # 移除动态主机行为，都清空自动添加的数据再获取
    AddressModel.delete().where(
        AddressModel.domain_id == domain_row.id,
        AddressModel.source == SourceEnum.AUTO
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
        try:
            update_domain_row(row)
        except Exception as e:
            logger.error(traceback.format_exc())


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
def auto_import_from_domain_async(root_domain, group_id=0, user_id=0):
    auto_import_from_domain(root_domain=root_domain, group_id=group_id, user_id=user_id)

    init_domain_cert_info_of_user(user_id=user_id)


def auto_import_from_domain(root_domain, group_id=0, user_id=0):
    """
    自动导入顶级域名下包含的子域名到证书列表
    :param root_domain: str
    :param group_id: int
    :param user_id: int
    :return:
    """
    logger.info("domain: %s", root_domain)

    lst = crtsh_api.search(root_domain)

    domain_set = set()

    for domain in lst:
        common_name = domain['common_name']

        # 过滤空域名
        if not common_name:
            continue

        # 过滤非主域名下子域
        if not common_name.endswith(root_domain):
            continue

        # 过滤邮箱数据
        if '@' in common_name:
            continue

        # 识别通配符 *.music.163.com -> music.163.com
        if common_name.startswith('*.'):
            common_name = common_name[2:]

        domain_set.add(common_name)

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


def add_domain_from_file(filename, user_id):
    logger.info('user_id: %s, filename: %s', user_id, filename)

    lst = list(domain_util.parse_domain_from_file(filename, domain_model.FIELD_MAPPING))

    # 导入分组
    group_name_list = [item.get('group_name') for item in lst if item.get('group_name')]
    if group_name_list:
        group_map = group_service.get_or_create_group_map(group_name_list, user_id)
    else:
        group_map = {}

    lst = [
        {
            'domain': item['domain'],
            'root_domain': domain_util.get_root_domain(item['domain']),
            'port': item.get('port'),
            'alias': item.get('alias', ''),
            'user_id': user_id,
            'group_id': group_map.get(item.get('group_name'), 0),
        } for item in lst
    ]

    # print(json_util.json_dump(lst))

    # fix: peewee.OperationalError: too many SQL variables
    # https://github.com/mouday/domain-admin/issues/63
    for batch in chunked(lst, 500):
        DomainModel.insert_many(batch).on_conflict_ignore().execute()


def export_domain_to_file(rows, ext):
    """
    导出域名到文件
    :param rows:
    :return:
    """

    # content = render_service.render_template('cert-export.csv', {'list': rows})

    filename = datetime.now().strftime("cert_%Y%m%d%H%M%S") + '.' + ext
    temp_filename = file_service.resolve_temp_file(filename)

    if ext == 'txt':
        lst = [row['domain'] for row in rows]
    else:
        lst = file_util.convert_to_export(rows, domain_model.FIELD_MAPPING)

    file_util.write_data_to_file(temp_filename, lst)

    # temp_filename = file_service.resolve_temp_file(filename)
    # # print(temp_filename)
    # with io.open(temp_filename, 'w', encoding='utf-8') as f:
    #     f.write(content)

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


def get_domain_list_query(keyword, group_id, group_ids, expire_days, user_id, role):
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

    query = DomainModel.select()

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    if keyword:
        query = query.where(DomainModel.domain.contains(keyword))

    if group_ids:
        query = query.where(DomainModel.group_id.in_(group_ids))
    else:
        if role == RoleEnum.ADMIN:
            pass

        elif user_group_ids:
            query = query.where(
                (DomainModel.user_id == user_id)
                | (DomainModel.group_id.in_(user_group_ids))
            )
        else:
            query = query.where(DomainModel.user_id == user_id)

    if expire_days is not None:
        if expire_days[0] is None:
            max_expire_time = datetime.now() + timedelta(days=expire_days[1])
            query = query.where(
                (DomainModel.expire_time <= max_expire_time)
                | (DomainModel.expire_time.is_null(True))
            )
        elif expire_days[1] is None:
            min_expire_time = datetime.now() + timedelta(days=expire_days[0])
            query = query.where(DomainModel.expire_time >= min_expire_time)
        else:
            min_expire_time = datetime.now() + timedelta(days=expire_days[0])
            max_expire_time = datetime.now() + timedelta(days=expire_days[1])

            query = query.where(DomainModel.expire_time.between(min_expire_time, max_expire_time))

    return query


def get_domain_ordering(order_prop='expire_days', order_type='ascending'):
    ordering = []

    # order by expire_days
    if order_prop == 'expire_days':
        if order_type == 'descending':
            ordering.append(DomainModel.expire_time.desc())
        else:
            ordering.append(DomainModel.expire_time.asc())

    # order by connect_status
    elif order_prop == 'connect_status':
        if order_type == 'descending':
            ordering.append(DomainModel.connect_status.desc())
        else:
            ordering.append(DomainModel.connect_status.asc())

    # order by domain
    elif order_prop == 'domain':
        if order_type == 'descending':
            ordering.append(DomainModel.domain.desc())
        else:
            ordering.append(DomainModel.domain.asc())

    # order by group_id
    elif order_prop == 'group_name':
        if order_type == 'descending':
            ordering.append(DomainModel.group_id.desc())
        else:
            ordering.append(DomainModel.group_id.asc())

    # order by port
    elif order_prop == 'port':
        if order_type == 'descending':
            ordering.append(DomainModel.port.desc())
        else:
            ordering.append(DomainModel.port.asc())

    # order by update_time
    elif order_prop == 'update_time':
        if order_type == 'descending':
            ordering.append(DomainModel.update_time.desc())
        else:
            ordering.append(DomainModel.update_time.asc())

    # order by domain_expire_monitor
    elif order_prop == 'domain_expire_monitor':
        if order_type == 'descending':
            ordering.append(DomainModel.domain_expire_monitor.desc())
        else:
            ordering.append(DomainModel.domain_expire_monitor.asc())

    # order by auto_update
    elif order_prop == 'auto_update':
        if order_type == 'descending':
            ordering.append(DomainModel.auto_update.desc())
        else:
            ordering.append(DomainModel.auto_update.asc())
    # order by  is_monitor
    elif order_prop == 'is_monitor':
        if order_type == 'descending':
            ordering.append(DomainModel.is_monitor.desc())
        else:
            ordering.append(DomainModel.is_monitor.asc())

    ordering.append(DomainModel.id.desc())

    return ordering


def init_domain_cert_info_of_user(user_id):
    """
    初始化证书信息
    :param user_id:
    :return:
    """
    # 更新插入的证书
    rows = DomainModel.select().where(
        DomainModel.version == 0,
        DomainModel.user_id == user_id,
    )

    for row in rows:
        update_domain_row(row)
