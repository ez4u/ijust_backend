# -*- coding: utf-8 -*-

# python imports
from passlib.apps import custom_app_context as pwd_context

# project imports
from project.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))


    def hash_password(self, password):
        password = password.encode('utf-8')
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        password = password.encode('utf-8')
        return pwd_context.verify(password, self.password)


    def to_json(self):
        return dict(email=self.email,
                    firstname=self.firstname,
                    lastname=self.lastname)
