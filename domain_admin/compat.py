# -*- coding: utf-8 -*-
"""
@File    : _compat.py
@Date    : 2023-07-09

requests: https://github.com/psf/requests/blob/v2.27.x/requests/compat.py
werkzeug: https://github.com/pallets/werkzeug/blob/1.0.x/src/werkzeug/_compat.py
flask: https://github.com/pallets/flask/blob/1.0.x/flask/_compat.py

six: https://six.readthedocs.io/
"""
from __future__ import print_function, unicode_literals, absolute_import, division

try:
    # Flask Version 2.1.0
    # safe_join is removed, use werkzeug.utils.safe_join instead
    from flask import safe_join
except ImportError:
    # werkzeug Version 0.7
    # Added werkzeug.security.safe_join().
    from werkzeug.security import safe_join

try:
    # @since Python 3.10
    from collections.abc import Iterator
except ImportError:
    from collections import Iterator
