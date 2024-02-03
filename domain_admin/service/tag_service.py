# -*- coding: utf-8 -*-
"""
@File    : tag_service.py
@Date    : 2023-11-05
"""
from domain_admin.model.tag_model import TagModel


def add_tags(tags):
    if not tags:
        return

    lst = set(tags)

    tag_rows = TagModel.select(TagModel.name).where(
        TagModel.name.in_(lst)
    )

    tags = set([tag_row.name for tag_row in tag_rows])
    lst = lst - tags

    lst = [
        {
            'name': tag
        } for tag in lst if tag
    ]

    if lst and len(lst) > 0:
        TagModel.insert_many(lst).on_conflict_ignore().execute()
