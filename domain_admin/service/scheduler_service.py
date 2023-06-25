# -*- coding: utf-8 -*-
import logging
import warnings
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler

from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.model.log_scheduler_model import LogSchedulerModel
from domain_admin.service import system_service, domain_service, domain_info_service, notify_service
from domain_admin.service.file_service import resolve_log_file
from domain_admin.utils import datetime_util

warnings.filterwarnings(action="ignore")

apscheduler_logger = logging.getLogger('apscheduler')

# 单个日志文件最大为1M
handler = RotatingFileHandler(resolve_log_file("apscheduler.log"), maxBytes=1024 * 1024 * 1, encoding='utf-8')
apscheduler_logger.addHandler(handler)

apscheduler_logger.setLevel(logging.DEBUG)

JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1
}

scheduler = BackgroundScheduler(job_defaults=JOB_DEFAULTS)


def init_scheduler():
    scheduler_cron = system_service.get_config(ConfigKeyEnum.SCHEDULER_CRON)

    if not scheduler_cron:
        return

    update_job(scheduler_cron)

    scheduler.start()


def update_job(cron_exp):
    scheduler.remove_all_jobs()

    # cron 定时任务
    minute, hour, day, month, day_of_week = cron_exp.split(' ')

    scheduler.add_job(
        func=task,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )


def task():
    """
    定时任务
    :return:
    """
    # 开始执行
    log_row = LogSchedulerModel.create()

    # 更新证书信息
    domain_service.update_all_domain_cert_info()

    # 更新域名信息
    domain_info_service.update_all_domain_info()

    # 触发通知
    success = notify_service.notify_all_event()

    # 执行完毕
    LogSchedulerModel.update({
        'status': True,
        'error_message': f'成功发送: {success}',
        'update_time': datetime_util.get_datetime(),
    }).where(
        LogSchedulerModel.id == log_row.id
    ).execute()
