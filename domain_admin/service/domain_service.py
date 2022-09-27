# -*- coding: utf-8 -*-
import json
from functools import cmp_to_key
from operator import itemgetter

from playhouse.shortcuts import model_to_dict

from domain_admin.config import BEFORE_EXPIRE_DAYS, MAIL_TO_ADDRESSES
from domain_admin.model import DomainModel, GroupModel
from domain_admin.service import email_service, render_service
from domain_admin.utils import cert_util, datetime_util
from domain_admin.utils.cert_util import get_cert_info
from domain_admin.utils.datetime_util import get_datetime
from domain_admin.utils.peewee_ext.model_util import list_with_relation_one


def add_domain(data):
    """
    添加域名
    :param data: { domain, alias, group_id }
    :return:
    """
    domain = data['domain']
    alias = data.get('alias', '')
    group_id = data.get('group_id', 0)

    connect_status = False

    info = {}

    try:
        info = cert_util.get_cert_info(domain)
        connect_status = True
    except Exception:
        pass

    row = DomainModel.create(
        domain=domain,
        alias=alias,
        group_id=group_id,
        start_time=info.get('start_date'),
        expire_time=info.get('expire_date'),
        ip=info.get('ip'),
        connect_status=connect_status,
        detail_raw=json.dumps(info, ensure_ascii=False),
        check_time=datetime_util.get_datetime(),
    )

    return row


def update_domain_cert_info(row):
    """
    更新域名的证书信息
    :param row:
    :return:
    """

    connect_status = False

    info = {}

    try:
        info = get_cert_info(row.domain)
        connect_status = True
    except Exception:
        pass

    DomainModel.update(
        start_time=info.get('start_date'),
        expire_time=info.get('expire_date'),
        ip=info.get('ip'),
        connect_status=connect_status,
        detail_raw=json.dumps(info, ensure_ascii=False),
        check_time=get_datetime(),
    ).where(
        DomainModel.id == row.id
    ).execute()


def update_all_domain_cert_info():
    """
    更新所有域名信息
    :return:
    """
    lst = DomainModel.select()
    for row in lst:
        update_domain_cert_info(row)


def get_domain_info_list():
    lst = DomainModel.select()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'start_date',
            'expire_date',
            'expire_days',
        ]
    ), lst))

    def compare(a, b):
        if a['expire_days'] and b['expire_days']:
            return a['expire_days'] - b['expire_days']
        else:
            if a['expire_days']:
                return a['expire_days']
            else:
                return -b['expire_days']

    lst = sorted(lst, key=cmp_to_key(compare))

    return lst


def check_domain_cert():
    """
    查询域名证书到期情况
    :return:
    """
    lst = get_domain_info_list()

    has_expired_domain = False

    for item in lst:
        if item['expire_days'] is None or item['expire_days'] <= BEFORE_EXPIRE_DAYS:
            has_expired_domain = True
            break

    if has_expired_domain:
        send_domain_list_email(MAIL_TO_ADDRESSES)


def send_domain_list_email(to_addresses):
    """
    发送域名信息
    :param to_addresses:
    :return:
    """
    lst = get_domain_info_list()

    content = render_service.render_template('domain-cert-email.html', {'list': lst})

    email_service.send_email(
        subject='[ssl]证书过期时间汇总',
        content=content,
        to_addresses=to_addresses,
        content_type='html'
    )


if __name__ == '__main__':
    print(get_domain_info_list())
