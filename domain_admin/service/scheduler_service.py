# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import logging
import traceback
import warnings
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler

from domain_admin.config import APP_MODE
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.log import logger
from domain_admin.model.base_model import db
from domain_admin.model.log_scheduler_model import LogSchedulerModel
from domain_admin.service import system_service, domain_service, domain_info_service, notify_service, \
    issue_certificate_service
from domain_admin.service.file_service import resolve_log_file
from domain_admin.utils import datetime_util

warnings.filterwarnings(action="ignore")

apscheduler_logger = logging.getLogger('apscheduler')

# 单个日志文件最大为1M
handler = RotatingFileHandler(resolve_log_file("apscheduler.log"), maxBytes=1024 * 1024 * 1, encoding='utf-8')

# 设置日志格式
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

apscheduler_logger.addHandler(handler)

apscheduler_logger.setLevel(logging.ERROR)

# development
if APP_MODE == 'development':
    apscheduler_logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    apscheduler_logger.addHandler(stream_handler)


JOB_DEFAULTS = {
    # seconds after the designated runtime that the job is still allowed to be run
    # (or ``None`` to allow the job to run no matter how late it is)
    'misfire_grace_time': None,  # 默认值 1

    # run once instead of many times if the scheduler determines that the
    # job should be run more than once in succession
    'coalesce': True,  # 默认值 True

    # maximum number of concurrently running instances allowed for this job
    'max_instances': 1  # 默认值 1
}

scheduler = BackgroundScheduler(job_defaults=JOB_DEFAULTS)

# 任务列表
TASK_LIST = [
    # 更新证书信息
    domain_service.update_all_domain_cert_info,

    # 更新域名信息
    domain_info_service.update_all_domain_info,

    # 更新所有SSL证书
    issue_certificate_service.renew_all_certificate,

    # 触发通知
    notify_service.notify_all_event,
]


def crontab_compatible_weekday(expr):
    """
    :param expr:
    :return:

    bugfix: 0-6表示周一到周日，改为周日到周六，并支持7为周日
    day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    ref: https://github.com/agronholm/apscheduler/issues/286#issuecomment-449273964
    """
    if expr == "*":
        return expr

    mapping = {
        "0": "sun",
        "1": "mon",
        "2": "tue",
        "3": "wed",
        "4": "thu",
        "5": "fri",
        "6": "sat",
        "7": "sun"
    }

    return "".join(map(lambda x: mapping.get(x, x), expr))


def init_scheduler():
    scheduler_cron = system_service.get_config(ConfigKeyEnum.SCHEDULER_CRON)

    if not scheduler_cron:
        return

    update_job(scheduler_cron)

    scheduler.start()


def update_job(cron_exp):
    scheduler.remove_all_jobs()

    # cron 定时任务
    # Bugfix: 用户输入的cron表达式有多余的空格
    minute, hour, day, month, day_of_week = cron_exp.split()

    scheduler.add_job(
        func=run_task,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=crontab_compatible_weekday(day_of_week)
    )


# fix: OperationalError: (2006, ‘MySQL server has gone away’)
# see: http://docs.peewee-orm.com/en/latest/peewee/database.html#context-managers
@db.connection_context()
def run_task():
    """
    定时任务
    :return:
    """
    # 开始执行
    log_row = LogSchedulerModel.create()

    message = '执行成功'
    status = True

    for func in TASK_LIST:
        try:
            func()
        except Exception as e:
            logger.error(traceback.format_exc())
            status = False
            message = str(e)

    # 执行完毕
    LogSchedulerModel.update({
        'status': status,
        'error_message': message,
        'update_time': datetime_util.get_datetime(),
    }).where(
        LogSchedulerModel.id == log_row.id
    ).execute()
