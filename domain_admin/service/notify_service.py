# -*- coding: utf-8 -*-
"""
@File    : notify_service.py
@Date    : 2022-10-30
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
import traceback
from datetime import datetime, timedelta

import requests
from jinja2 import Template
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.enums.event_enum import EventEnum
from domain_admin.enums.notify_type_enum import NotifyTypeEnum
from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import domain_service, render_service, system_service
from domain_admin.utils import email_util
from domain_admin.utils.flask_ext.app_exception import AppException
from domain_admin.utils.open_api import feishu_api, work_weixin_api, ding_talk_api

# 通知参数配置
NOTIFY_CONFIGS = [
    {
        'event_id': EventEnum.SSL_CERT_EXPIRE,
        'email_template': 'cert-email.html',
        'email_subject': '[Domain Admin]证书过期提醒',
    },
    {
        'event_id': EventEnum.DOMAIN_EXPIRE,
        'email_template': 'domain-email.html',
        'email_subject': '[Domain Admin]域名过期提醒',
    }
]


def get_notify_config(event_id):
    """
    获取通知配置
    :param event_id: int
    :return:
    """
    for config in NOTIFY_CONFIGS:
        if config['event_id'] == event_id:
            return config


def get_notify_row_value(user_id, type_id):
    """
    获取通知配置
    :param user_id:
    :param type_id:
    :return:
    """
    notify_row = NotifyModel.select().where(
        NotifyModel.user_id == user_id,
        NotifyModel.type_id == type_id
    ).get_or_none()

    if not notify_row:
        return None

    if not notify_row.value:
        return None

    return notify_row.value


def get_notify_email_list_of_user(user_id):
    """
    获取通知配置 - 邮箱列表
    :param user_id:
    :return: Optional[List[str]]
    """
    notify_row_value = get_notify_row_value(user_id, NotifyTypeEnum.Email)

    if not notify_row_value:
        return None

    email_list = notify_row_value.get('email_list')

    if not email_list:
        return None

    return email_list


def get_notify_webhook_row_of_user(user_id):
    """
    获取通知配置 - webhook
    :param user_id:
    :return:
    """
    return get_notify_row_value(user_id, NotifyTypeEnum.WebHook)


def notify_webhook_of_user(user_id):
    """
    通过 webhook 方式通知用户
    :param user_id:
    :return:
    """
    notify_webhook_row = get_notify_webhook_row_of_user(user_id)

    if not notify_webhook_row:
        raise AppException('webhook未设置')

    method = notify_webhook_row.get('method')
    url = notify_webhook_row.get('url')
    headers = notify_webhook_row.get('headers')
    body = notify_webhook_row.get('body')

    if not url:
        raise AppException('url未设置')

    # 支持模板变量
    template = Template(body)
    body_render = template.render(get_template_data(user_id))

    res = requests.request(method=method, url=url, headers=headers, data=body_render.encode('utf-8'))
    res.encoding = res.apparent_encoding

    return res.text


def get_template_data(user_id):
    # 两种参数形式
    domain_list = domain_service.get_domain_info_list(user_id)
    return {
        'domain_list': domain_list
    }


def notify_all_event():
    """
    触发所有通知事件
    :return: int 成功数量
    """
    rows = NotifyModel.select().where(
        NotifyModel.status == True
    )

    success = 0
    for row in rows:
        try:
            notify_user_about_some_event(row)
        except:
            logger.error(traceback.format_exc())

        success = success + 1

    return success


def notify_user_about_some_event(notify_row):
    """
    由于某个事件触发，通知用户
    :param notify_row: NotifyModel
    :return:
    """
    if notify_row.event_id == EventEnum.SSL_CERT_EXPIRE:
        # ssl证书
        return notify_user_about_cert_expired(notify_row)
    elif notify_row.event_id == EventEnum.DOMAIN_EXPIRE:
        # 域名过期
        return notify_user_about_domain_expired(notify_row)
    else:
        logger.warn("notify_row event_id not support: %s", notify_row.event_id)


def notify_user_about_cert_expired(notify_row):
    """
    证书过期事件触发
    :param notify_row: NotifyModel
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=notify_row.expire_days)

    # 所在分组
    group_user_rows = GroupUserModel.select().where(
        GroupUserModel.user_id == notify_row.user_id
    )

    group_user_list = list(group_user_rows)
    user_group_ids = [row.group_id for row in group_user_list]

    # 注意null的情况
    query = DomainModel.select().where(
        DomainModel.is_monitor == True
    )

    # 分组
    if user_group_ids:
        query = query.where(
            (DomainModel.user_id == notify_row.user_id)
            | (DomainModel.group_id.in_(user_group_ids))
        )
    else:
        query = query.where(
            DomainModel.user_id == notify_row.user_id,
        )

    rows = query.where(
        (DomainModel.expire_time <= notify_expire_time)
        | (DomainModel.expire_time.is_null(True))
    ).order_by(
        DomainModel.expire_time.asc(),
        DomainModel.id.desc()
    )

    lst = [model_to_dict(
        model=row,
        extra_attrs=[
            'start_date',
            'expire_date',
            'real_time_expire_days',
        ]
    ) for row in rows]

    for row in lst:
        row['expire_days'] = row['real_time_expire_days']

    if len(lst) > 0:
        return notify_user(notify_row, lst)


def notify_user_about_domain_expired(notify_row):
    """
    域名过期事件触发
    :param notify_row: NotifyModel
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=notify_row.expire_days)

    # 所在分组
    group_user_rows = GroupUserModel.select().where(
        GroupUserModel.user_id == notify_row.user_id
    )

    group_user_list = list(group_user_rows)
    user_group_ids = [row.group_id for row in group_user_list]

    # 注意null的情况
    query = DomainInfoModel.select().where(
        DomainInfoModel.is_expire_monitor == True
    )

    if user_group_ids:
        query = query.where(
            (DomainInfoModel.user_id == notify_row.user_id)
            | (DomainInfoModel.group_id.in_(user_group_ids))
        )
    else:
        query = query.where(
            DomainInfoModel.user_id == notify_row.user_id,
        )

    rows = query.where(
        (DomainInfoModel.domain_expire_time <= notify_expire_time)
        | (DomainInfoModel.domain_expire_time.is_null(True))
    ).order_by(
        DomainInfoModel.domain_expire_time.asc(),
        DomainInfoModel.id.desc()
    )

    lst = [model_to_dict(
        model=row,
        extra_attrs=[
            'domain_start_date',
            'domain_expire_date',
            'real_domain_expire_days',
        ]
    ) for row in rows]

    for row in lst:
        row['start_date'] = row['domain_start_date']
        row['expire_date'] = row['domain_expire_date']
        row['expire_days'] = row['real_domain_expire_days']

    if len(lst) > 0:
        return notify_user(notify_row, lst)


def notify_user(notify_row, rows):
    """
    通知用户
    :param notify_row: NotifyModel
    :param rows: List
    :return:
    """
    # 通知用户
    if notify_row.type_id == NotifyTypeEnum.Email:
        notify_config = get_notify_config(notify_row.event_id)

        return notify_user_by_email(
            template=notify_config['email_template'],
            subject=notify_config['email_subject'],
            data={'list': rows},
            email_list=notify_row.email_list
        )
    elif notify_row.type_id == NotifyTypeEnum.WebHook:
        return notify_user_by_webhook(
            notify_row=notify_row,
            data={
                'list': rows,
                'domain_list': rows  # 兼容旧版本
            })
    elif notify_row.type_id == NotifyTypeEnum.WORK_WEIXIN:
        return notify_user_by_work_weixin(notify_row=notify_row)

    elif notify_row.type_id == NotifyTypeEnum.DING_TALK:
        return notify_user_by_ding_talk(notify_row=notify_row)

    elif notify_row.type_id == NotifyTypeEnum.FEISHU:
        return notify_user_by_feishu(notify_row=notify_row)

    else:
        logger.warn("type not support")


def notify_user_by_webhook(
        notify_row,
        data):
    """
    通过 webhook 方式通知用户
    :param notify_row: NotifyModel
    :param data: Dict
    :return:
    """

    if not notify_row.webhook_url:
        logger.warn("webhook url未设置")
        return

    # 支持模板变量
    template = Template(notify_row.webhook_body)
    body_render = template.render(data)

    logger.info(body_render)

    res = requests.request(
        method=notify_row.webhook_method,
        url=notify_row.webhook_url,
        headers=notify_row.webhook_headers,
        data=body_render.encode('utf-8'))

    res.encoding = res.apparent_encoding
    logger.info(res.text)
    return res.text


def notify_user_by_email(
        template,
        subject,
        data,
        email_list,
):
    """
    通过邮件通知用户证书到期
    :param template: str
    :param subject: str
    :param data: Dict
    :param email_list: List[str]
    :return:
    """
    if not email_list or len(email_list) == 0:
        logger.warn("email_list is empty")
        return

    content = render_service.render_template(
        template=template,
        data=data
    )

    config = system_service.get_system_config()

    email_util.send_email(
        mail_host=config[ConfigKeyEnum.MAIL_HOST],
        mail_port=int(config[ConfigKeyEnum.MAIL_PORT]),
        mail_alias=config[ConfigKeyEnum.MAIL_ALIAS],
        subject=subject,
        content=content,
        to_addresses=email_list,
        mail_username=config[ConfigKeyEnum.MAIL_USERNAME],
        mail_password=config[ConfigKeyEnum.MAIL_PASSWORD],
        content_type='html'
    )


def notify_user_by_work_weixin(notify_row):
    """
    发送企业微信消息
    :param notify_row: NotifyModel
    :return:
    """
    token = work_weixin_api.get_access_token(notify_row.work_weixin_corpid, notify_row.work_weixin_corpsecret)
    logger.info('work weixin token %s', token)
    res = work_weixin_api.send_message(token['access_token'], json.loads(notify_row.work_weixin_body))
    return res


def notify_user_by_ding_talk(notify_row):
    """
    发送钉钉消息
    :param notify_row: NotifyModel
    :return:
    """
    token = ding_talk_api.get_access_token(notify_row.ding_talk_appkey, notify_row.ding_talk_appsecret)
    logger.info('ding talk token %s', token)
    res = ding_talk_api.send_message(token['access_token'], json.loads(notify_row.ding_talk_body))
    return res


def notify_user_by_feishu(notify_row):
    """
    发送飞书消息
    :param notify_row: NotifyModel
    :return:
    """
    token = feishu_api.get_access_token(notify_row.feishu_app_id, notify_row.feishu_app_secret)
    logger.info('feishu token %s', token)

    res = feishu_api.send_message(
        access_token=token['tenant_access_token'],
        body=json.loads(notify_row.feishu_body),
        params=notify_row.feishu_params
    )
    return res
