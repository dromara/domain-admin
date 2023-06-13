# -*- coding: utf-8 -*-
"""
@File    : auto_release.py
@Date    : 2023-06-09
"""

import glob
import os
import re
from packaging import version

# 项目根路径
ROOT_DIRNAME = os.path.dirname(os.path.dirname(__file__))

# 版本文件路径
VERSION_FILE = glob.glob(f"{ROOT_DIRNAME}/*/version.py", recursive=True)[0]

# 版本的匹配正则
VERSION_REGEX = "VERSION = '(?P<version>\d+\.\d+\.\d+)'"


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def write_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def parse_version(source_text):
    ret = re.search(VERSION_REGEX, source_text)
    return ret.groupdict().get('version')


def replace_version(source_text, new_version):
    return re.sub(VERSION_REGEX, f"VERSION = '{new_version}'", source_text)


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
    os.system(f"git add . && git commit -m 'auto release' && git tag v{new_version} && git push --tag")


if __name__ == '__main__':
    main()
