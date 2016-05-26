# -*- coding: utf-8 -*-

# python imports
from passlib.apps import custom_app_context as pwd_context

# project imports
from project.extensions import db


class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    rate = db.Column(db.SMALLINT)
    open_to_public = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(128))

    create_dt = db.Column(db.DateTime, nullable=False)
    start_dt = db.Column(db.DateTime, nullable=False)
    close_dt = db.Column(db.DateTime)
    duration = db.Column(db.Time, nullable=False)

    fk_owner = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    owner = db.relationship('User', foreign_keys='Contest.fk_owner')


    def hash_password(self, password):
        password = password.encode('utf-8')
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        password = password.encode('utf-8')
        return pwd_context.verify(password, self.password)

