# -*- coding: utf-8 -*-

from flask import request, g
from peewee import fn
from playhouse.shortcuts import model_to_dict

from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import async_task_service
from domain_admin.service import domain_service, global_data_service
from domain_admin.service import file_service
from domain_admin.utils import datetime_util
from domain_admin.utils.cert_util import cert_consts
from domain_admin.utils.flask_ext.app_exception import AppException


def add_domain():
    """
    添加域名
    :return:
    """

    current_user_id = g.user_id

    domain = request.json.get('domain')

    if not domain:
        raise AppException('参数缺失：domain')

    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id') or 0
    port = request.json.get('port') or cert_consts.SSL_DEFAULT_PORT

    data = {
        # 基本信息
        'user_id': current_user_id,
        'domain': domain,
        'port': port,
        'alias': alias,
        'group_id': group_id,
    }

    row = DomainModel.create(**data)

    domain_service.update_domain_row(row)

    return {'id': row.id}


def update_domain_setting():
    """
    更新域名配置信息
    @since v1.2.13
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['domain_id']

    data = {
        # 域名信息
        'domain_start_time': request.json.get('domain_start_time'),
        'domain_expire_time': request.json.get('domain_expire_time'),
        'domain_auto_update': request.json.get('domain_auto_update'),
        'domain_expire_monitor': request.json.get('domain_expire_monitor'),

        # 证书信息
        # 'start_time': request.json.get('start_time'),
        # 'expire_time': request.json.get('expire_time'),
        # 'auto_update': request.json.get('auto_update'),

        'domain_check_time': datetime_util.get_datetime(),
        'update_time': datetime_util.get_datetime()
    }

    DomainModel.update(data).where(
        DomainModel.id == domain_id
    ).execute()


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

    domain_service.update_domain_row(domain_row)


def update_domain_expire_monitor_by_id():
    """
    更新监控状态
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json.get('domain_id')

    data = {
        "domain_expire_monitor": request.json.get('domain_expire_monitor', True)
    }

    DomainModel.update(
        data
    ).where(
        DomainModel.id == domain_id
    ).execute()


def delete_domain_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    domain_service.check_permission_and_get_row(domain_id, current_user_id)

    DomainModel.delete_by_id(domain_id)

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

    order_prop = request.json.get('order_prop', 'expire_days')
    order_type = request.json.get('order_type', 'ascending')
    group_ids = request.json.get('group_ids')
    expire_days = request.json.get('expire_days')
    domain_expire_days = request.json.get('domain_expire_days')
    connect_status = request.json.get('connect_status')

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

    if domain_expire_days is not None:
        if domain_expire_days[0] is None:
            query = query.where(DomainModel.domain_expire_days <= domain_expire_days[1])
        elif domain_expire_days[1] is None:
            query = query.where(DomainModel.domain_expire_days >= domain_expire_days[0])
        else:
            query = query.where(DomainModel.domain_expire_days.between(domain_expire_days[0], domain_expire_days[1]))

    if connect_status is not None:
        # 连接正常
        if connect_status == 'success':
            connect_status = True
        # 连接异常
        elif connect_status == 'error':
            connect_status = False
        # 状态未知
        elif connect_status == 'unknown':
            connect_status = None

        query = query.where(DomainModel.connect_status == connect_status)

    ordering = []

    # order by expire_days
    if order_prop == 'expire_days':
        if order_type == 'descending':
            ordering.append(DomainModel.expire_days.desc())
        else:
            ordering.append(DomainModel.expire_days.asc())

    # order by domain_expire_days
    elif order_prop == 'domain_expire_days':
        if order_type == 'descending':
            ordering.append(DomainModel.domain_expire_days.desc())
        else:
            ordering.append(DomainModel.domain_expire_days.asc())

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

    ordering.append(DomainModel.id.desc())

    lst = query.order_by(*ordering).paginate(page, size)

    total = query.count()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
            'create_time_label',
            'check_time_label',
            'real_time_expire_days',
            'real_time_ssl_total_days',
            'real_time_ssl_expire_days',
            'real_time_domain_expire_days',
            'domain_url',
            'update_time_label',
        ]
    ), lst))

    # lst = model_util.list_with_relation_one(lst, 'group', GroupModel)

    return {
        'list': lst,
        'total': total
    }


def get_domain_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    return model_to_dict(
        model=row,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
            'real_time_expire_days',
            'real_time_domain_expire_days',
            'detail',
            'group',
            'domain_url',
            'domain_check_time_label',
        ]
    )


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
    # domain_service.update_all_domain_cert_info_of_user(current_user_id)
    # 异步更新
    key = f'update_domain_status:{current_user_id}'
    global_data_service.set_value(key, True)
    async_task_service.submit_task(fn=domain_service.update_all_domain_cert_info_of_user, user_id=current_user_id)


def get_update_domain_status_of_user():
    """
    获取域名信息更新状态
    true：正在更新
    false：更新完毕
    :return:
    """
    current_user_id = g.user_id
    key = f'update_domain_status:{current_user_id}'

    return {
        'status': global_data_service.get_value(key)
    }


def get_check_domain_status_of_user():
    """
    获取证书检查状态
    true：正在更新
    false：更新完毕
    :return:
    """
    current_user_id = g.user_id
    key = f'check_domain_status:{current_user_id}'

    return {
        'status': global_data_service.get_value(key)
    }


def update_domain_cert_info_by_id():
    """
    更新域名证书信息
    :return:
    """
    current_user_id = g.user_id

    # @since v1.2.24 支持参数 domain_id
    domain_id = request.json.get('domain_id') or request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    # domain_service.update_domain_row(row)
    err = domain_service.update_domain_info(row)


def update_domain_row_info_by_id():
    """
    更新域名信息及其关联的证书信息
    :return:
    @since v1.3.1
    """
    current_user_id = g.user_id

    # @since v1.2.24 支持参数 domain_id
    domain_id = request.json.get('domain_id') or request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    err = domain_service.update_domain_row(row)
    if err:
        raise AppException(err)


def send_domain_info_list_email():
    """
    发送域名证书信息到邮箱
    :return:
    """
    current_user_id = g.user_id

    domain_service.send_domain_list_email(current_user_id)


def check_domain_cert():
    """
    检查域名证书信息
    :return:
    """
    current_user_id = g.user_id

    key = f'check_domain_status:{current_user_id}'
    global_data_service.set_value(key, True)

    # # 先更新，再检查
    # domain_service.update_all_domain_cert_info_of_user(current_user_id)
    #
    # domain_service.check_domain_cert(current_user_id)
    # 异步检查更新
    async_task_service.submit_task(fn=domain_service.update_and_check_domain_cert, user_id=current_user_id)


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
