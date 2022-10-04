# -*- coding: utf-8 -*-
import logging

from domain_admin.service.file_service import resolve_log_file

logger = logging.getLogger('domain-admin')
logger.addHandler(logging.FileHandler(resolve_log_file("domain-admin.log")))
logger.setLevel(logging.DEBUG)
