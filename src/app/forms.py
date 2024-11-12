'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Incidents
'''

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Optional, ReadOnly
from datetime import datetime
import csv

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class IncidentSearchForm(FlaskForm):
    year = IntegerField('Year', default=None, validators=[Optional()])
    actorType = SelectField('Actor Type', choices=[
        (0, "any"),
        (1, "criminal"), 
        (2, "hactivist"),
        (3, "hobbyist"), 
        (4, "nation-state"),
        (5, "terrorist"), 
        (6, "other")
    ])
    industry = SelectField("Industry", choices=[
        (0, "any"),
        (1, 'Accommodation and Food Services'), 
        (2, 'Waste Management and Remediation Services'), 
        (3, 'Agriculture, Forestry, Fishing and Hunting'),
        (4, 'Arts, Entertainment, and Recreation'),
        (5, 'Construction'),
        (6, 'Educational Services'),
        (7, 'Finance and Insurance'),
        (8, 'Health Care and Social Assistance'),
        (9, 'Information'),
        (10, 'Management of Companies and Enterprises'),
        (11, 'Manufacturing'),
        (12, 'Medusa'),
        (13, 'Mining, Quarrying, and Oil and Gas Extraction'),
        (14, 'Other Services (except Public Administration)'),
        (15, 'Professional, Scientific, and Technical Services'),
        (16, 'Public Administration'),
        (17, 'Real Estate and Rental and Leasing'),
        (18, 'Retail Trade'),
        (19, 'Transportation and Warehousing'),
        (20, 'Undetermined'),
        (21, 'Utilities'),
        (22, 'Wholesale Trade')
    ])
    motive = SelectField("Motive", choices=[
        (0, "any"),
        (1, 'financial'), 
        (2, 'industrial espionage'), 
        (3, 'personal attack'), 
        (4, 'political espionage'), 
        (5, 'protest'), 
        (6, 'sabotage'), 
        (7, 'other')
    ])
    eventType = SelectField("Event type", choices=[
        (0, "any"),
        (1, 'exploitive'), 
        (2, 'disruptive'), 
        (3, 'mixed'), 
        (4, 'other')
    ])
    
    _countries = [("NV", "any")]  
    try:
        with open('../data/countries.csv', 'rt') as f:
            for row in csv.DictReader(f, delimiter=',', quotechar='"'):
                code = row.get("Code")  # Use .get() to avoid KeyError
                name = row.get("Name")
                if code and name:  # Only append if both values exist
                    _countries.append((code, name))
                else:
                    print(f"Missing data in row: {row}")  # Debugging output
    except FileNotFoundError:
        print("Error: countries.csv file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    countries = SelectField("Country", choices=_countries)

    submit = SubmitField('Confirm')
class IncidentCreateForm(FlaskForm):
    date = DateField('Year', validators=[DataRequired()])
    actor = TextAreaField('Actor', validators=[DataRequired()])
    actorType = SelectField('Actor Type', choices=[
            (1, "criminal"),
            (2, "hactivist"),
            (3, "hobbyist"), 
            (4, "nation-state"), 
            (5, "terrorist"), 
            (6, "other")
        ], validators=[DataRequired()])
    organization = TextAreaField("Targeted organization", validators=[DataRequired()])
    industry = SelectField("Industry", choices=[
            (1, 'Accommodation and Food Services'), 
            (2, 'Waste Management and Remediation Services'), 
            (3, 'Agriculture, Forestry, Fishing and Hunting'),
            (4, 'Arts, Entertainment, and Recreation'),
            (5, 'Construction'),
            (6, 'Educational Services'),
            (7, 'Finance and Insurance'),
            (8, 'Health Care and Social Assistance'),
            (9, 'Information'),
            (10, 'Management of Companies and Enterprises'),
            (11, 'Manufacturing'),
            (12, 'Medusa'),
            (13, 'Mining, Quarrying, and Oil and Gas Extraction'),
            (14, 'Other Services (except Public Administration)'),
            (15, 'Professional, Scientific, and Technical Services'),
            (16, 'Public Administration'),
            (17, 'Real Estate and Rental and Leasing'),
            (18, 'Retail Trade'),
            (19, 'Transportation and Warehousing'),
            (20, 'Undetermined'),
            (21, 'Utilities'),
            (22, 'Wholesale Trade')
        ])
    motive = SelectField("Motive", choices=[
            (1, 'financial'), 
            (2, 'industrial espionage'), 
            (3, 'personal attack'), 
            (4, 'political espionage'), 
            (5, 'protest'), 
            (6, 'sabotage'), 
            (7, 'other')
        ],validators=[DataRequired()])
    eventType = SelectField("Event type", choices=[
            (1, 'exploitive'), 
            (2, 'disruptive'), 
            (3, 'mixed'), 
            (4, 'other')
        ],validators=[DataRequired()])
    description = TextAreaField("Description")
    sourceUrl = TextAreaField("Source URL")
    
    actor 
    _countries = []  
    try:
        with open('../data/countries.csv', 'rt') as f:
            for row in csv.DictReader(f, delimiter=',', quotechar='"'):
                code = row.get("Code")  # Use .get() to avoid KeyError
                name = row.get("Name")
                if code and name:  # Only append if both values exist
                    _countries.append((code, name))
                else:
                    print(f"Missing data in row: {row}")  # Debugging output
    except FileNotFoundError:
        print("Error: countries.csv file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    countries = SelectField("Attack Country", choices=_countries, validators=[DataRequired()])
    actorCountries = SelectField("Actor Country", choices=_countries, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class IncidentUpdateForm(FlaskForm):
    id = IntegerField('ID', validators=[ReadOnly()])
    date = DateField('Year', validators=[DataRequired()])
    actor = StringField('Actor', validators=[DataRequired()])
    actor_type_code = SelectField('Actor Type', choices=[
        (1, "criminal"),
        (2, "hactivist"),
        (3, "hobbyist"), 
        (4, "nation-state"), 
        (5, "terrorist"), 
        (6, "other")
    ], validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    industry_code = SelectField("Industry", choices= [
        (1, 'Accommodation and Food Services'), 
        (2, 'Waste Management and Remediation Services'), 
        (3, 'Agriculture, Forestry, Fishing and Hunting'),
        (4, 'Arts, Entertainment, and Recreation'),
        (5, 'Construction'),
        (6, 'Educational Services'),
        (7, 'Finance and Insurance'),
        (8, 'Health Care and Social Assistance'),
        (9, 'Information'),
        (10, 'Management of Companies and Enterprises'),
        (11, 'Manufacturing'),
        (12, 'Medusa'),
        (13, 'Mining, Quarrying, and Oil and Gas Extraction'),
        (14, 'Other Services (except Public Administration)'),
        (15, 'Professional, Scientific, and Technical Services'),
        (16, 'Public Administration'),
        (17, 'Real Estate and Rental and Leasing'),
        (18, 'Retail Trade'),
        (19, 'Transportation and Warehousing'),
        (20, 'Undetermined'),
        (21, 'Utilities'),
        (22, 'Wholesale Trade')
    ], validators=[DataRequired()])
    motive_code = SelectField("Motive", choices=[
        (1, 'financial'), 
        (2, 'industrial espionage'), 
        (3, 'personal attack'), 
        (4, 'political espionage'), 
        (5, 'protest'), 
        (6, 'sabotage'), 
        (7, 'other')
    ], validators=[DataRequired()])
    event_type_code = SelectField("Event type", choices=[
        (1, 'exploitive'), 
        (2, 'disruptive'), 
        (3, 'mixed'), 
        (4, 'other')
    ], validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    source_url = StringField('Source URL', validators=[DataRequired()])
    # Getting countries from csv 
    _countries = []
    try:
        with open('../data/countries.csv', 'rt') as f:
            for row in csv.DictReader(f, delimiter=',', quotechar='"'):
                _countries.append((row["Code"], row["Name"]))
    except FileNotFoundError:
        _countries.extend([("US", "United States"), ("UK", "United Kingdom")])
    
    country_code = SelectField("Country", choices=_countries)
    actor_country = StringField('Actor Country', validators=[DataRequired()])
    submit = SubmitField('Confirm')

