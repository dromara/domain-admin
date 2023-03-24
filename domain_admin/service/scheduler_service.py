# -*- coding: utf-8 -*-
import logging
import warnings
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler
from pytz_deprecation_shim import PytzUsageWarning

from domain_admin.service import system_service, domain_service
from domain_admin.service.file_service import resolve_log_file

warnings.filterwarnings(action="ignore", category=PytzUsageWarning)

apscheduler_logger = logging.getLogger('apscheduler')

# apscheduler_logger.addHandler(logging.FileHandler(resolve_log_file("apscheduler.log")))

# 单个日志文件最大为1M
handler = RotatingFileHandler(resolve_log_file("apscheduler.log"), maxBytes=1024 * 1024 * 1, encoding='utf-8')
apscheduler_logger.addHandler(handler)

apscheduler_logger.setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()


def init_scheduler():
    config = system_service.get_system_config()
    scheduler_cron = config.get('scheduler_cron')

    if not scheduler_cron:
        return

    update_job(scheduler_cron)

    scheduler.start()


def update_job(cron_exp):
    scheduler.remove_all_jobs()

    # cron 定时任务
    minute, hour, day, month, day_of_week = cron_exp.split(' ')

    scheduler.add_job(
        func=domain_service.update_and_check_all_domain_cert,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week
    )
