# -*- coding: utf-8 -*-

from operator import itemgetter

from playhouse.shortcuts import model_to_dict

from domain_admin.config import MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from domain_admin.model import DomainModel
from domain_admin.service.render_service import render_template
from domain_admin.utils.email_util import EmailServer


def send_email(subject,
               content,
               to_addresses,
               content_type='plain'):
    email_server = EmailServer(
        mail_host=MAIL_HOST,
        mail_port=MAIL_PORT,
        mail_username=MAIL_USERNAME,
        mail_password=MAIL_PASSWORD
    )

    email_server.send_email(
        subject=subject,
        content=content,
        to_addresses=to_addresses,
        content_type=content_type
    )

    email_server.quit()


def send_domain_list_email(to_addresses):
    lst = DomainModel.select()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'start_date',
            'expire_date',
            'expire_days',
        ]
    ), lst))

    lst = sorted(lst, key=itemgetter('expire_days'))

    content = render_template('domain-cert-email.html', {'list': lst})

    send_email(
        subject='域名证书信息',
        content=content,
        to_addresses=to_addresses,
        content_type='html'
    )


if __name__ == '__main__':
    #     render_template('domain-cert-email.html', )
    # send_email("关于你好的通知", "这是内容", '1940607002@qq.com')
    send_domain_list_email()
