# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


class EmailServer(object):
    """
    邮件发送
    """

    def __init__(self,
                 mail_host,
                 mail_port,
                 mail_alias,
                 mail_username,
                 mail_password):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_alias = mail_alias
        self.mail_username = mail_username
        self.mail_password = mail_password
        self._server = None

    # def __del__(self):
    #     self.quit()

    @property
    def server(self):
        if self._server is None:
            self._server = self.get_server()

        return self._server

    def quit(self):
        if self.server:
            self.server.quit()
            self._server = None

    def get_server(self):
        """
        获取邮件服务器
        """
        if self.mail_port == 465:
            # ssl 465端口
            server = smtplib.SMTP_SSL(self.mail_host)
        elif self.mail_port == 587:
            # starttls 587端口
            server = smtplib.SMTP(self.mail_host, self.mail_port)
            server.starttls()
        else:
            # 25端口
            server = smtplib.SMTP(self.mail_host, self.mail_port)

        # server.connect(host=self.mail_host, port=self.mail_port)

        # print(self.mail_username, self.mail_password)

        server.login(self.mail_username, self.mail_password)

        return server

    def get_email_content(self, subject, content, content_type='plain'):
        # 构造邮件
        msg = MIMEText(content, content_type, 'utf-8')
        # 邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr((self.mail_alias, self.mail_username))
        # msg['To'] = to_addresses.join(',')
        msg['Subject'] = subject
        return msg

    def send_email(self, subject, content, to_addresses, content_type='plain'):
        """
        :param subject:
        :param content:
        :param to_addresses:
        :param content_type:  plain/html
        :return:
        """

        email_content = self.get_email_content(subject, content, content_type)

        # 发送邮件
        self.server.sendmail(
            from_addr=self.mail_username,
            to_addrs=to_addresses,
            msg=email_content.as_string()
        )


def send_email(
        subject, content, to_addresses,
        mail_host='localhost', mail_port=25, content_type='plain',
        mail_alias=None, mail_username=None, mail_password=None
):
    """
    发送邮件
    ref: https://www.runoob.com/python/python-email.html

    :param mail_host:
    :param mail_port:
    :param mail_alias:
    :param subject:
    :param content:
    :param to_addresses:
    :param mail_username:
    :param mail_password:
    :param content_type:
    :return:
    """
    mail_username = mail_username or 'admin@domain-admin.com'
    mail_alias = mail_alias or mail_username

    # 构造邮件
    message = MIMEText(content, content_type, 'utf-8')
    # 邮箱昵称、发件人邮箱账号
    message['From'] = formataddr((mail_alias, mail_username))
    message['Subject'] = Header(subject, 'utf-8')

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
