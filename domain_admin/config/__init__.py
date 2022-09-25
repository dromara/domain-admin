# -*- coding: utf-8 -*-
from .default_config import *
from .yaml_config import *

# 'sqlite:///default.db'
SQLITE_DATABASE_PATH = os.path.join(ROOT_DIR, 'database.db')
SQLITE_DATABASE_URL = 'sqlite:///' + SQLITE_DATABASE_PATH
