# -*- coding: utf-8 -*-

# python imports
from functools import wraps

# flask imports
from flask import request, jsonify, g
from uuid import uuid4
from redis import Redis

# project imports
from project import app

redis = Redis()


def generate_token(data):
	token = str(uuid4())
	redis.setex(token, data, app.config['TOKEN_EXPIRE_TIME'])
	return token


def expire_token():
	redis.delete(request.headers['TOKEN'])


def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		if not 'TOKEN' in request.headers:
			return jsonify(errors='token not found'), 401

		token = request.headers['TOKEN']
		token_data = redis.get(token)
		if not token_data:
			return jsonify(errors='token is invalid or has expired'), 401
		
		g.token_data = token_data

		return f(*args, **kwargs)

	return decorated
