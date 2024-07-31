# -*- coding: utf-8 -*-
"""
@File    : tag_api.py
@Date    : 2023-11-05
"""
from flask import request, g

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.model.tag_model import TagModel
from domain_admin.service import auth_service
from domain_admin.utils.flask_ext.app_exception import DataNotFoundAppException


@auth_service.permission(role=RoleEnum.USER)
def get_tag_by_id():
    """
    添加标签
    :return:
    """
    current_user_id = g.user_id

    tag_id = request.json['tag_id']

    # data check
    tag_row = TagModel.select().where(
        TagModel.id == tag_id,
        TagModel.user_id == current_user_id,
    ).first()

    if not tag_row:
        raise DataNotFoundAppException()

    return tag_row


@auth_service.permission(role=RoleEnum.USER)
def add_tag():
    """
    添加标签
    :return:
    """
    current_user_id = g.user_id

    name = request.json['name']

    TagModel.create(
        name=name,
        user_id=current_user_id
    )


@auth_service.permission(role=RoleEnum.USER)
def update_tag_by_id():
    """
    添加标签
    :return:
    """
    current_user_id = g.user_id

    tag_id = request.json['tag_id']
    name = request.json['name']

    # data check
    tag_row = TagModel.select().where(
        TagModel.id == tag_id,
        TagModel.user_id == current_user_id,
    ).first()

    if not tag_row:
        raise DataNotFoundAppException()

    TagModel.update(
        name=name
    ).where(
        TagModel.id == tag_row.id
    ).execute()


@auth_service.permission(role=RoleEnum.USER)
def get_all_tag_list():
    """
    获取所有标签，用于筛选器
    :return:
    """
    current_user_id = g.user_id

    query = TagModel.select().where(
        TagModel.user_id == current_user_id
    )

    lst = list(query)

    return {
        'list': lst,
        'total': len(lst),
    }


@auth_service.permission(role=RoleEnum.USER)
def get_tag_list():
    """
    获取所有标签，用于列表显示
    :return:
    """
    current_user_id = g.user_id

    keyword = request.json.get('keyword')

    query = TagModel.select().where(
        TagModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(TagModel.name.contains(keyword))

    query = query.order_by(TagModel.id.desc())

    lst = list(query)

    return {
        'list': lst,
        'total': len(lst),
    }


@auth_service.permission(role=RoleEnum.USER)
def delete_tag_by_id():
    """
    删除标签
    :return:
    """
    current_user_id = g.user_id

    tag_id = request.json.get('tag_id')

    # data check
    tag_row = TagModel.select().where(
        TagModel.id == tag_id,
        TagModel.user_id == current_user_id,
    ).first()

    if not tag_row:
        raise DataNotFoundAppException()

    TagModel.delete_by_id(tag_row.id)
