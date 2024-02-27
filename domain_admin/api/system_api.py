# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime, timedelta

from flask import request, g

from domain_admin import version
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.enums.monitor_status_enum import MonitorStatusEnum
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.model.system_model import SystemModel
from domain_admin.service import scheduler_service
from domain_admin.service.scheduler_service import scheduler_main
from domain_admin.utils import datetime_util, email_util


def update_system_config():
    """
    更新单个配置
    :return:
    """
    allow_keys = [
        ConfigKeyEnum.MAIL_HOST,
        ConfigKeyEnum.MAIL_PORT,
        ConfigKeyEnum.MAIL_ALIAS,
        ConfigKeyEnum.MAIL_USERNAME,
        ConfigKeyEnum.MAIL_PASSWORD,
    ]

    for key in allow_keys:
        value = request.json[key]

        SystemModel.update(
            {
                'value': value,
                'update_time': datetime_util.get_datetime()
            }
        ).where(
            SystemModel.key == key
        ).execute()


def get_all_system_config():
    """
    获取所有配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.MAIL_HOST,
            ConfigKeyEnum.MAIL_PORT,
            ConfigKeyEnum.MAIL_ALIAS,
            ConfigKeyEnum.MAIL_USERNAME,
            ConfigKeyEnum.MAIL_PASSWORD,
        ])
    )

    return {item.key: item.value for item in lst}


def get_system_env_config():
    """
    获取配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.PROMETHEUS_KEY
        ])
    )

    return {item.key: item.value for item in lst}


def get_cron_config():
    """
    获取配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.SCHEDULER_CRON
        ])
    )

    return {item.key: item.value for item in lst}


def update_cron_config():
    """
    更新cron配置
    :return:
    """
    scheduler_cron = request.json['scheduler_cron']

    SystemModel.update(
        {
            'value': scheduler_cron,
            'update_time': datetime_util.get_datetime()
        }
    ).where(
        SystemModel.key == ConfigKeyEnum.SCHEDULER_CRON
    ).execute()

    # 更新定时
    scheduler_service.update_job(scheduler_cron)


def get_system_version():
    """
    获取当前应用版本号
    :return:
    """
    return {
        'version': version.VERSION
    }


def get_system_data():
    current_user_id = g.user_id
    now = datetime.now()
    now_add_7_day = datetime.now() + timedelta(days=7)
    ssl_cert_count = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    ).count()

    ssl_cert_expire_count = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    ).where(
        (DomainModel.expire_time <= now) |
        (DomainModel.expire_time.is_null(True))
    ).count()

    ssl_cert_will_expire_count = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    ).where(
        (DomainModel.expire_time > now) &
        (DomainModel.expire_time <= now_add_7_day)
    ).count()

    domain_count = DomainInfoModel.select().where(
        DomainInfoModel.user_id == current_user_id
    ).count()

    domain_expire_count = DomainInfoModel.select().where(
        DomainInfoModel.user_id == current_user_id
    ).where(
        (DomainInfoModel.domain_expire_time <= now) |
        (DomainInfoModel.domain_expire_time.is_null(True))
    ).count()

    domain_will_expire_count = DomainInfoModel.select().where(
        DomainInfoModel.user_id == current_user_id
    ).where(
        (DomainInfoModel.domain_expire_time > now) &
        (DomainInfoModel.domain_expire_time < now_add_7_day)
    ).count()

    monitor_count = MonitorModel.select().where(
        MonitorModel.user_id == current_user_id
    ).count()

    monitor_error_count = MonitorModel.select().where(
        MonitorModel.user_id == current_user_id,
        MonitorModel.status == MonitorStatusEnum.ERROR,
    ).count()

    return [
        {
            'title': '证书数量',
            'key': 'ssl_cert_count',
            'count': ssl_cert_count,
            'path': '/cert/list',
        },
        {
            'title': '即将过期证书',
            'key': 'ssl_cert_will_expire_count',
            'count': ssl_cert_will_expire_count,
            'path': '/cert/list',
        },
        {
            'title': '过期证书',
            'key': 'ssl_cert_expire_count',
            'count': ssl_cert_expire_count,
            'path': '/cert/list'
        },
        {
            'title': '域名数量',
            'key': 'domain_count',
            'count': domain_count,
            'path': '/domain/list'
        },
        {
            'title': '即将过期域名',
            'key': 'domain_will_expire_count',
            'count': domain_will_expire_count,
            'path': '/domain/list',
        },
        {
            'title': '过期域名',
            'key': 'domain_expire_count',
            'count': domain_expire_count,
            'path': '/domain/list'
        },
        {
            'title': '监控数量',
            'count': monitor_count,
            'key': 'monitor_count',
            'path': '/monitor/list'
        },

        {
            'title': '监控异常',
            'key': 'monitor_error_count',
            'count': monitor_error_count,
            'path': '/monitor/list'
        }
    ]


def get_monitor_task_next_run_time():
    return {
        'next_run_time': scheduler_main.get_monitor_task_next_run_time()
    }


def send_test_email():
    """
    发送测试邮件
    :return:
    """
    mail_host = request.json['mail_host']
    mail_port = request.json['mail_port']
    mail_alias = request.json['mail_alias']
    mail_username = request.json['mail_username']
    mail_password = request.json['mail_password']

    subject = request.json['subject']
    content = request.json['content']
    email_list = request.json['email_list']

    email_util.send_email(
        mail_host=mail_host,
        mail_port=int(mail_port),
        mail_alias=mail_alias,
        subject=subject,
        content=content,
        to_addresses=email_list,
        mail_username=mail_username,
        mail_password=mail_password,
        content_type='plain'
    )
