# -*- coding: utf-8 -*-
"""
@File    : fabric_util.py
@Date    : 2023-07-26

参考
https://www.fabfile.org/installing.html
https://docs.fabfile.org/en/stable/api/connection.html

https://www.cnblogs.com/superhin/p/13887526.html
"""

import six
from fabric import Connection


def deploy_file(host, user, password, content, remote):
    with Connection(
            host=host,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.put(six.StringIO(content), remote)


def run_command(host, user, password, command):
    with Connection(
            host=host,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.run(command, hide=True)
