# -*- coding: utf-8 -*-
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DATE_FORMAT = "%Y-%m-%d"


def get_datetime():
    return datetime.now().strftime(DATETIME_FORMAT)


def get_date():
    return datetime.now().strftime(DATE_FORMAT)


def format_datetime(date_time):
    return datetime.strftime(date_time, DATETIME_FORMAT)


def format_date(date_time):
    return datetime.strftime(date_time, DATE_FORMAT)
