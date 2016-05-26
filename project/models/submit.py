# -*- coding: utf-8 -*-

# project imports
from project.extensions import db


class Submit(db.Model):
    __tablename__ = 'submits'
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String(16), nullable=False)
    code = db.Column(db.String(100 * 1024), nullable=False)
    language = db.Column(db.String(16), nullable=False)
    submitted_on = db.Column(db.DateTime, nullable=False)

    fk_user = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    user = db.relationship('User', foreign_keys='Submit.fk_user')

    fk_team = db.Column(db.Integer, db.ForeignKey('teams.id'), index=True, nullable=False)
    team = db.relationship('Team', foreign_keys='Submit.fk_team')

    fk_problem = db.Column(db.Integer, db.ForeignKey('problems.id'), index=True, nullable=False)
    problem = db.relationship('Problem', foreign_keys='Submit.fk_problem')

