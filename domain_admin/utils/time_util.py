# -*- coding: utf-8 -*-
"""
@File    : time_util.py
@Date    : 2023-06-03
"""
from dateutil import parser
from datetime import datetime

# 时间格式化
from peewee import DateTimeField

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_time(time_str) -> datetime:
    """
    解析字符串为时间
    :param time_str: str
    :return: str
    """

    return datetime.strptime(
        parser.parse(time_str).astimezone().strftime(DATETIME_FORMAT),
        DATETIME_FORMAT
    )


def get_diff_days(start_date: [datetime, DateTimeField], end_date: [datetime, DateTimeField]):
    """
    获取两个时间对象的时间差天数
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date and end_date \
            and isinstance(start_date, datetime) \
            and isinstance(end_date, datetime):
        return (end_date - start_date).days
    else:
        return 0
