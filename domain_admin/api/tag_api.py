# -*- coding: utf-8 -*-
"""
@File    : tag_api.py
@Date    : 2023-11-05
"""
from flask import request

from domain_admin.model.tag_model import TagModel


def get_tag_by_id():
    """
    添加标签
    :return:
    """
    tag_id = request.json['tag_id']

    return TagModel.get_by_id(tag_id)


def add_tag():
    """
    添加标签
    :return:
    """
    name = request.json['name']

    TagModel.create(name=name)


def update_tag_by_id():
    """
    添加标签
    :return:
    """
    tag_id = request.json['tag_id']
    name = request.json['name']

    TagModel.update(
        name=name
    ).where(
        TagModel.id == tag_id
    ).execute()


def get_all_tag_list():
    """
    获取所有标签，用于筛选器
    :return:
    """
    query = TagModel.select()

    lst = list(query)

    return {
        'list': lst,
        'total': len(lst),
    }


def get_tag_list():
    """
    获取所有标签，用于列表显示
    :return:
    """
    keyword = request.json.get('keyword')

    query = TagModel.select()

    if keyword:
        query = query.where(TagModel.name.contains(keyword))

    query = query.order_by(TagModel.id.desc())

    lst = list(query)

    return {
        'list': lst,
        'total': len(lst),
    }


def delete_tag_by_id():
    """
    删除标签
    :return:
    """
    tag_id = request.json.get('tag_id')

    TagModel.delete_by_id(tag_id)
