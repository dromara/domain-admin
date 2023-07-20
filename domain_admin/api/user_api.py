# -*- coding: utf-8 -*-
"""
user_api.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request, g
from playhouse.shortcuts import model_to_dict, fn

from domain_admin.config import DEFAULT_BEFORE_EXPIRE_DAYS
from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.notify_model import NotifyModel
from domain_admin.model.user_model import UserModel
from domain_admin.utils import datetime_util, bcrypt_util, secret_util
from domain_admin.utils.flask_ext.app_exception import AppException


def get_user_info():
    """
    获取当前用户信息
    :return:
    """
    current_user_id = g.user_id

    row = UserModel.get_by_id(current_user_id)

    return model_to_dict(
        model=row,
        exclude=[UserModel.password],
    )


def update_user_info():
    """
    更新当前用户信息
    :return:
    """
    current_user_id = g.user_id

    # avatar_url = request.json.get('avatar_url')
    before_expire_days = request.json.get('before_expire_days') or DEFAULT_BEFORE_EXPIRE_DAYS
    # email_list = request.json.get('email_list')

    UserModel.update({
        # 'avatar_url': avatar_url,
        'before_expire_days': int(before_expire_days),
        # 'email_list_raw': json.dumps(email_list, ensure_ascii=False),
        'update_time': datetime_util.get_datetime()
    }).where(
        UserModel.id == current_user_id
    ).execute()


def update_user_password():
    """
    更新用户密码
    :return:
    """
    current_user_id = g.user_id

    password = request.json.get('password')
    new_password = request.json.get('new_password')

    user_row = UserModel.get_by_id(current_user_id)

    if not bcrypt_util.check_password(password, user_row.password):
        raise AppException('旧密码不正确')

    UserModel.update(
        {
            'password': bcrypt_util.encode_password(new_password),
        }
    ).where(
        UserModel.id == current_user_id
    ).execute()


def get_user_list():
    """
    获取用户列表
    :return:
    """
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')

    query = UserModel.select()

    if keyword:
        query = query.where(UserModel.username.contains(keyword))

    total = query.count()

    lst = query.order_by(
        UserModel.create_time.desc(),
        UserModel.id.desc(),
    ).paginate(page, size)

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[
            UserModel.password,
        ]
    ), lst))

    row_ids = [row['id'] for row in lst]

    # 证书数量
    domain_groups = DomainModel.select(
        DomainModel.user_id,
        fn.COUNT(DomainModel.id).alias('count')
    ).where(
        DomainModel.user_id.in_(row_ids)
    ).group_by(DomainModel.user_id)

    domain_groups_map = {
        str(row.user_id): row.count
        for row in domain_groups
    }

    for row in lst:
        row['cert_count'] = domain_groups_map.get(str(row['id']), 0)

    # 域名数量
    domain_info_groups = DomainInfoModel.select(
        DomainInfoModel.user_id,
        fn.COUNT(DomainInfoModel.id).alias('count')
    ).where(
        DomainInfoModel.user_id.in_(row_ids)
    ).group_by(DomainInfoModel.user_id)

    domain_info_groups_map = {
        str(row.user_id): row.count
        for row in domain_info_groups
    }

    for row in lst:
        row['domain_count'] = domain_info_groups_map.get(str(row['id']), 0)

    # 通知渠道
    notify_groups = NotifyModel.select(
        NotifyModel.user_id,
        fn.COUNT(NotifyModel.id).alias('count')
    ).where(
        NotifyModel.user_id.in_(row_ids)
    ).group_by(NotifyModel.user_id)

    notify_groups_map = {
        str(row.user_id): row.count
        for row in notify_groups
    }

    for row in lst:
        row['notify_count'] = notify_groups_map.get(str(row['id']), 0)

    # 分组数量
    group_groups = GroupModel.select(
        GroupModel.user_id,
        fn.COUNT(GroupModel.id).alias('count')
    ).where(
        GroupModel.user_id.in_(row_ids)
    ).group_by(GroupModel.user_id)

    group_groups_map = {
        str(row.user_id): row.count
        for row in group_groups
    }

    for row in lst:
        row['group_count'] = group_groups_map.get(str(row['id']), 0)

    return {
        'list': lst,
        'total': total
    }


def add_user():
    """
    添加用户
    :return:
    """
    username = request.json.get('username')
    password = request.json.get('password')

    row = UserModel.select().where(
        UserModel.username == username
    ).get_or_none()

    if row:
        raise AppException('用户已存在')

    UserModel.create(
        username=username,
        password=bcrypt_util.encode_password(password)
    )


def update_user_status():
    """
    更新账号可用状态
    :return:
    """
    user_id = request.json.get('user_id')
    status = request.json.get('status')

    UserModel.update({
        'status': status
    }).where(
        UserModel.id == user_id
    ).execute()


def reset_user_password():
    """
    重置用户密码
    :return:
    """
    user_id = request.json.get('user_id')

    password = secret_util.get_random_password()

    UserModel.update({
        'password': bcrypt_util.encode_password(password)
    }).where(
        UserModel.id == user_id
    ).execute()

    return {
        'password': password
    }


def delete_user():
    """
    删除用户账号
    :return:
    """
    user_id = request.json.get('user_id')

    UserModel.delete_by_id(user_id)
