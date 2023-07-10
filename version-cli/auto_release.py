# -*- coding: utf-8 -*-
"""
@File    : auto_release.py
@Date    : 2023-06-09
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import six

if six.PY2:
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')

import io
import glob
import os
import re
from packaging import version

# 项目根路径
ROOT_DIRNAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 版本文件路径
VERSION_FILE = glob.glob("{}/*/version.py".format(ROOT_DIRNAME))[0]

# 版本的匹配正则
VERSION_REGEX = "VERSION = '(?P<version>\d+\.\d+\.\d+)'"


def read_file(filename):
    with io.open(filename, 'r', encoding='utf-8') as f:
        # with open(filename, 'r') as f:
        return f.read()


def write_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def parse_version(source_text):
    ret = re.search(VERSION_REGEX, source_text)
    return ret.groupdict().get('version')


def replace_version(source_text, new_version):
    return re.sub(VERSION_REGEX, "VERSION = '{}'".format(new_version), source_text)


def update_version(current_version):
    parsed_version = version.parse(current_version)

    return '.'.join(str(item) for item in [
        parsed_version.major,
        parsed_version.minor,
        parsed_version.micro + 1])


def main():
    source_text = read_file(VERSION_FILE)

    current_version = parse_version(source_text)

    new_version = update_version(current_version)

    target_text = replace_version(source_text, new_version)

    write_file(VERSION_FILE, target_text)
    print(new_version)

    # 提交代码
    os.system("git add . && git commit -m 'auto release' && git tag v{} && git push --tag".format(new_version))


if __name__ == '__main__':
    main()
