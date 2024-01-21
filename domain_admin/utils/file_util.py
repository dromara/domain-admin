# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import uuid

from domain_admin.utils import excel_util, csv_util, txt_util

# 文件读取配置
read_config = {
    'xlsx': excel_util.read_excel,
    'csv': csv_util.read_csv,
    'txt': txt_util.read_txt,
}

# 文件写入配置
write_config = {
    'xlsx': excel_util.write_excel,
    'csv': csv_util.write_csv,
    'txt': txt_util.write_txt,
}


def get_random_filename(ext):
    """
    获取一个随机文件名
    :param ext: str
    :return:
    """
    return str(uuid.uuid4()) + '.' + ext


def get_filename_ext(filename):
    """
    获取文件名的扩展名
    :param filename:
    :return:
    """
    return filename.split('.')[-1]


def read_data_from_file(filename):
    file_type = get_filename_ext(filename)

    if file_type in read_config:
        return read_config[file_type](filename)
    else:
        raise Exception('not support .{}'.format(file_type))


def write_data_to_file(filename, rows):
    file_type = get_filename_ext(filename)

    if file_type in write_config:
        return write_config[file_type](filename, rows)
    else:
        raise Exception('not support .{}'.format(file_type))


def convert_to_export(rows, field_mapping):
    lst = []
    for row in rows:
        data = {}
        for item in field_mapping:
            data[item['name']] = row.get(item['field'], '')

        lst.append(data)

    return lst


def convert_to_import(rows, field_mapping):
    lst = []
    for row in rows:
        data = {
            item['field']: row.get(item['name'], item.get('default_value', ''))
            for item in field_mapping
        }

        lst.append(data)

    return lst
