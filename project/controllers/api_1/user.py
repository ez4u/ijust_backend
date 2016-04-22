# -*- coding: utf-8 -*-

# project imports
from project import app
from project.utils.auth import login_required, generate_token
from project.utils.validators import api_validate_schema

from project.extensions import db
from project.models.user import User

# flask imports
from flask import request, jsonify, g

# python imports
from sqlalchemy.exc import IntegrityError



@app.api_route('/user/', methods=['GET'])
@login_required
def get_user_info():
	user_obj = User.query.get(g.token_data['id'])
	return jsonify(user_obj.to_json()), 200


@app.api_route('/user/login/', methods=['POST'])
@api_validate_schema('user.login_schema')
def login():
	data = request.json
	username = data['username']
	password = data['password']

	user_obj = User.query.filter_by(username=username).first()
	if not user_obj:
		return jsonify(errors='user does not exist'), 404
	if user_obj.verify_password(password):
		return jsonify(token=generate_token(dict(id=user_obj.id))), 200
	return jsonify(errors='wrong password'), 406


@app.api_route('/user/signup/', methods=['POST'])
@api_validate_schema('user.signup_schema')
def signup():
	data = request.json
	username = data['username']
	email = data['email']
	password = data['password']

	try:
		user_obj = User(username=username, email=email)
		user_obj.hash_password(password)
		db.session.add(user_obj)
		db.session.commit()
	except IntegrityError:
		return jsonify(errors='username already exist'), 406

	return '', 201
