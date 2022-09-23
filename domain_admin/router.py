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
    get_domain_by_id
)

routes = {
    "/api/addDomain": add_domain,
    "/api/updateDomainById": update_domain_by_id,
    "/api/deleteDomainById": delete_domain_by_id,
    "/api/getDomainList": get_domain_list,
    "/api/getDomainById": get_domain_by_id,
    "/api/getCertInformation": get_cert_information,
}
