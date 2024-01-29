# -*- coding: utf-8 -*-
"""
@File    : icp_item.py
@Date    : 2024-01-29
@Author  : Peng Shiyu
"""


class ICPItem(object):
    name = ''
    icp = ''

    def to_dict(self):
        return {
            'name': self.name,
            'icp': self.icp,
        }
