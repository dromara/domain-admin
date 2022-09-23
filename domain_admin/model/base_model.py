# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.db_url import connect

db = connect('sqlite:///default.db')


class BaseModel(Model):
    class Meta:
        database = db
