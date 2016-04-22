# -*- coding: utf-8 -*-

# python imports
from functools import wraps

# flask imports
from flask import request, jsonify, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

# project imports
from project import app

serializer = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=app.config['TOKEN_EXPIRE_TIME'])


def generate_token(data):	
	return serializer.dumps(data)


def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		if not 'TOKEN' in request.headers:
			return jsonify(errors='token not found'), 401

		token = request.headers['TOKEN']
		try:
			token_data = serializer.loads(token)
		except SignatureExpired:
			return jsonify(errors='expired token'), 401
		except BadSignature:
			return jsonify(errors='invalid token'), 401

		g.token_data = token_data

		return f(*args, **kwargs)

	return decorated
