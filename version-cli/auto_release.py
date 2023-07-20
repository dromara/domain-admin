# -*- coding: utf-8 -*-
"""
@File    : auto_release.py
@Date    : 2023-06-09
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import six

# fix: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
if six.PY2:
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')

import glob
import io
import os
import re
from datetime import datetime

from packaging import version

# 项目根路径
ROOT_DIRNAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 版本文件路径
VERSION_FILE = glob.glob("{}/*/version.py".format(ROOT_DIRNAME))[0]

# 版本的匹配正则
VERSION_REGEX = "VERSION = '(?P<version>\d+\.\d+\.\d+)'"

# CHANGELOG
CHANGELOG_FILE = os.path.join(ROOT_DIRNAME, 'CHANGELOG.md')


def read_file(filename):
    with io.open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filename, text):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def parse_version(source_text):
    ret = re.search(VERSION_REGEX, source_text)
    return ret.groupdict().get('version')


def replace_version(source_text, new_version):
    return re.sub(VERSION_REGEX, "VERSION = '{}'".format(new_version), source_text)


def git_commit_log(version):
    """
    ref:
    git log 查看提交记录
    https://www.cnblogs.com/lsgxeva/p/9485874.html

    :param version:
    :return:
    """
    cmd = 'git log v{}.. --pretty=format:"%s"'.format(version)
    # cmd = 'git log v1.4.34.. --pretty=format:"%s"'

    ret = os.popen(cmd)
    return ret.read()


def get_current_version():
    source_text = read_file(VERSION_FILE)

    return parse_version(source_text)


def get_next_version(current_version):
    parsed_version = version.parse(current_version)

    return '.'.join(str(item) for item in [
        parsed_version.major,
        parsed_version.minor,
        parsed_version.micro + 1])


def modify_changelog_file(data):
    with io.open(CHANGELOG_FILE, "r+", encoding='utf-8') as f:
        old = f.read()
        f.seek(0)
        f.write(data)
        f.write(old)


def update_changelog_file(current_version, next_version):
    changelog = get_changelog(current_version, next_version)
    modify_changelog_file(changelog)


def get_changelog(version, next_version):
    commit_log = git_commit_log(version)
    update_info = '\n'.join(['    - {}'.format(line) for line in commit_log.split('\n')])
    changelog = """- v{version}({date})
{update_info}

""".format(version=next_version, date=datetime.now().strftime('%Y-%m-%d'), update_info=update_info)
    return changelog


def release(next_version):
    # 提交代码
    os.system(
        "git add . && git commit -m 'release v{}' && git tag v{} && git push && git push --tag".format(
            next_version, next_version)
    )


def main():
    source_text = read_file(VERSION_FILE)

    current_version = parse_version(source_text)

    next_version = get_next_version(current_version)

    update_changelog_file(current_version, next_version)

    target_text = replace_version(source_text, next_version)

    write_file(VERSION_FILE, target_text)
    print(current_version, '=>', next_version)

    release(next_version)


if __name__ == '__main__':
    main()
