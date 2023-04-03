# -*- coding: utf-8 -*-
import re
import tldextract
from tldextract.tldextract import ExtractResult


def parse_domain(domain):
    """
    解析域名信息
    :param domain:
    :return:
    """
    ret = re.match('.*?//([a-zA-Z\\.0-9_:-]+)/?.*?', domain)
    if ret:
        return ret.groups()[0]
    else:
        return domain


def parse_domain_from_file(filename):
    # lst = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            yield parse_domain(line.strip())


def extract_domain(domain: str) -> ExtractResult:
    """
    解析域名
    :param domain:
    :return:
    """
    return tldextract.extract(domain)
