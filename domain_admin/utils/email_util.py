# -*- coding: utf-8 -*-
"""
email_util.py
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

# 默认的发件人
DEFAULT_MAIL_USERNAME = 'admin@domain-admin.com'


def get_email_server(mail_host='localhost', mail_port=25):
    """
    创建邮箱连接服务的工厂方法
    :param mail_host: 主机地址
    :param mail_port: 端口
    :return:
    """
    # 获取email服务
    if mail_port == 465:
        # ssl 465端口
        server = smtplib.SMTP_SSL(mail_host)
    elif mail_port == 587:
        # starttls 587端口
        server = smtplib.SMTP(mail_host, mail_port)
        server.starttls()
    else:
        # 25端口
        server = smtplib.SMTP(mail_host, mail_port)

    return server


def send_email(
        subject, content, to_addresses,
        mail_host='localhost', mail_port=25, content_type='plain',
        mail_alias=None, mail_username=None, mail_password=None
):
    """
    发送邮件
    ref: https://www.runoob.com/python/python-email.html

    :param mail_host: 主机地址
    :param mail_port: 端口
    :param mail_alias: 发件人别名
    :param subject: 主题
    :param content: 内容
    :param to_addresses: 收件人列表
    :param mail_username: 发件人账号
    :param mail_password: 发件人密码
    :param content_type: 内容类型
        - plain: 文本
        - html: 富文本
    :return:
    """
    mail_username = mail_username or DEFAULT_MAIL_USERNAME
    mail_alias = mail_alias or mail_username

    # 构造邮件
    message = MIMEText(content, content_type, 'utf-8')
    # 邮箱昵称、发件人邮箱账号
    message['From'] = formataddr((mail_alias, mail_username))
    message['Subject'] = Header(subject, 'utf-8')

    server = get_email_server(mail_host, mail_port)

    # 需要登录，否则匿名
    if mail_password:
        server.login(mail_username, mail_password)

    # 发送
    server.sendmail(
        from_addr=mail_username,
        to_addrs=to_addresses,
        msg=message.as_string()
    )

    # 退出
    server.quit()
