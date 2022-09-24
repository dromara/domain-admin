# -*- coding: utf-8 -*-
"""
路由配置
"""
from domain_admin.api.cert_api import get_cert_information
from domain_admin.api.domain_api import (
    add_domain,
    update_domain_by_id,
    delete_domain_by_id,
    get_domain_list,
    get_domain_by_id,
    update_domain_cert_info_by_id)
from domain_admin.api.group_api import add_group, get_group_by_id, get_group_list, delete_group_by_id, \
    update_group_by_id

routes = {
    "/api/getCertInformation": get_cert_information,

    "/api/addDomain": add_domain,
    "/api/updateDomainById": update_domain_by_id,
    "/api/deleteDomainById": delete_domain_by_id,
    "/api/getDomainList": get_domain_list,
    "/api/getDomainById": get_domain_by_id,
    "/api/updateDomainCertInfoById": update_domain_cert_info_by_id,

    "/api/addGroup": add_group,
    "/api/updateGroupById": update_group_by_id,
    "/api/deleteGroupById": delete_group_by_id,
    "/api/getGroupList": get_group_list,
    "/api/getGroupById": get_group_by_id,

}
