# -*- coding: utf-8 -*-

from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ['cache', 'db']

cache = Cache()
db = SQLAlchemy()
