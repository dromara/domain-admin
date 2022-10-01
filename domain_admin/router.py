# -*- coding: utf-8 -*-
"""
路由配置
"""
from domain_admin.api import cert_api
from domain_admin.api import domain_api
from domain_admin.api import group_api
from domain_admin.api import auth_api

routes = {
    "/api/getCertInformation": cert_api.get_cert_information,

    # 登录注册
    "/api/login": auth_api.login,
    "/api/register": auth_api.register,

    # 域名
    "/api/addDomain": domain_api.add_domain,
    "/api/updateDomainById": domain_api.update_domain_by_id,
    "/api/deleteDomainById": domain_api.delete_domain_by_id,
    "/api/getDomainList": domain_api.get_domain_list,
    "/api/getDomainById": domain_api.get_domain_by_id,
    "/api/updateDomainCertInfoById": domain_api.update_domain_cert_info_by_id,
    "/api/updateAllDomainCertInfo": domain_api.update_all_domain_cert_info,
    "/api/updateAllDomainCertInfoOfUser": domain_api.update_all_domain_cert_info_of_user,
    "/api/sendDomainInfoListEmail": domain_api.send_domain_info_list_email,
    "/api/checkDomainCert": domain_api.check_domain_cert,
    "/api/importDomainFromFile": domain_api.import_domain_from_file,

    "/api/addGroup": group_api.add_group,
    "/api/updateGroupById": group_api.update_group_by_id,
    "/api/deleteGroupById": group_api.delete_group_by_id,
    "/api/getGroupList": group_api.get_group_list,
    "/api/getGroupById": group_api.get_group_by_id,

}
