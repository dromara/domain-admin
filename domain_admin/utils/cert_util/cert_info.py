# -*- coding: utf-8 -*-
"""
@File    : cert_info.py
@Date    : 2023-06-19
"""

from datetime import datetime
from typing import NamedTuple


class CertInfo(NamedTuple):
    # 开始时间
    start_time: datetime
    # 结束时间
    expire_time: datetime
