# -*- coding: utf-8 -*-
"""
datetime_util.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import sys
import time
from datetime import datetime
import math
import six
from domain_admin import i18n

DATETIME_WITH_MICROSECOND_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATETIME_SHORT_FORMAT = "%Y-%m-%d %H:%M"

DATE_FORMAT = "%Y-%m-%d"

TIME_FORMAT = "%H:%M:%S"


class TimeEnum(object):
    Second = 1
    Minute = 60 * Second
    Hour = 60 * Minute
    Day = 24 * Hour


def get_timestamp(datetime_obj):
    """
    fix: Python 2.7 AttributeError: 'datetime.datetime' object has no attribute 'timestamp'
    ref: https://stackoverflow.com/questions/50650704/attributeerror-datetime-datetime-object-has-no-attribute-timestamp

    :param datetime_obj:
    :return: int
    """
    return int(time.mktime(datetime_obj.timetuple()))


def get_timestamp_with_microsecond(datetime_obj):
    """
    fix: Python 2.7 AttributeError: 'datetime.datetime' object has no attribute 'timestamp'
    ref: https://stackoverflow.com/questions/50650704/attributeerror-datetime-datetime-object-has-no-attribute-timestamp

    :param datetime_obj:
    :return: int
    """
    if sys.version_info[0] < 3 or sys.version_info[1] < 4:
        # python version < 3.3
        return int(time.mktime(datetime_obj.timetuple()) * 1000)
    else:
        return int(datetime_obj.timestamp() * 1000)


def get_datetime():
    return datetime.now().strftime(DATETIME_FORMAT)


def get_datetime_with_microsecond():
    return datetime.now().strftime(DATETIME_WITH_MICROSECOND_FORMAT)


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


def microsecond_for_human(value):
    """
    将时间格式化为: 1d 2h 3m 4s 5ms
    :param value:
    :return:
    """
    if value is None:
        return

    MICROSECOND = 1
    SECOND = MICROSECOND * 1000
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    lst = []

    if value >= DAY:
        days, value = divmod(value, DAY)
        lst.append(str(days) + 'd')

    if value >= HOUR:
        hours, value = divmod(value, HOUR)
        lst.append(str(hours) + 'h')

    if value >= MINUTE:
        minutes, value = divmod(value, MINUTE)
        lst.append(str(minutes) + 'm')

    if value >= SECOND:
        seconds, value = divmod(value, SECOND)
        lst.append(str(seconds) + 's')

    if value > 0:
        lst.append(str(value) + 'ms')

    if len(lst) == 0:
        lst.append('0ms')

    return ' '.join(lst)


def seconds_for_human(seconds):
    """
    将时间格式化为: 1d 2h 3m 4s
    :param seconds:
    :return:
    """
    return microsecond_for_human(seconds * 1000)


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
        return i18n.translate('刚刚')
    elif duration < hour:
        return six.text_type(int(duration / minute)) + i18n.translate('分钟前')
    elif duration < day:
        return six.text_type(int(duration / hour)) + i18n.translate('小时前')
    elif duration < day_8:
        return six.text_type(int(duration / day)) + i18n.translate('天前')
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


def get_diff_time_with_microsecond(start_date, end_date):
    """
    获取两个时间对象的时间差秒数
    :param start_date:
    :param end_date:
    :return: int
    """
    if start_date and end_date \
            and isinstance(start_date, datetime) \
            and isinstance(end_date, datetime):
        return get_timestamp_with_microsecond(end_date) - get_timestamp_with_microsecond(start_date)
    else:
        return 0


def is_less_than(source_date, target_date):
    # source_date - target_date < 0
    return get_diff_time(target_date, source_date) < 0


def is_greater_than(source_date, target_date):
    # source_date - target_date > 0
    return get_diff_time(target_date, source_date) > 0
