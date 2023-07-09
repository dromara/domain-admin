# -*- coding: utf-8 -*-
"""
用户自定义配置覆盖系统默认配置
优先级：由高到低
env_config > default_config > runtime_config
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from .runtime_config import *
from .env_config import *
