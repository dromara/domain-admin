# -*- coding: utf-8 -*-
from domain_admin.log import logger
from domain_admin.service import system_service
from domain_admin.utils.email_util import EmailServer
from domain_admin.utils.flask_ext.app_exception import AppException


def send_email(content: str,
               to_addresses: list,
               content_type: str = 'plain'):
    """
    发送邮件
    :param content:
    :param to_addresses:
    :param content_type:
    :return:
    """
    # print('to_addresses:', to_addresses)

    config = system_service.get_system_config()

    system_service.check_email_config(config)

    email_server = EmailServer(
        mail_host=config['mail_host'],
        mail_port=int(config['mail_port']),
        mail_alias=config['mail_alias'],
        mail_username=config['mail_username'],
        mail_password=config['mail_password']
    )

    email_server.send_email(
        subject=config.get('mail_subject', '-'),
        content=content,
        to_addresses=to_addresses,
        content_type=content_type
    )

    email_server.quit()
