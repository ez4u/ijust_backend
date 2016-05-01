# -*- coding: utf-8 -*-

# project imports
from project.extensions import db


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    fk_owner = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    owner = db.relationship('User', foreign_keys='Team.fk_owner')

    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    owner=self.owner.to_json())

