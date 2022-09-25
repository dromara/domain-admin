# -*- coding: utf-8 -*-

from jinja2 import Environment
from jinja2 import FileSystemLoader

from domain_admin.config import TEMPLATE_DIR


def render_template(template, data):
    """
    渲染模板
    :param template:
    :param data:
    :return:
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    t = env.get_template(template)
    return t.render(data)
