# -*- coding: utf-8 -*-
import re

from domain_admin.utils.cert_util.cert_consts import SSL_DEFAULT_PORT


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

def remove_default_ssl_port(domain):
    if domain.endswith(':' + str(SSL_DEFAULT_PORT)):
        return domain.split(':')[0]
