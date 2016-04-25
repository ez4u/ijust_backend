# -*- coding: utf-8 -*-

# python imports
import random
import string
import os


data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')


class DefaultConfig(object):
	DEFAULT_APP_NAME = 'ijust'
	DEBUG = True
	TESTING = True
	TOKEN_EXPIRE_TIME = 3600 * 5

	# CACHE
	CACHE_TYPE = 'redis'
	CACHE_DEFAULT_TIMEOUT = 10
	CACHE_THRESHOLD = 100
	CACHE_DIR = os.path.join(data_dir, 'cache')
	CACHE_NO_NULL_WARNING = True

	# DATABASE
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/db.sqlite' % data_dir


class DevelopmentConfig(DefaultConfig):
	TESTING = False


class ProductionConfig(DevelopmentConfig):
	DEBUG = False
