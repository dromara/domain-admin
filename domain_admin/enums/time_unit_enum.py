# -*- coding: utf-8 -*-
"""
@File    : time_unit_enum.py
@Date    : 2024-11-02
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division


class TimeUnitEnum(object):
    """
    时间单位枚举值
    @since v1.6.56
    """
    # 毫秒
    Millisecond = 1

    # 秒
    Second = 2

    # 分钟
    Minute = 3

    # 小时
    Hour = 4

    # 天
    Day = 5

    # 周
    Week = 6

    # 月
    Month = 7

    # 年
    Year = 8

    @staticmethod
    def get_config():
        return [
            (TimeUnitEnum.Millisecond, '毫秒'),
            (TimeUnitEnum.Second, '秒'),
            (TimeUnitEnum.Minute, '分钟'),
            (TimeUnitEnum.Hour, '小时'),
            (TimeUnitEnum.Day, '天'),
            (TimeUnitEnum.Week, '周'),
            (TimeUnitEnum.Month, '月'),
            (TimeUnitEnum.Year, '年'),
        ]

    @staticmethod
    def get_label(value):
        mapping = {k: v for k, v in TimeUnitEnum.get_config()}
        return mapping.get(value)

    @staticmethod
    def get_value(label):
        mapping = {k: v for v, k in TimeUnitEnum.get_config()}
        return mapping.get(label)

    @staticmethod
    def to_millisecond(value, unit=Second):
        # 基础单位：毫秒
        mapping = {
            TimeUnitEnum.Millisecond: 1,
            TimeUnitEnum.Second: 1000,
            TimeUnitEnum.Minute: 1000 * 60,
            TimeUnitEnum.Hour: 1000 * 60 * 60,
            TimeUnitEnum.Day: 1000 * 60 * 60 * 24,
            TimeUnitEnum.Week: 1000 * 60 * 60 * 24 * 7,
            TimeUnitEnum.Month: 1000 * 60 * 60 * 24 * 30,
            TimeUnitEnum.Year: 1000 * 60 * 60 * 24 * 365,
        }

        return value * mapping.get(unit)
