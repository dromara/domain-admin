# -*- coding: utf-8 -*-

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import domain_service, global_data_service
from domain_admin.service import file_service
from domain_admin.service import async_task_service
from domain_admin.utils import datetime_util
from domain_admin.utils.flask_ext.app_exception import AppException
from domain_admin.utils.peewee_ext import model_util


def add_domain():
    """
    添加域名
    :return:
    """

    current_user_id = g.user_id

    domain = request.json.get('domain')
    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id') or 0

    if not domain:
        raise AppException('参数缺失：domain')

    row = domain_service.add_domain({
        'user_id': current_user_id,
        'domain': domain,
        'alias': alias,
        'group_id': group_id,
    })

    domain_service.update_domain_cert_info(row)

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

    domain_service.check_permission_and_get_row(domain_id, current_user_id)

    data['update_time'] = datetime_util.get_datetime()
    data['group_id'] = data.get('group_id') or 0

    DomainModel.update(data).where(
        DomainModel.id == domain_id
    ).execute()

    domain_row = DomainModel.get_by_id(domain_id)

    domain_service.update_domain_cert_info(domain_row)


def delete_domain_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    domain_service.check_permission_and_get_row(domain_id, current_user_id)

    DomainModel.delete_by_id(domain_id)


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

    query = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    if keyword:
        query = query.where(DomainModel.domain.contains(keyword))

    ordering = []
    if order_prop == 'expire_days':
        if order_type == 'descending':
            ordering.append(DomainModel.expire_days.desc())
        else:
            ordering.append(DomainModel.expire_days.asc())

    elif order_prop == 'domain_expire_days':
        if order_type == 'descending':
            ordering.append(DomainModel.domain_expire_days.desc())
        else:
            ordering.append(DomainModel.domain_expire_days.asc())

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
            'real_time_domain_expire_days',
            'domain_url',
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

    domain_id = request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    domain_service.update_domain_cert_info(row)


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

    # 异步导入
    async_task_service.submit_task(fn=domain_service.add_domain_from_file, filename=filename, user_id=current_user_id)


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
