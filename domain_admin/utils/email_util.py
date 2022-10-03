# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class EmailServer(object):
    def __init__(self, mail_host, mail_port,mail_alias, mail_username, mail_password):
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

    def get_server(self):
        """
        获取邮件服务器
        """
        if self.mail_port == 465:
            # ssl 465端口
            server = smtplib.SMTP_SSL(self.mail_host)
        else:
            # 25端口
            server = smtplib.SMTP(self.mail_host, self.mail_port)

        # server.connect(host=self.mail_host, port=self.mail_port)

        # print(self.mail_username, self.mail_password)

        server.login(self.mail_username, self.mail_password)

        return server

    def quit(self):
        if self.server:
            self.server.quit()

    def get_email_content(self, subject, content, content_type='plain'):
        # 构造邮件
        msg = MIMEText(content, content_type, 'utf-8')
        # 邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr([self.mail_alias, self.mail_username])
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
