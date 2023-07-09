# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.utils.flask_ext.json.default import default_json_encoder

try:
    from flask.json import JSONEncoder as _JSONEncoder
except ImportError:
    class _JSONEncoder(object):
        def _default(self, o):
            pass


class JSONEncoder(_JSONEncoder):
    """ flask == 0.1 """

    def default(self, o):
        ret = default_json_encoder(o)
        if ret is not o:
            return ret

        return super(JSONEncoder, self).default(o)
