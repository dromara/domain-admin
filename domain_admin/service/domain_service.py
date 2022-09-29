# -*- coding: utf-8 -*-
import json
from functools import cmp_to_key

from playhouse.shortcuts import model_to_dict

from domain_admin.model import DomainModel, UserModel
from domain_admin.service import email_service, render_service
from domain_admin.utils import cert_util, datetime_util
from domain_admin.utils.flask_ext.app_exception import AppException, ForbiddenAppException


def add_domain(data):
    """
    添加域名
    :param data: {
        domain 必传
        user_id 必传
        alias 可选，默认 ""
        group_id 可选，默认 0
     }
    :return:
    """
    user_id = data['user_id']
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
        user_id=user_id,
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
        info = cert_util.get_cert_info(row.domain)
        connect_status = True
    except Exception:
        pass

    DomainModel.update(
        start_time=info.get('start_date'),
        expire_time=info.get('expire_date'),
        ip=info.get('ip'),
        connect_status=connect_status,
        detail_raw=json.dumps(info, ensure_ascii=False),
        check_time=datetime_util.get_datetime(),
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


def update_all_domain_cert_info_of_user(user_id):
    """
    更新用户的所有域名信息
    :return:
    """
    lst = DomainModel.select().where(
        DomainModel.user_id == user_id
    )

    for row in lst:
        update_domain_cert_info(row)


def get_domain_info_list(user_id=None):
    query = DomainModel.select()

    if user_id:
        query = query.where(
            DomainModel.user_id == user_id
        )

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'start_date',
            'expire_date',
            'expire_days',
        ]
    ), query))

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


def check_domain_cert(user_id):
    """
    查询域名证书到期情况
    :return:
    """
    user_row = UserModel.get_by_id(user_id)

    lst = get_domain_info_list(user_id)

    has_expired_domain = False

    for item in lst:
        if item['expire_days'] is None or item['expire_days'] <= user_row.before_expire_days:
            has_expired_domain = True
            break

    if has_expired_domain:
        send_domain_list_email(user_id)


def send_domain_list_email(user_id):
    """
    发送域名信息
    :param user_id:
    :return:
    """
    user_row = UserModel.get_by_id(user_id)

    if not user_row.email_list:
        raise AppException('邮箱未设置')

    lst = get_domain_info_list(user_row.id)

    content = render_service.render_template('domain-cert-email.html', {'list': lst})

    email_service.send_email(
        subject='[ssl]证书过期时间汇总',
        content=content,
        to_addresses=user_row.email_list,
        content_type='html'
    )


def check_permission_and_get_row(domain_id, user_id):
    """
    权限检查
    :param domain_id:
    :param user_id:
    :return:
    """
    row = DomainModel.get_by_id(domain_id)
    if row.user_id != user_id:
        raise ForbiddenAppException()

    return row


if __name__ == '__main__':
    print(get_domain_info_list())
