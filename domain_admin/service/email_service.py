# -*- coding: utf-8 -*-

from domain_admin.config import MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from domain_admin.utils.email_util import EmailServer


def send_email(subject: str,
               content: str,
               to_addresses: list,
               content_type: str = 'plain'):
    """
    发送邮件
    :param subject:
    :param content:
    :param to_addresses:
    :param content_type:
    :return:
    """
    
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
