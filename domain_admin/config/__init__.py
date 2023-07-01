# -*- coding: utf-8 -*-
"""
用户自定义配置覆盖系统默认配置
优先级：由高到低
env_config > default_config > runtime_config
"""
from .runtime_config import *
from .env_config import *
