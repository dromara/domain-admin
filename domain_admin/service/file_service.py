# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import os

from domain_admin.config import TEMP_DIR, TEMP_DIR_BASE_URL, LOG_DIR
from domain_admin.utils import file_util


def resolve_temp_file(filename):
    return os.path.join(TEMP_DIR, filename)


def resolve_log_file(filename):
    return os.path.join(LOG_DIR, filename)


def resolve_temp_url(filename):
    # return urljoin(TEMP_DIR_BASE_URL, filename)
    return TEMP_DIR_BASE_URL + '/' + filename


def get_temp_filename(ext):
    filename = file_util.get_random_filename(ext)
    return resolve_temp_file(filename)


def save_temp_file(update_file):
    """保存上传的文件"""
    ext = update_file.filename.split('.')[-1]
    filename = get_temp_filename(ext)
    update_file.save(filename)
    return filename


if __name__ == '__main__':
    print(get_temp_filename('txt'))
