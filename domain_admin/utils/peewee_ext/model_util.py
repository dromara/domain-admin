# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division


def list_with_relation_one(lst, field, model):
    """
    获取一对一 关联对象
    :param lst: list
    :param field: 字段名称
    :param model: 模型对象
    :return: list
    """

    field_id = field + '_id'
    field_ids = set(map(lambda item: item[field_id], lst))

    field_models = model.select().where(
        model.id.in_(field_ids)
    )

    field_map = {}
    for field_model in field_models:
        field_map[field_model.id] = field_model

    for row in lst:
        row[field] = field_map.get(row[field_id])

    return lst


def list_with_relation_many(lst, field, model, limit=None):
    """待完成"""
    pass

    # field_id = field + '_id'
    # field_ids = set(map(lambda item: item['id'], lst))
    #
    # query = model.select().where(
    #     model.id.in_(field_ids)
    # )
    #
    # if limit:
    #     query = query.limit(limit)
    #
    # field_models = query
    #
    # field_map = {}
    # for field_model in field_models:
    #     field_model_list = field_map.get(field_model.id, [])
    #
    #     field_map[field_model.id] = field_model_list
    #
    # for row in lst:
    #     row[field] = field_map.get(row[field_id])
    #
    # return lst
