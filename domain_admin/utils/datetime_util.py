# -*- coding: utf-8 -*-
"""
datetime_util.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import time
from datetime import datetime
import math
import six

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATETIME_SHORT_FORMAT = "%Y-%m-%d %H:%M"

DATE_FORMAT = "%Y-%m-%d"

TIME_FORMAT = "%H:%M:%S"


def get_timestamp(datetime_obj):
    """
    fix: Python 2.7 AttributeError: 'datetime.datetime' object has no attribute 'timestamp'
    ref: https://stackoverflow.com/questions/50650704/attributeerror-datetime-datetime-object-has-no-attribute-timestamp

    :param datetime_obj:
    :return: int
    """
    return int(time.mktime(datetime_obj.timetuple()))


def get_datetime():
    return datetime.now().strftime(DATETIME_FORMAT)


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, DATETIME_FORMAT)


def get_date():
    return datetime.now().strftime(DATE_FORMAT)


def format_datetime(date_time):
    return datetime.strftime(date_time, DATETIME_FORMAT)


def format_date(date_time):
    return datetime.strftime(date_time, DATE_FORMAT)


def format_time(date_time):
    return datetime.strftime(date_time, TIME_FORMAT)


def format_datetime_label(date_time):
    if not isinstance(date_time, datetime):
        return

    now = datetime.now()

    if now.day == date_time.day:
        return format_time(date_time)
    else:
        return format_date(date_time)


def seconds_for_human(seconds):
    """
    将时间格式化为: 1d 2h 3m 4s
    :param seconds:
    :return:
    """
    second = 1
    minute = second * 60
    hour = minute * 12
    day = hour * 24

    lst = []

    if seconds > day:
        days, seconds = divmod(seconds, day)
        lst.append(str(days) + 'd')

    if seconds > hour:
        hours, seconds = divmod(seconds, hour)
        lst.append(str(hours) + 'h')

    if seconds > minute:
        minutes, seconds = divmod(seconds, minute)
        lst.append(str(minutes) + 'm')

    if seconds >= 0:
        lst.append(str(seconds) + 's')

    return ' '.join(lst)


def time_for_human(time_value):
    """
    格式化时间为人类可读的字符串格式
    :param time_value: {int|string|datetime} time_value 10位时间戳
    :return: string

    时间格式化为：
    刚刚
    1分钟前-56分钟前
    1小时前-23小时前
    1天前-7天前
    2022-10-09 13:33
    """
    if not time_value:
        return

    second = 1
    minute = second * 60
    hour = minute * 60
    day = hour * 24
    day_8 = day * 8

    if isinstance(time_value, datetime):
        time_value = get_timestamp(time_value)

    if isinstance(time_value, six.text_type):
        time_value = time.mktime(time.strptime(time_value, DATETIME_FORMAT))

    now_time = time.time()

    duration = now_time - time_value

    if duration < minute:
        return '刚刚'
    elif duration < hour:
        return six.text_type(int(duration / minute)) + '分钟前'
    elif duration < day:
        return six.text_type(int(duration / hour)) + '小时前'
    elif duration < day_8:
        return six.text_type(int(duration / day)) + '天前'
    else:
        return time.strftime(DATE_FORMAT, time.localtime(time_value))


def get_diff_time(start_date, end_date):
    """
    获取两个时间对象的时间差秒数
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date and end_date \
            and isinstance(start_date, datetime) \
            and isinstance(end_date, datetime):
        return get_timestamp(end_date) - get_timestamp(start_date)
    else:
        return 0


if __name__ == '__main__':
    print(time_for_human(1665381270))
    # 2天前

    print(time_for_human(datetime.now()))
    # 刚刚

    print(time_for_human(time.time() - 100))
    # 1分钟前

    print(time_for_human('2022-10-10 13:33:11'))
    # 2天前

    print(get_timestamp(datetime.now()))
