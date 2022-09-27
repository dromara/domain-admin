# -*- coding: utf-8 -*-

from domain_admin.utils.flask_ext.json.default import default_json_encoder

try:
    from flask.json.provider import DefaultJSONProvider, _default
except ImportError:
    class DefaultJSONProvider(object):
        pass


    def _default(o):
        pass


class JSONProvider(DefaultJSONProvider):
    """
    Flask 2.2.2
    """

    @staticmethod
    def default(o):
        ret = default_json_encoder(o)
        if ret is not o:
            return ret

        return _default(o)
