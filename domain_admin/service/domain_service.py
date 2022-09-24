# -*- coding: utf-8 -*-
import json

from domain_admin.model import DomainModel
from domain_admin.utils.cert_util import get_cert_info
from domain_admin.utils.datetime_util import get_datetime


def update_domain_cert_info(row):
    """
    更新域名的证书信息
    :param row:
    :return:
    """

    connect_status = False

    info = {}

    try:
        info = get_cert_info(row.domain)
        connect_status = True
    except Exception:
        pass

    DomainModel.update(
        start_time=info.get('start_date'),
        expire_time=info.get('expire_date'),
        connect_status=connect_status,
        detail_raw=json.dumps(info, ensure_ascii=False),
        check_time=get_datetime(),
    ).where(
        DomainModel.id == row.id
    ).execute()


if __name__ == '__main__':
    update_domain_cert_info(1)
