# -*- coding: utf-8 -*-

# project imports
from project import app
from project.utils.auth import login_required, generate_token, expire_token
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
def get_current_user_profile():
    """
    Get Current User Profile
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
        description: Current user profile
        schema:
          id: UserProfile
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
        description: Token is invalid or has expired
    """

    user_obj = User.query.get(g.token_data['user_id'])
    return jsonify(user_obj.to_json()), 200


#############################################################################


@app.api_route('/user/<string:username>/', methods=['GET'])
def get_user_profile(username):
    """
    Get An User Profile
    ---
    tags:
      - user
    parameters:
      - name: username
        in: path
        type: string
        required: true
    responses:
      200:
        description: User profile
        schema:
          $ref: "#/definitions/api_1_user_get_current_user_profile_get_UserProfile"
      404:
        description: User does not exist
    """

    user_obj = User.query.filter_by(username=username).first()
    if not user_obj:
        return jsonify(errors='user does not exist'), 404
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
        description: username and password for login
        required: true
        schema:
          id: UserLogin
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
        return jsonify(token=generate_token(dict(user_id=user_obj.id))), 200

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
        description: username, email and password for signup
        required: true
        schema:
          id: UserSignup
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
              minLength: 3
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


###############################  Logout  ####################################
#############################################################################


@app.api_route('/user/logout/', methods=['POST'])
@login_required
def logout():
    """
    Logout
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
        description: Successfully logged out
      401:
        description: Token is invalid or has expired
    """

    expire_token()
    return '', 200


################################  Edit  #####################################
#############################################################################


@app.api_route('/user/', methods=['PUT'])
@api_validate_schema('user.edit_schema')
@login_required
def edit():
    """
    Edit Current User Profile
    ---
    tags:
      - user
    parameters:
      - name: TOKEN
        in: header
        type: string
        required: true
        description: Token of current user
      - name: body
        in: body
        required: true
        schema:
          id: UserEdit
          properties:
            firstname:
              type: string
              example: newbaby
              maxLength: 32
            lastname:
              type: string
              example: newknight
              maxLength: 32
            password:
              schema:
                id: UserChangePassword
                properties:
                    old:
                      type: string
                      example: baby123
                      minLength: 3
                      maxLength: 32
                    new:
                      type: string
                      example: baby321
                      minLength: 3
                      maxLength: 32
    responses:
      200:
        description: Successfully edited
      400:
          description: Bad request
      406:
          description: Not acceptable
    """

    data = request.json
    user_obj = User.query.get(g.token_data['user_id'])

    if 'password' in data:
        old = data['password']['old']
        new = data['password']['new']
        data.pop('password')

        if not user_obj.verify_password(old):
            return '', 406
        user_obj.hash_password(new)

    if len(data):
        user_obj.query.update(data)
    db.session.commit()

    return '', 200

