# -*- coding: utf-8 -*-
"""
@File    : notify_service.py
@Date    : 2022-10-30
@Author  : Peng Shiyu
"""
import json
import traceback
from datetime import datetime, timedelta
from typing import List, Optional, Dict

import requests

from playhouse.shortcuts import model_to_dict

from domain_admin.enums.event_enum import EventEnum
from domain_admin.enums.notify_type_enum import NotifyTypeEnum
from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import domain_service, render_service, email_service
from domain_admin.utils.open_api import feishu_api, work_weixin_api, ding_talk_api
from domain_admin.utils.flask_ext.app_exception import AppException
from jinja2 import Template

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


def get_notify_config(event_id: int):
    """
    获取通知配置
    :param event_id:
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


def get_notify_email_list_of_user(user_id) -> Optional[List[str]]:
    """
    获取通知配置 - 邮箱列表
    :param user_id:
    :return:
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


def notify_all_event() -> int:
    """
    触发所有通知事件
    :return: 成功数量
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


def notify_user_about_some_event(notify_row: NotifyModel):
    """
    由于某个事件触发，通知用户
    :param notify_row:
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


def notify_user_about_cert_expired(notify_row: NotifyModel):
    """
    证书过期事件触发
    :param notify_row:
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=notify_row.expire_days)

    rows = DomainModel.select().where(
        DomainModel.user_id == notify_row.user_id,
        DomainModel.is_monitor == True,
        DomainModel.expire_time <= notify_expire_time
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


def notify_user_about_domain_expired(notify_row: NotifyModel):
    """
    域名过期事件触发
    :param notify_row:
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=notify_row.expire_days)

    rows = DomainInfoModel.select().where(
        DomainInfoModel.user_id == notify_row.user_id,
        DomainInfoModel.is_expire_monitor == True,
        DomainInfoModel.domain_expire_time <= notify_expire_time
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


def notify_user(notify_row: NotifyModel, rows: List):
    """
    通知用户
    :param notify_row:
    :param rows:
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
        notify_row: NotifyModel,
        data: Dict):
    """
    通过 webhook 方式通知用户
    :param notify_row:
    :param data:
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
        template: str,
        subject: str,
        data: Dict,
        email_list: List[str],
):
    """
    通过邮件通知用户证书到期
    :param template:
    :param subject:
    :param data:
    :param email_list:
    :return:
    """
    if not email_list or len(email_list) == 0:
        logger.warn("email_list is empty")
        return

    content = render_service.render_template(
        template=template,
        data=data
    )

    email_service.send_email(
        subject=subject,
        content=content,
        to_addresses=email_list,
        content_type='html'
    )


def notify_user_by_work_weixin(notify_row: NotifyModel):
    """
    发送企业微信消息
    :param notify_row:
    :return:
    """
    token = work_weixin_api.get_access_token(notify_row.work_weixin_corpid, notify_row.work_weixin_corpsecret)
    logger.info('work weixin token %s', token)
    res = work_weixin_api.send_message(token['access_token'], json.loads(notify_row.work_weixin_body))
    return res


def notify_user_by_ding_talk(notify_row: NotifyModel):
    """
    发送钉钉消息
    :param notify_row:
    :return:
    """
    token = ding_talk_api.get_access_token(notify_row.ding_talk_appkey, notify_row.ding_talk_appsecret)
    logger.info('ding talk token %s', token)
    res = ding_talk_api.send_message(token['access_token'], json.loads(notify_row.ding_talk_body))
    return res


def notify_user_by_feishu(notify_row: NotifyModel):
    """
    发送飞书消息
    :param notify_row:
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
