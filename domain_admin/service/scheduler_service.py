# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from pytz_deprecation_shim import PytzUsageWarning

from domain_admin.api import domain_api
import warnings

warnings.filterwarnings(action="ignore", category=PytzUsageWarning)


def start_scheduler(cron_exp):
    """
    定时检测域名到期情况
    :param cron_exp:
    :return:
    """

    scheduler = BackgroundScheduler()

    # cron 定时任务
    minute, hour, day, month, day_of_week = cron_exp.split(' ')

    scheduler.add_job(
        func=domain_api.check_domain_cert,
        trigger='cron',
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week)

    scheduler.start()
