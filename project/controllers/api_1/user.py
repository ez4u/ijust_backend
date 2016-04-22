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



###############################  View  ######################################
#############################################################################


@app.api_route('/user/', methods=['GET'])
@login_required
def get_user_info():
	"""
    Get Current User Info
    Get basic information of current user
    ---
    tags:
      - user
    parameters:
      - name: TOKEN
        in: header
        type: string
        required: true
        description: Token of current user
    responses:
      200:
        description: Current user basic information
        schema:
          type: object
          properties:
            email:
              type: string
              description: Email of current user
            firstname:
              type: string
              description: Firstname of current user
            lastname:
              type: string
              description: Lastname of current user
      401:
        description: Token not found or is invalid or has expired
	"""

	user_obj = User.query.get(g.token_data['id'])
	return jsonify(user_obj.to_json()), 200


###############################  Login  #####################################
#############################################################################


@app.api_route('/user/login/', methods=['POST'])
@api_validate_schema('user.login_schema')
def login():
	"""
    Login
    ---
    tags:
      - user
    parameters:
      - name: body
        in: body
        type: object
        description: username and password for login
        required: true
        schema:
          id: Login
          required:
            - login
            - password
          properties:
            login:
              type: string
              example: babyknight
              description: Username or Email
            password:
              type: string
              example: baby123
    responses:
      200:
        description: Successfully logged in
        schema:
          type: object
          properties:
            token:
              type: string
              description: Generated RESTful token
      400:
      	description: Bad request
      404:
        description: User does not exist
      406:
      	description: Wrong password
	"""

	data = request.json
	login = data['login']
	password = data['password']

	if '@' in login:
		user_obj = User.query.filter_by(email=login).first()
	else:
		user_obj = User.query.filter_by(username=login).first()
	if not user_obj:
		return jsonify(errors='user does not exist'), 404
	if user_obj.verify_password(password):
		return jsonify(token=generate_token(dict(id=user_obj.id))), 200
	return jsonify(errors='wrong password'), 406


###############################  Signup  ####################################
#############################################################################


@app.api_route('/user/signup/', methods=['POST'])
@api_validate_schema('user.signup_schema')
def signup():
	"""
    Signup
    ---
    tags:
      - user
    parameters:
      - name: body
        in: body
        type: object
        description: username, email and password for signup
        required: true
        schema:
          id: Signup
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              pattern: ^[\w.]+$
              example: babyknight
              maxLength: 32
            email:
              type: string
              example: baby@knight.org
            password:
              type: string
              example: baby123
              maxLength: 32
    responses:
      201:
        description: Successfully registered
      400:
      	description: Bad request
      406:
      	description: Username or email already exist
	"""

	data = request.json
	username = data['username']
	email = data['email']
	password = data['password']

	if User.query.filter_by(email=email).first():
		return jsonify(errors='email already exist'), 406

	try:
		user_obj = User(username=username, email=email)
		user_obj.hash_password(password)
		db.session.add(user_obj)
		db.session.commit()
	except IntegrityError:
		return jsonify(errors='username already exist'), 406

	return '', 201

