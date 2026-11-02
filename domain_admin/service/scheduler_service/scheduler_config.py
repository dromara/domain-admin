# -*- coding: utf-8 -*-
"""
@File    : scheduler_config.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.service import domain_service, domain_info_service, notify_service, \
    issue_certificate_service


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


from domain_admin.service import domain_service, domain_info_service, notify_service, \
    issue_certificate_service

from domain_admin.utils import uuid_util

TASK_JOB_ID = uuid_util.get_uuid()

NOTIFY_TASK_JOB_ID = uuid_util.get_uuid()

MONITOR_TASK_JOB_ID = uuid_util.get_uuid()

# 任务列表
TASK_LIST = [
    # 更新证书信息
    domain_service.update_all_domain_cert_info,

    # 更新域名信息
    domain_info_service.update_all_domain_info,

    # 更新所有SSL证书
    issue_certificate_service.renew_all_certificate,
]

# 通知任务列表
# fix: 通知任务从 TASK_LIST 中拆出，单独注册 job。
# 原因是任务列表按顺序串行执行，前面的证书续签一旦卡死（外部 ACME 服务无响应等），
# 后面的通知任务永远无法执行，导致「证书/域名到期不通知」，而手动测试发送却正常。
NOTIFY_TASK_LIST = [
    # 触发通知
    notify_service.notify_all_event,
]
