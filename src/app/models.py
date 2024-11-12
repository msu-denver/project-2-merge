'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Incidents
'''

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms.validators import DataRequired
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    passwd = db.Column(db.String, nullable=False)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Country(db.Model):
    __tablename__ = 'countries'
    code = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'

class ActorType(db.Model):
    __tablename__ = 'actor_types'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'

class EventType(db.Model):
    __tablename__ = 'event_types'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'

class Motive(db.Model):
    __tablename__ = 'motives'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'

class Industry(db.Model):
    __tablename__ = 'industries'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'

class Incident(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    actor = db.Column(db.String, nullable=False)
    actor_type_code = db.Column(db.Integer, db.ForeignKey('actor_types.code'))
    actor_type = db.relationship('ActorType', backref='incidents', foreign_keys=[actor_type_code])
    organization = db.Column(db.String, nullable=False)
    industry_code = db.Column(db.Integer, db.ForeignKey('industries.code'))
    industry = db.relationship('Industry', backref='incidents', foreign_keys=[industry_code])
    motive_code = db.Column(db.Integer, db.ForeignKey('motives.code'))
    motive = db.relationship('Motive', backref='incidents', foreign_keys=[motive_code])
    event_type_code = db.Column(db.Integer, db.ForeignKey('event_types.code'))
    event_type = db.relationship('EventType', backref='incidents', foreign_keys=[event_type_code])
    description = db.Column(db.String, nullable=False)
    source_url = db.Column(db.String, nullable=False)
    country_code = db.Column(db.String, db.ForeignKey('countries.code'))
    country = db.relationship('Country', backref='incidents', foreign_keys=[country_code])
    actor_country = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.id},{self.date},{self.actor},{self.actor_type},{self.organization},{self.industry},{self.motive},{self.event_type},{self.description},{self.source_url},{self.country},{self.actor_country}'