# -*- coding: utf-8 -*-

from flask.json import JSONEncoder as _JSONEncoder

from domain_admin.utils.flask_ext.json.default import default_json_encoder


class JSONEncoder(_JSONEncoder):
    """ flask == 0.1 """

    def default(self, o):
        ret = default_json_encoder(o)
        if ret is not o:
            return ret

        return super().default(o)
