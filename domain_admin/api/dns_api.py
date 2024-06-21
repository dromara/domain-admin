# -*- coding: utf-8 -*-
"""
@File    : dns_api.py
@Date    : 2023-07-29
"""
from flask import request, g

from domain_admin.config import DEFAULT_SSH_PORT
from domain_admin.enums.dns_type_enum import DnsTypeEnum
from domain_admin.log import logger
from domain_admin.model.dns_model import DnsModel
from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.service import issue_certificate_service
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.open_api import aliyun_domain_api
from domain_admin.utils.open_api.aliyun_domain_api import RecordTypeEnum


def add_dns():
    """
    添加Dns
    :return:
    """
    current_user_id = g.user_id

    dns_type_id = request.json.get('dns_type_id') or DnsTypeEnum.ALIYUN
    name = request.json['name']
    access_key = request.json['access_key']
    secret_key = request.json['secret_key']

    row = DnsModel.create(
        user_id=current_user_id,
        dns_type_id=dns_type_id,
        name=name,
        access_key=access_key,
        secret_key=secret_key,
    )

    return row


def update_dns_by_id():
    """
    更新Dns
    :return:
    """
    current_user_id = g.user_id

    dns_type_id = request.json.get('dns_type_id') or DnsTypeEnum.ALIYUN
    dns_id = request.json['dns_id']
    name = request.json['name']
    access_key = request.json['access_key']
    secret_key = request.json['secret_key']

    DnsModel.update(
        dns_type_id=dns_type_id,
        name=name,
        access_key=access_key,
        secret_key=secret_key,
    ).where(
        DnsModel.id == dns_id
    ).execute()


def get_dns_by_id():
    """
    获取Dns
    :return:
    """
    dns_id = request.json['dns_id']

    return DnsModel.get_by_id(dns_id)


def delete_dns_by_id():
    """
    移除Dns
    :return:
    """
    dns_id = request.json['dns_id']

    return DnsModel.delete_by_id(dns_id)


def get_dns_list():
    """
    Dns列表
    :return:
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    dns_type_id = request.json.get('dns_type_id')

    query = DnsModel.select().where(
        DnsModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(DnsModel.name.contains(keyword))
    if dns_type_id:
        query = query.where(DnsModel.dns_type_id == dns_type_id)

    total = query.count()

    rows = query.order_by(
        DnsModel.create_time.desc(),
        DnsModel.id.desc()
    )

    return {
        'list': rows,
        'total': total,
    }


def add_dns_domain_record():
    """
    添加dns记录
    :return:
    """
    dns_id = request.json['dns_id']
    issue_certificate_id = request.json['issue_certificate_id']

    dns_row = DnsModel.get_by_id(dns_id)

    # 获取验证方式
    challenge_list = issue_certificate_service.get_certificate_challenges(issue_certificate_id)

    for challenge_row in challenge_list:
        challenge_json = challenge_row['challenge'].to_json()
        if challenge_json['type'] == ChallengeType.DNS01:

            if challenge_row['sub_domain'] and challenge_row['sub_domain'] != 'www':
                record_key = '_acme-challenge.' + challenge_row['sub_domain']
            else:
                record_key = '_acme-challenge'

            aliyun_domain_api.add_domain_record(
                access_key_id=dns_row.access_key,
                access_key_secret=dns_row.secret_key,
                domain_name=challenge_row['domain'],
                record_type=RecordTypeEnum.TXT,
                record_key=record_key,
                record_value=challenge_row['validation']
            )
