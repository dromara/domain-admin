# -*- coding: utf-8 -*-
"""
由于历史原因，domain指代 SSL证书的域名
"""
from operator import itemgetter

from flask import request, g
from playhouse.shortcuts import model_to_dict, fn

from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import async_task_service, domain_info_service
from domain_admin.service import domain_service
from domain_admin.service import file_service
from domain_admin.utils import datetime_util, domain_util
from domain_admin.utils.cert_util import cert_consts
from domain_admin.utils.flask_ext.app_exception import AppException


def add_domain():
    """
    添加域名
    :return:
    """

    current_user_id = g.user_id

    domain = request.json['domain']

    alias = request.json.get('alias') or ''
    group_id = request.json.get('group_id') or 0
    is_dynamic_host = request.json.get('is_dynamic_host', False)
    port = request.json.get('port') or cert_consts.SSL_DEFAULT_PORT

    data = {
        # 基本信息
        'user_id': current_user_id,
        'domain': domain.strip(),
        'port': int(port),  # fix: TypeError: an integer is required (got type str)
        'root_domain': domain_util.get_root_domain(domain),
        'alias': alias,
        'group_id': group_id,
        'is_dynamic_host': is_dynamic_host,
    }

    row = DomainModel.create(**data)

    domain_service.update_domain_row(row)

    # 顺带添加到域名监测列表
    if not domain_util.is_ipv4(domain):

        first_domain_info_row = DomainInfoModel.select(
            DomainInfoModel.id
        ).where(
            DomainInfoModel.domain == data['root_domain'],
            DomainInfoModel.user_id == current_user_id
        ).first()

        if not first_domain_info_row:
            domain_info_service.add_domain_info(
                domain=domain_util.get_root_domain(domain),
                comment=alias,
                group_id=group_id,
                user_id=current_user_id,
            )

    return {'id': row.id}


def update_domain_by_id():
    """
    更新数据
    id domain alias group_id notify_status
    :return:
    """
    current_user_id = g.user_id

    data = request.json
    domain_id = data.pop('id')

    # domain_service.check_permission_and_get_row(domain_id, current_user_id)

    data['update_time'] = datetime_util.get_datetime()
    data['group_id'] = data.get('group_id') or 0

    DomainModel.update(data).where(
        DomainModel.id == domain_id
    ).execute()

    domain_row = DomainModel.get_by_id(domain_id)

    if domain_row.auto_update:
        domain_service.update_domain_row(domain_row)


def update_domain_expire_monitor_by_id():
    """
    更新监控状态
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json.get('domain_id')

    data = {
        "is_monitor": request.json.get('is_monitor', True)
    }

    DomainModel.update(
        data
    ).where(
        DomainModel.id == domain_id
    ).execute()


def update_domain_field_by_id():
    """
    更新单个数据
    :return:
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']
    field = request.json.get('field')
    value = request.json.get('value')

    if field not in ['auto_update']:
        raise AppException("not allow field")

    data = {
        field: value,
    }

    DomainModel.update(data).where(
        DomainModel.id == domain_id
    ).execute()


def delete_domain_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    # domain_service.check_permission_and_get_row(domain_id, current_user_id)

    DomainModel.delete().where(
        DomainModel.id == domain_id,
        DomainModel.user_id == current_user_id,
    ).execute()

    # 同时移除主机信息
    AddressModel.delete().where(
        AddressModel.domain_id == domain_id
    ).execute()


def delete_domain_by_ids():
    """
    批量删除
    @since v1.2.16
    :return:
    """
    current_user_id = g.user_id

    domain_ids = request.json['ids']

    DomainModel.delete().where(
        DomainModel.id.in_(domain_ids),
        DomainModel.user_id == current_user_id
    ).execute()

    # 同时移除主机信息
    AddressModel.delete().where(
        AddressModel.domain_id.in_(domain_ids)
    ).execute()


def get_domain_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json.get('domain_id') or request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    row = model_to_dict(
        model=row,
        extra_attrs=[
            'real_time_expire_days',
            'domain_url',
            'update_time_label',
        ]
    )

    # 主机数量
    address_count = AddressModel.select().where(
        AddressModel.domain_id == domain_id
    ).count()

    row['address_count'] = address_count

    return row


def update_all_domain_cert_info():
    """
    更新所有域名证书信息
    :return:
    """

    domain_service.update_all_domain_cert_info()


def update_all_domain_cert_info_of_user():
    """
    更新当前用户的所有域名信息
    :return:
    """
    current_user_id = g.user_id

    async_task_service.submit_task(fn=domain_service.update_all_domain_cert_info_of_user, user_id=current_user_id)


def update_domain_row_info_by_id():
    """
    更新域名关联的证书信息
    :return:
    @since v1.3.1
    """
    current_user_id = g.user_id

    # @since v1.2.24 支持参数 domain_id
    domain_id = request.json.get('domain_id') or request.json['id']

    # row = domain_service.check_permission_and_get_row(domain_id, current_user_id)
    row = DomainModel.get_by_id(domain_id)

    domain_service.update_domain_row(row)


def get_all_domain_list_of_user():
    """
    获取用户的所有域名数据
    :return:
    """

    current_user_id = g.user_id
    # temp_filename = domain_service.export_domain_to_file(current_user_id)

    rows = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    lst = [{'domain': row.domain} for row in rows]

    return {
        'list': lst,
        'total': len(lst)
    }


def import_domain_from_file():
    """
    从文件导入域名
    支持 txt 和 csv格式
    :return:
    """
    current_user_id = g.user_id

    update_file = request.files.get('file')

    filename = file_service.save_temp_file(update_file)

    # 导入数据
    domain_service.add_domain_from_file(filename, current_user_id)

    # 异步导入
    # async_task_service.submit_task(fn=domain_service.add_domain_from_file, filename=filename, user_id=current_user_id)

    # 异步查询
    async_task_service.submit_task(fn=domain_service.update_all_domain_cert_info_of_user, user_id=current_user_id)


def export_domain_file():
    """
    导出域名文件
    csv格式
    :return:
    """
    current_user_id = g.user_id

    filename = domain_service.export_domain_to_file(current_user_id)

    return {
        'name': filename,
        'url': file_service.resolve_temp_url(filename)
    }


def domain_relation_group():
    """
    分组关联域名
    :return:
    """
    current_user_id = g.user_id
    # temp_filename = domain_service.export_domain_to_file(current_user_id)
    domain_ids = request.json['domain_ids']
    group_id = request.json['group_id']

    DomainModel.update(
        group_id=group_id
    ).where(
        DomainModel.id.in_(domain_ids)
    ).execute()


def get_domain_list():
    """
    获取域名列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    group_id = request.json.get('group_id')

    order_prop = request.json.get('order_prop') or 'expire_days'
    order_type = request.json.get('order_type') or 'ascending'
    group_ids = request.json.get('group_ids')
    expire_days = request.json.get('expire_days')

    query = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    if keyword:
        query = query.where(DomainModel.domain.contains(keyword))

    if group_ids:
        query = query.where(DomainModel.group_id.in_(group_ids))

    if expire_days is not None:
        if expire_days[0] is None:
            query = query.where(DomainModel.expire_days <= expire_days[1])
        elif expire_days[1] is None:
            query = query.where(DomainModel.expire_days >= expire_days[0])
        else:
            query = query.where(DomainModel.expire_days.between(expire_days[0], expire_days[1]))

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

    total = query.count()
    lst = []

    if total > 0:
        lst = query.order_by(*ordering).paginate(page, size)

        lst = list(map(lambda m: model_to_dict(
            model=m,
            extra_attrs=[
                'expire_days',
                'create_time_label',
                'real_time_expire_days',
                'real_time_ssl_total_days',
                'real_time_ssl_expire_days',
                'domain_url',
                'update_time_label',
            ]
        ), lst))

        # 加载主机数量
        domain_service.load_address_count(lst)

        # 加载域名过期时间
        domain_service.load_domain_expire_days(lst)

    # lst = model_util.list_with_relation_one(lst, 'group', GroupModel)

    return {
        'list': lst,
        'total': total
    }


def get_domain_group_filter():
    """
    获取证书分组筛选器
    :return:
    """

    current_user_id = g.user_id

    # 分组列表数据
    rows = GroupModel.select().where(
        GroupModel.user_id == current_user_id
    )

    # 证书分组统计
    cert_groups = DomainModel.select(
        DomainModel.group_id,
        fn.COUNT(DomainModel.id).alias('count')
    ).group_by(DomainModel.group_id)

    cert_groups_map = {
        str(row.group_id): row.count
        for row in cert_groups
    }

    lst = []
    for row in rows:
        row_dict = model_to_dict(row)
        row_dict['cert_count'] = cert_groups_map.get(str(row.id), 0)
        lst.append(row_dict)

    if cert_groups_map.get('0'):
        lst.append({
            'cert_count': cert_groups_map.get('0'),
            'id': 0,
            'name': '未分组',
        })

    lst.sort(key=itemgetter('cert_count'), reverse=True)

    return {
        'list': lst,
        'total': len(lst),
    }
