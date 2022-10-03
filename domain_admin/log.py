# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('domain-admin')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
