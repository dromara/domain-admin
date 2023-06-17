# -*- coding: utf-8 -*-
"""
domain_util.py
"""

import re

from typing import NamedTuple

import tldextract
from tldextract.tldextract import ExtractResult

from domain_admin.utils import file_util
from domain_admin.utils.cert_util import cert_consts


class ParsedDomain(NamedTuple):
    """
    解析后的domain数据
    """
    domain: str
    root_domain: str
    port: int
    alias: str


def parse_domain(domain):
    """
    解析域名信息
    :param domain:
    :return:
    """
    # print(domain)

    ret = re.match('((http(s)?:)?//)?(?P<domain>[\\w\\._:-]+)/?.*?', domain)
    if ret:
        # print(ret.groups())
        return ret.groupdict().get("domain")
    else:
        return None


def parse_domain_from_csv_file(filename) -> ParsedDomain:
    """
    读取csv文件 适合完整导入
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        # 标题
        first_line = f.readline()
        keys = [filed.strip() for filed in first_line.split(',')]

        # 内容字段
        for line in f.readlines():
            values = [filed.strip() for filed in line.split(',')]
            item = dict(zip(keys, values))

            domain = parse_domain(item.get('域名', ''))
            if ':' in domain:
                domain, port = domain.split(":")

            alias = item.get('备注', '')

            # SSL端口
            port = item.get('端口') or port or cert_consts.SSL_DEFAULT_PORT

            if domain:
                item = ParsedDomain(
                    domain=domain,
                    root_domain=get_root_domain(domain),
                    port=int(port),
                    alias=alias
                )

                yield item


def parse_domain_from_txt_file(filename) -> ParsedDomain:
    """
    读取txt文件 适合快速导入
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        for line in f.readlines():

            domain = parse_domain(line.strip())

            if ':' in domain:
                domain, port = domain.split(":")
            else:
                # SSL默认端口
                port = cert_consts.SSL_DEFAULT_PORT

            if domain:
                yield ParsedDomain(
                    domain=domain,
                    root_domain=get_root_domain(domain),
                    port=int(port),
                    alias=''
                )


def parse_domain_from_file(filename) -> ParsedDomain:
    """
    解析域名文件的工厂方法
    :param filename:
    :return:
    """
    file_type = file_util.get_filename_ext(filename)

    if file_type == 'csv':
        return parse_domain_from_csv_file(filename)
    else:
        return parse_domain_from_txt_file(filename)


def extract_domain(domain: str) -> ExtractResult:
    """
    解析域名
    :param domain:
    :return:
    """
    return tldextract.extract(domain)


def get_root_domain(domain: str) -> str:
    """
    解析出域名和顶级后缀
    :param domain:
    :return:
    """
    extract_result = extract_domain(domain)
    return '.'.join([extract_result.domain, extract_result.suffix])
