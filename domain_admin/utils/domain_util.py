# -*- coding: utf-8 -*-
import re
import tldextract
from tldextract.tldextract import ExtractResult

from domain_admin.utils import file_util


def parse_domain(domain):
    """
    解析域名信息
    :param domain:
    :return:
    """
    ret = re.match('.*?/?/?([a-zA-Z\\.0-9_:-]+)/?.*?', domain)
    if ret:
        return ret.groups()[0]
    else:
        return None


def parse_domain_from_csv_file(filename):
    """
    读取csv文件 适合完整导入
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        # 标题
        first_line = f.readline()
        first_line_fields = [filed.strip() for filed in first_line.split(',')]
        # 域名
        if '域名' in first_line_fields:
            domain_index = first_line_fields.index('域名')

        if '备注' in first_line_fields:
            alias_index = first_line_fields.index('备注')

        # 内容字段
        for line in f.readlines():
            # 域名,备注
            fields = line.split(',')

            if len(fields) > domain_index:
                domain = parse_domain(fields[domain_index].strip())

            if len(fields) > alias_index:
                alias = fields[alias_index].strip()

            if domain:
                item = {
                    'domain': domain,
                    'alias': alias,
                }
                yield item


def parse_domain_from_txt_file(filename):
    """
    读取txt文件 适合快速导入
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        for line in f.readlines():

            domain = parse_domain(line.strip())

            if domain:
                yield {
                    'domain': domain,
                }


def parse_domain_from_file(filename):
    # lst = []
    file_type = file_util.get_filename_ext(filename)
    print('file_type', file_type)
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
