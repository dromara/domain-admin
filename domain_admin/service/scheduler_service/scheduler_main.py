# -*- coding: utf-8 -*-
"""
@File    : scheduler_main.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import traceback
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from domain_admin.service.scheduler_service import scheduler_config

from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.log import logger
from domain_admin.model.base_model import db
from domain_admin.model.log_scheduler_model import LogSchedulerModel
from domain_admin.service import system_service, monitor_service
from domain_admin.service.scheduler_service import scheduler_log, scheduler_util
from domain_admin.utils import datetime_util

scheduler = BackgroundScheduler(job_defaults=scheduler_config.JOB_DEFAULTS)


def init_scheduler():
    scheduler_log.init_log()

    scheduler.start()

    # 监测任务
    update_monitor_task(datetime.now())

    # 证书监测任务
    scheduler_cron = system_service.get_config(ConfigKeyEnum.SCHEDULER_CRON)

    if not scheduler_cron:
        return

    update_job(scheduler_cron)


def update_job(cron_exp):
    # scheduler.remove_all_jobs()

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
        day_of_week=scheduler_util.crontab_compatible_weekday(day_of_week),
        id=scheduler_config.TASK_JOB_ID,
        replace_existing=True
    )


def run_one_monitor_task(monitor_row):
    next_run_time = monitor_service.run_monitor_warp(monitor_row)

    # 监测任务
    if next_run_time:
        update_monitor_task(next_run_time)


def update_monitor_task(next_run_time):
    monitor_job = scheduler.get_job(scheduler_config.MONITOR_TASK_JOB_ID)

    # 如果下次运行时间比唤起时间早，就替换唤起时间
    if monitor_job and datetime_util.is_greater_than(next_run_time, monitor_job.next_run_time):
        return

    scheduler.add_job(
        func=run_monitor_task,
        next_run_time=next_run_time,
        id=scheduler_config.MONITOR_TASK_JOB_ID,
        replace_existing=True
    )


def get_monitor_task_next_run_time():
    monitor_task = scheduler.get_job(job_id=scheduler_config.MONITOR_TASK_JOB_ID)

    if monitor_task:
        return monitor_task.next_run_time


def run_monitor_task():
    next_run_time = monitor_service.run_monitor_task()

    if next_run_time:
        update_monitor_task(next_run_time)


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

    for func in scheduler_config.TASK_LIST:
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
