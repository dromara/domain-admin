# -*- coding: utf-8 -*-
import yaml


def read_yaml_file(filename):
    with open(filename, "rb") as f:
        return yaml.safe_load(f)
