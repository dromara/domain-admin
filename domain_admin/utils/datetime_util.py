# -*- coding: utf-8 -*-
from datetime import datetime

import pendulum

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
