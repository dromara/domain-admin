# -*- coding: utf-8 -*-
import re


def parse_domain(domain):
    """
    解析域名信息
    :param domain:
    :return:
    """
    ret = re.match('.*?//([a-zA-Z\.0-9]+)/?.*?', domain)
    if ret:
        return ret.groups()[0]
    else:
        return domain


def parse_domain_from_file(filename):
    lst = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            lst.append(parse_domain(line.strip()))

    return lst
