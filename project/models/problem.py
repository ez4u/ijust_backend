# -*- coding: utf-8 -*-

# project imports
from project.extensions import db


class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    rate = db.Column(db.SMALLINT)

    time_limit = db.Column(db.SMALLINT, nullable=False) ## seconds
    space_limit = db.Column(db.SMALLINT, nullable=False) ## megabytes

    body = db.Column(db.String(100 * 1024), nullable=False)

    fk_contest = db.Column(db.Integer, db.ForeignKey('contests.id'), index=True, nullable=False)
    contest = db.relationship('Contest', foreign_keys='Problem.fk_contest')


    __table_args__  = (db.UniqueConstraint('number', 'fk_contest'), )

