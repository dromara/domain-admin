# -*- coding: utf-8 -*-
"""
路由配置
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.api import (
    cert_api, ip_api, notify_api,
    whois_api, address_api,
    domain_info_api, prometheus_api,
    log_operation_api, group_user_api,
    log_async_task_api)
from domain_admin.api import domain_api
from domain_admin.api import group_api
from domain_admin.api import auth_api
from domain_admin.api import system_api
from domain_admin.api import user_api
from domain_admin.api import log_scheduler_api

routes = {
    # 域名信息
    "/api/getCertInformation": cert_api.get_cert_information,

    # 登录注册
    "/api/login": auth_api.login,
    "/api/register": auth_api.register,

    # 域名（SSL证书）
    "/api/addDomain": domain_api.add_domain,
    "/api/updateDomainById": domain_api.update_domain_by_id,
    "/api/updateDomainFieldById": domain_api.update_domain_field_by_id,
    "/api/updateDomainExpireMonitorById": domain_api.update_domain_expire_monitor_by_id,
    "/api/deleteDomainById": domain_api.delete_domain_by_id,
    "/api/deleteDomainByIds": domain_api.delete_domain_by_ids,
    "/api/getDomainList": domain_api.get_domain_list,
    "/api/getDomainById": domain_api.get_domain_by_id,
    "/api/updateDomainCertInfoById": domain_api.update_domain_row_info_by_id,
    "/api/updateDomainRowInfoById": domain_api.update_domain_row_info_by_id,
    "/api/updateAllDomainCertInfo": domain_api.update_all_domain_cert_info,
    "/api/getDomainGroupFilter": domain_api.get_domain_group_filter,

    # "/api/updateDomainSetting": domain_api.update_domain_setting,

    "/api/updateAllDomainCertInfoOfUser": domain_api.update_all_domain_cert_info_of_user,
    # "/api/sendDomainInfoListEmail": domain_api.send_domain_info_list_email,
    # "/api/checkDomainCert": domain_api.check_domain_cert,
    "/api/importDomainFromFile": domain_api.import_domain_from_file,
    "/api/getAllDomainListOfUser": domain_api.get_all_domain_list_of_user,
    # "/api/getUpdateDomainStatusOfUser": domain_api.get_update_domain_status_of_user,
    # "/api/getCheckDomainStatusOfUser": domain_api.get_check_domain_status_of_user,
    "/api/exportDomainFile": domain_api.export_domain_file,
    '/api/domainRelationGroup': domain_api.domain_relation_group,

    # 分组管理
    "/api/addGroup": group_api.add_group,
    "/api/updateGroupById": group_api.update_group_by_id,
    "/api/deleteGroupById": group_api.delete_group_by_id,
    "/api/deleteGroupByIds": group_api.delete_group_by_ids,
    "/api/getGroupList": group_api.get_group_list,
    "/api/getGroupById": group_api.get_group_by_id,

    # 用户
    '/api/getUserInfo': user_api.get_user_info,
    '/api/updateUserInfo': user_api.update_user_info,
    '/api/updateUserPassword': user_api.update_user_password,

    # 调度日志
    '/api/getLogSchedulerList': log_scheduler_api.get_log_scheduler_list,
    '/api/clearLogSchedulerList': log_scheduler_api.clear_log_scheduler_list,

    # 操作日志
    '/api/getOperationLogList': log_operation_api.get_operation_log_list,
    '/api/clearLogOperationList': log_operation_api.clear_log_operation_list,

    # 系统管理 (管理员权限)
    '/api/getAllSystemConfig': system_api.get_all_system_config,
    '/api/updateSystemConfig': system_api.update_system_config,
    '/api/getSystemEnvConfig': system_api.get_system_env_config,
    '/api/getCronConfig': system_api.get_cron_config,
    '/api/updateCronConfig': system_api.update_cron_config,
    '/api/getSystemVersion': system_api.get_system_version,

    # 用户管理 (管理员权限)
    '/api/getUserList': user_api.get_user_list,
    '/api/addUser': user_api.add_user,
    '/api/updateUserStatus': user_api.update_user_status,
    '/api/deleteUser': user_api.delete_user,
    '/api/resetUserPasswordUser': user_api.reset_user_password,

    # 获取ip信息
    '/api/getIpInfo': ip_api.get_ip_info,

    # 通知方式
    # '/api/getNotifyOfUser': notify_api.get_notify_of_user,
    # '/api/updateNotifyOfUser': notify_api.update_notify_of_user,
    # '/api/testWebhookNotifyOfUser': notify_api.test_webhook_notify_of_user,
    # '/api/testWorkWeixinNotifyOfUser': notify_api.test_work_weixin_notify_of_user,
    # '/api/getTemplateData': notify_api.get_template_data,
    '/api/getNotifyListOfUser': notify_api.get_notify_list_of_user,
    '/api/addNotify': notify_api.add_notify,
    '/api/deleteNotifyById': notify_api.delete_notify_by_id,
    '/api/updateNotifyStatusById': notify_api.update_notify_status_by_id,
    '/api/updateNotifyById': notify_api.update_notify_by_id,
    '/api/getNotifyById': notify_api.get_notify_by_id,
    '/api/handleTestNotifyById': notify_api.handle_test_notify_by_id,
    '/api/handleNotifyByEventId': notify_api.handle_notify_by_event_id,

    # 实验室
    '/api/getWhoisRaw': whois_api.get_whois_raw,

    # 主机地址
    '/api/getAddressListByDomainId': address_api.get_address_list_by_domain_id,
    '/api/addAddress': address_api.add_address,
    '/api/getAddressById': address_api.get_address_by_id,
    '/api/deleteAddressById': address_api.delete_address_by_id,
    '/api/updateAddressById': address_api.update_address_by_id,
    '/api/updateAddressListInfoByDomainId': address_api.update_address_list_info_by_domain_id,
    '/api/updateAddressRowInfoById': address_api.update_address_row_info_by_id,
    '/api/deleteAddressByIds': address_api.delete_address_by_ids,

    # 域名列表
    '/api/getDomainInfoList': domain_info_api.get_domain_info_list,
    '/api/addDomainInfo': domain_info_api.add_domain_info,
    '/api/updateDomainInfoRowById': domain_info_api.update_domain_info_row_by_id,
    '/api/updateDomainInfoOfUser': domain_info_api.update_all_domain_info_of_user,
    '/api/updateDomainInfoFieldById': domain_info_api.update_domain_info_field_by_id,
    '/api/deleteDomainInfoById': domain_info_api.delete_domain_info_by_id,
    '/api/getDomainInfoById': domain_info_api.get_domain_info_by_id,
    '/api/updateDomainInfoById': domain_info_api.update_domain_info_by_id,
    # '/api/checkDomainExpire': domain_info_api.check_domain_expire,
    '/api/deleteDomainInfoByIds': domain_info_api.delete_domain_info_by_ids,
    '/api/importDomainInFromFile': domain_info_api.import_domain_info_from_file,
    '/api/exportDomainInfoFile': domain_info_api.export_domain_info_file,
    '/api/getDomainInfoGroupFilter': domain_info_api.get_domain_info_group_filter,
    '/api/getSubDomainCert': domain_info_api.get_sub_domain_cert,
    '/api/updateDomainICPOfUser': domain_info_api.update_all_domain_icp_of_user,
    '/api/updateDomainRowICP': domain_info_api.update_domain_row_icp,

    # prometheus
    '/metrics': prometheus_api.metrics,

    # 备案查询
    '/api/getICP': domain_info_api.get_icp,

    # 分组权限
    '/api/addGroupUser': group_user_api.add_group_user,
    '/api/updateGroupUserById': group_user_api.update_group_user_by_id,
    '/api/deleteGroupUserById': group_user_api.delete_group_user_by_id,
    '/api/deleteGroupUserByIds': group_user_api.delete_group_user_by_ids,
    '/api/getGroupUserById': group_user_api.get_group_user_by_id,
    '/api/getGroupUserList': group_user_api.get_group_user_list,

    # 异步任务日志
    '/api/getAsyncTaskLogList': log_async_task_api.get_async_task_log_list,
    '/api/clearAsyncTaskLogList': log_async_task_api.clear_async_task_log_list,

}
