# -*- coding: utf-8 -*-
"""
database.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.log import logger
from domain_admin.model import base_model, domain_icp_model, tag_model, certificate_model, deploy_cert_model
from domain_admin.model import (
    address_model,
    log_operation_model,
    group_user_model,
    log_async_task_model,
    issue_certificate_model,
    host_model,
    monitor_model,
    log_monitor_model,
    domain_info_model,
    domain_model,
    group_model,
    log_scheduler_model,
    notify_model,
    system_model,
    user_model,
    version_model,
)

# 需要查询初始数据操作的表放前面
tables = [
    (system_model.SystemModel, system_model.init_table_data),
    (version_model.VersionModel, None),
    (user_model.UserModel, user_model.init_table_data),
    (log_scheduler_model.LogSchedulerModel, None),
    (group_model.GroupModel, None),
    (domain_model.DomainModel, None),
    (notify_model.NotifyModel, None),
    (address_model.AddressModel, None),
    (domain_info_model.DomainInfoModel, None),
    (log_operation_model.LogOperationModel, None),
    (group_user_model.GroupUserModel, None),
    (log_async_task_model.AsyncTaskModel, None),
    (issue_certificate_model.IssueCertificateModel, None),
    (host_model.HostModel, None),
    (log_monitor_model.LogMonitorModel, None),
    (monitor_model.MonitorModel, None),
    (domain_icp_model.DomainIcpModel, None),
    (tag_model.TagModel, None),
    (certificate_model.CertificateModel, None),
    (deploy_cert_model.DeployCertModel, None),
]


def init_database():
    """
    初始化数据表
    :return:
    """
    base_model.db.connect()

    db_tables = base_model.db.get_tables()

    for model, init_func in tables:
        # if not model.table_exists():
        if model._meta.table_name not in db_tables:
            logger.info('create table: %s', model._meta.table_name)
            model.create_table()

            if init_func:
                init_func()

    base_model.db.close()
