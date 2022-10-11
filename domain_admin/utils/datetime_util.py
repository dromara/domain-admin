# -*- coding: utf-8 -*-
"""
datetime_util.py
"""

from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATE_FORMAT = "%Y-%m-%d"

TIME_FORMAT = "%H:%M:%S"


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

    if seconds > 0:
        lst.append(str(seconds) + 's')

    return ' '.join(lst)


if __name__ == '__main__':
    print(seconds_for_human(100.010))
