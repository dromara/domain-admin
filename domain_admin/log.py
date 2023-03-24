# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

from domain_admin.service.file_service import resolve_log_file

logger = logging.getLogger('domain-admin')

# 单个日志文件最大为1M
handler = RotatingFileHandler(resolve_log_file("domain-admin.log"), maxBytes=1024 * 1024 * 1, encoding='utf-8')

# logger.addHandler(logging.FileHandler(resolve_log_file("domain-admin.log")))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
