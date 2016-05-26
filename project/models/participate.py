# -*- coding: utf-8 -*-

# project imports
from project.extensions import db


class Participate(db.Model):
    __tablename__ = 'participates'
    accept_reject = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime)

    fk_team = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True, nullable=False)
    team = db.relationship('Team', foreign_keys='Participate.fk_team')

    fk_contest = db.Column(db.Integer, db.ForeignKey('contests.id'), primary_key=True, nullable=False)
    contest = db.relationship('Contest', foreign_keys='Participate.fk_contest')

