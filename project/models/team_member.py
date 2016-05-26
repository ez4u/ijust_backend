# -*- coding: utf-8 -*-

# project imports
from project.extensions import db


class TeamMember(db.Model):
    __tablename__ = 'team_members'
    fk_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    user = db.relationship('User', foreign_keys='TeamMember.fk_user')

    fk_team = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True, nullable=False)
    team = db.relationship('Team', foreign_keys='TeamMember.fk_team')


    def to_json(self):
        return dict(user=self.user.to_json(),
                    team=self.team.to_json())

