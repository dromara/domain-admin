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
from domain_admin.model.certificate_model import CertificateModel
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import domain_service, render_service, system_service, async_task_service, group_service
from domain_admin.utils import email_util, json_util
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
    },
    {
        'event_id': EventEnum.MONITOR_EXCEPTION,
        'email_template': 'monitor-email.html',
        'email_subject': '[Domain Admin]监控异常提醒',
    },
    {
        'event_id': EventEnum.SSL_CERT_FILE_EXPIRE,
        'email_template': 'cert-email.html',
        'email_subject': '[Domain Admin]托管证书到期提醒',
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
    # fix: TypeError: inner() takes 2 positional arguments but 3 were given
    rows = NotifyModel.select().where(
        NotifyModel.status == True,
        NotifyModel.event_id.in_([
            EventEnum.SSL_CERT_EXPIRE,
            EventEnum.DOMAIN_EXPIRE,
            EventEnum.SSL_CERT_FILE_EXPIRE
        ])
    )

    success = 0
    for row in rows:
        try:
            notify_user_about_some_event(row)
        except:
            logger.error(traceback.format_exc())

        success = success + 1

    return success


def notify_user_about_monitor_exception(monitor_row, error):
    rows = NotifyModel.select().where(
        NotifyModel.status == True,
        NotifyModel.event_id == EventEnum.MONITOR_EXCEPTION
    )

    for row in rows:
        try:
            notify_user(notify_row=row, rows=rows, data={'monitor_row': monitor_row, 'error': str(error)})
        except:
            logger.error(traceback.format_exc())


# @async_task_service.sync_task_decorator("触发通知用户")
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
    elif notify_row.event_id == EventEnum.SSL_CERT_FILE_EXPIRE:
        # 托管证书到期
        return notify_user_about_cert_file_expired(notify_row)
    else:
        raise AppException("notify_row event_id not support: {}".format(notify_row.event_id))


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
    if notify_row.groups:
        query = query.where(
            DomainModel.group_id.in_(notify_row.groups)
        )
    elif user_group_ids:
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
            'update_time_label',
        ]
    ) for row in rows]

    for row in lst:
        row['expire_days'] = row['real_time_expire_days']
        row['comment'] = row['alias']
        row['is_auto_update'] = row['auto_update']
        row['is_expire_monitor'] = row['is_monitor']

    group_service.load_group_name(lst)

    if len(lst) > 0:
        return notify_user(notify_row, lst)


def notify_user_about_cert_file_expired(notify_row):
    """
    托管证书到期
    :param notify_row:
    :return:
    """
    now = datetime.now()

    notify_expire_time = now + timedelta(days=notify_row.expire_days)

    # 注意null的情况
    query = CertificateModel.select()

    rows = query.where(
        (CertificateModel.expire_time <= notify_expire_time)
        | (CertificateModel.expire_time.is_null(True))
    ).order_by(
        CertificateModel.expire_time.asc(),
        CertificateModel.id.desc()
    )

    lst = [row.to_dict() for row in rows]

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

    if notify_row.groups:
        query = query.where(
            DomainInfoModel.group_id.in_(notify_row.groups)
        )
    elif user_group_ids:
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
            'tags',
            'start_date',
            'expire_date',
            'expire_days',
            'tags_str',
            'update_time_label',
        ]
    ) for row in rows]

    for row in lst:
        row['start_time'] = row['domain_start_time']
        row['expire_time'] = row['domain_expire_time']
    #     row['start_date'] = row['domain_start_date']
    #     row['expire_date'] = row['domain_expire_date']
    #     row['expire_days'] = row['real_domain_expire_days']
    group_service.load_group_name(lst)

    if len(lst) > 0:
        return notify_user(notify_row, lst)


def notify_user(notify_row, rows, data=None):
    """
    通知用户
    :param notify_row: NotifyModel
    :param rows: List
    :return:
    """
    logger.debug(json_util.json_dump(rows))

    data = data if data else {}

    # 通知用户
    if notify_row.type_id == NotifyTypeEnum.Email:
        notify_config = get_notify_config(notify_row.event_id)

        if not notify_config:
            raise AppException('邮件通知模板未配置')

        return notify_user_by_email(
            template=notify_config['email_template'],
            subject=notify_config['email_subject'],
            data={**data, 'list': rows},
            email_list=notify_row.email_list
        )
    elif notify_row.type_id == NotifyTypeEnum.WebHook:
        return notify_user_by_webhook(
            notify_row=notify_row,
            data={
                **data,
                'list': rows,
                'domain_list': rows  # 兼容旧版本
            })
    elif notify_row.type_id == NotifyTypeEnum.WORK_WEIXIN:
        return notify_user_by_work_weixin(notify_row=notify_row, data={**data, 'list': rows})

    elif notify_row.type_id == NotifyTypeEnum.DING_TALK:
        return notify_user_by_ding_talk(notify_row=notify_row, data={**data, 'list': rows})

    elif notify_row.type_id == NotifyTypeEnum.FEISHU:
        return notify_user_by_feishu(notify_row=notify_row, data={**data, 'list': rows})

    else:
        logger.warn("type not support")


@async_task_service.sync_task_decorator("触发Webhook通知")
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


@async_task_service.sync_task_decorator("触发邮件通知")
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


@async_task_service.sync_task_decorator("触发企业微信通知")
def notify_user_by_work_weixin(notify_row, data):
    """
    发送企业微信消息
    :param notify_row: NotifyModel
    :return:
    """
    token = work_weixin_api.get_access_token(notify_row.work_weixin_corpid, notify_row.work_weixin_corpsecret)
    logger.info('work weixin token %s', token)

    # 支持模板变量
    template = Template(notify_row.work_weixin_body)
    work_weixin_body = template.render(data)

    res = work_weixin_api.send_message(token['access_token'], json.loads(work_weixin_body))
    return res


@async_task_service.sync_task_decorator("触发钉钉通知")
def notify_user_by_ding_talk(notify_row, data):
    """
    发送钉钉消息
    :param notify_row: NotifyModel
    :return:
    """
    token = ding_talk_api.get_access_token(notify_row.ding_talk_appkey, notify_row.ding_talk_appsecret)
    logger.info('ding talk token %s', token)

    # 支持模板变量
    template = Template(notify_row.ding_talk_body)
    ding_talk_body = template.render(data)

    res = ding_talk_api.send_message(token['access_token'], json.loads(ding_talk_body))
    return res


@async_task_service.sync_task_decorator("触发飞书通知")
def notify_user_by_feishu(notify_row, data):
    """
    发送飞书消息
    :param notify_row: NotifyModel
    :return:
    """
    token = feishu_api.get_access_token(notify_row.feishu_app_id, notify_row.feishu_app_secret)
    logger.info('feishu token %s', token)

    # 支持模板变量
    template = Template(notify_row.feishu_body)
    feishu_body = template.render(data)

    res = feishu_api.send_message(
        access_token=token['tenant_access_token'],
        body=json.loads(feishu_body),
        params=notify_row.feishu_params
    )

    return res
