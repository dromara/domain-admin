# -*- coding: utf-8 -*-
"""
@File    : fake_stmpd.py
@Date    : 2023-07-01
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import smtpd
import asyncore


class FakeSMTPServer(smtpd.SMTPServer):
    """
    A Fake smtp server
    ref: https://www.coder.work/article/341931
    """

    def __init__(*args, **kwargs):
        print("Running fake smtp server on port 25")
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        print('process_message')
        pass


if __name__ == "__main__":
    smtp_server = FakeSMTPServer(('localhost', 8081), None)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
