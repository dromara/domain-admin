# -*- coding: utf-8 -*-

from operator import itemgetter

from playhouse.shortcuts import model_to_dict

from domain_admin.config import MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from domain_admin.model import DomainModel
from domain_admin.service import render_service
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