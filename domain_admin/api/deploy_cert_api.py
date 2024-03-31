# -*- coding: utf-8 -*-
"""
@File    : deploy_cert_api.py
@Date    : 2024-03-31
"""

from flask import g, request

from domain_admin.model.deploy_cert_model import DeployCertModel
from domain_admin.model.host_model import HostModel
from domain_admin.service import deploy_cert_service


def get_deploy_list_by_cert_id():
    """
    获取列表
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    cert_id = request.json['cert_id']
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = DeployCertModel.select().where(
        DeployCertModel.cert_id == cert_id,
    )

    total = query.count()
    lst = []

    if total > 0:
        rows = query.order_by(
            DeployCertModel.id,
        ).paginate(page, size)

        lst = [row.to_dict() for row in rows]

        # deploy_host
        deploy_cert_service.load_cert_deploy_host(lst)

    return {
        "list": lst,
        "total": total
    }


def add_deploy_cert():
    """
    添加详情
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    cert_id = request.json['cert_id']
    deploy_host_id = request.json['deploy_host_id']
    deploy_key_file = request.json['deploy_key_file']
    deploy_fullchain_file = request.json['deploy_fullchain_file']
    deploy_reloadcmd = request.json['deploy_reloadcmd']

    data = {
        'user_id': current_user_id,
        'cert_id': cert_id,
        'deploy_host_id': deploy_host_id,
        'deploy_key_file': deploy_key_file,
        'deploy_fullchain_file': deploy_fullchain_file,
        'deploy_reloadcmd': deploy_reloadcmd,
    }

    DeployCertModel.create(**data)


def update_deploy_cert_by_id():
    """
    更新详情
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    deploy_cert_id = request.json['deploy_cert_id']
    deploy_host_id = request.json['deploy_host_id']
    deploy_key_file = request.json['deploy_key_file']
    deploy_fullchain_file = request.json['deploy_fullchain_file']
    deploy_reloadcmd = request.json['deploy_reloadcmd']

    data = {
        'deploy_host_id': deploy_host_id,
        'deploy_key_file': deploy_key_file,
        'deploy_fullchain_file': deploy_fullchain_file,
        'deploy_reloadcmd': deploy_reloadcmd,
    }

    DeployCertModel.update(data).where(
        DeployCertModel.id == deploy_cert_id
    ).execute()


def delete_by_deploy_cert_id():
    """
    删除详情
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    deploy_cert_id = request.json['deploy_cert_id']

    DeployCertModel.delete_by_id(deploy_cert_id)


def delete_by_deploy_cert_ids():
    """
    批量删除详情
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    deploy_cert_ids = request.json['deploy_cert_ids']

    DeployCertModel.delete().where(
        DeployCertModel.id.in_(deploy_cert_ids)
    ).execute()


def get_deploy_cert_by_id():
    """
    获取详情
    :return:
    @since v1.6.20
    """

    current_user_id = g.user_id

    deploy_cert_id = request.json['deploy_cert_id']

    deploy_cert_row = DeployCertModel.get_by_id(deploy_cert_id)
    deploy_cert_dict = deploy_cert_row.to_dict()

    deploy_cert_dict['deploy_host'] = HostModel.get_by_id(deploy_cert_dict['deploy_host_id'])

    return deploy_cert_dict


def handle_deploy_cert():
    """
    部署证书
    @since v1.6.20
    :return:
    """
    deploy_cert_id = request.json['deploy_cert_id']
    err = deploy_cert_service.handle_deploy_cert(deploy_cert_id)
    if err:
        raise err
