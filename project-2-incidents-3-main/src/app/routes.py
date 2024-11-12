'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Incidents
'''

from datetime import datetime
from app import app, db, cache
from app.models import User, Incident, Country
from app.forms import IncidentUpdateForm, SignUpForm, LoginForm, IncidentSearchForm, IncidentCreateForm
from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import and_, func, desc
from flask_login import login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            user_id = form.id.data.strip()
            existing_user = User.query.filter_by(id=user_id).first()
            if existing_user is None:
                hashed_passwd = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
                new_user = User(id=user_id, name=form.name.data, about=form.about.data, admin=False, passwd=hashed_passwd)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('search_list_incidents')) 
            else:
                flash("user ID already taken! please choose a different one.")
        else:
            flash("passwords do not match! please try again.")
    return render_template('signup.html', form=form)

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.password.data.encode("utf-8"), user.passwd):
            login_user(user)
            flash('login successful!')
            return redirect(url_for('search_list_incidents')) 
        else:
            flash('incorrect username or password. please try again.')
    return render_template('login.html', form=form)


@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    flash('you have been logged out.')
    return redirect(url_for('login'))

@login_required
@app.route('/incidents/search', methods=['GET', 'POST'])
def search_incidents():
    form = IncidentSearchForm()
    if form.validate_on_submit():
        filters = []
        if form.year.data:
            filters.append(Incident.date <= str(form.year.data) + "01-01")
            filters.append(Incident.date >= str(form.year.data -1) + "01-01")
        if form.actorType.data != "0":
            filters.append(Incident.actor_type_code == form.actorType.data)
        if form.industry.data != "0":
            filters.append(Incident.industry_code == form.industry.data)
        if form.motive.data != "0":
            filters.append(Incident.motive_code == form.motive.data)
        if form.eventType.data != "0":
            filters.append(Incident.event_type_code == form.eventType.data)
        if form.countries.data != "NV":
            filters.append(Incident.country_code == form.countries.data)
        
        incidents = []
        if filters:
            incidents = db.session.query(Incident).filter(and_(*filters)).all()
        else:
            incidents = db.session.query(Incident).all()
        return render_template('list_incidents.html', 
            incidents=incidents,
            counter=0, 
            prev_page=0, 
            next_page=2)
    else: 
        print("form.errors:" +  str(form.errors))
    return render_template('search_incidents.html', form=form)


@login_required
@app.route('/incidents')
@cache.cached(timeout=300)
def list_incidents():
    year = request.args.get('year', None)
    country = request.args.get('country', None)
    actor = request.args.get('actor', None)
    event = request.args.get('event', None)
    motive = request.args.get('motive', None)
    industry = request.args.get('industry', None)
    page = request.args.get('page', default=0, type=int)
    page_size = 10
    query = db.session.query(Incident)

    if year:
        query = query.filter(Incident.date == year)
    if country:
        query = query.filter(Incident.country_code == country)
    if actor:
        query = query.filter(Incident.actor_type_code == actor)
    if event:
        query = query.filter(Incident.event_type_code == event)
    if motive:
        query = query.filter(Incident.motive_code == motive)
    if industry:
        query = query.filter(Incident.industry_code == industry)

    counter = query.count()
    query = query.limit(page_size).offset(page * page_size)
    incidents = query.all()
    prev_page = page - 1
    next_page = page + 1
    return render_template('list_incidents.html', incidents=incidents, counter=counter, prev_page=prev_page, next_page=next_page)

@login_required
@app.route('/incidents/search_list', methods=['GET', 'POST'])
def search_list_incidents():
    form = IncidentSearchForm()
    filters = []
    page = request.args.get('page', default=1, type=int)  
    year = request.args.get('year', None)
    country = request.args.get('country', None)
    actor = request.args.get('actor', None)
    event = request.args.get('event', None)
    motive = request.args.get('motive', None)
    industry = request.args.get('industry', None)
    page_size = 10

    if form.validate_on_submit():
        page = 1  
        filters = []  
        if form.year.data:
            year = form.year.data
            filters.append(Incident.date <= str(year) + "01-01")
            filters.append(Incident.date >= str(year - 1) + "01-01")
        if form.actorType.data != "0":
            actor = form.actorType.data
            filters.append(Incident.actor_type_code == form.actorType.data)
        if form.industry.data != "0":
            industry = form.industry.data
            filters.append(Incident.industry_code == form.industry.data)
        if form.motive.data != "0":
            motive = form.motive.data
            filters.append(Incident.motive_code == form.motive.data)
        if form.eventType.data != "0":
            filters.append(Incident.event_type_code == form.eventType.data)
        if form.countries.data != "NV":
            filters.append(Incident.country_code == form.countries.data)
    else:
        if year:
            filters.append(Incident.date <= str(int(year)) + "01-01")
            filters.append(Incident.date >= str(int(year) - 1) + "01-01")
        if country and country != "NV":
            filters.append(Incident.country_code == country)
        if actor and actor != "0":
            filters.append(Incident.actor_type_code == actor)
        if event and event != "0":
            filters.append(Incident.event_type_code == event)
        if motive and motive != "0":
            filters.append(Incident.motive_code == motive)
        if industry and industry != "0":
            filters.append(Incident.industry_code == industry)

    incidents = Incident.query.filter(and_(*filters)).paginate(page=page, per_page=page_size, error_out=False)

    return render_template(
        'search_list_incidents.html',
        incidents=incidents,
        year=year,
        country=country,
        actor=actor,
        event=event,
        motive=motive,
        industry=industry,
        page=page,
        form = IncidentSearchForm()
    )

@login_required
@app.route('/incidents/create',methods=['GET', 'POST'])
def create_incident():
    form = IncidentCreateForm()
    if form.validate_on_submit():
        last_id = db.session.query(Incident.id).order_by(desc(Incident.id)).first()
        # print(db.session.query(Country).filter(Country.code == form.actorCountries.data).all())
        try :
            db.session.add(
                Incident(
                    id = int(last_id[0]) + 1,
                    date = form.date.data,
                    actor = form.actor.data,
                    actor_type_code = form.actor.data,
                    organization = form.organization.data,
                    industry_code = form.industry.data,
                    motive_code = form.motive.data,
                    event_type_code = form.eventType.data,
                    description = form.description.data,
                    source_url = form.sourceUrl.data,
                    country_code = form.countries.data,
                    actor_country = form.actorCountries.data
                )
            )
            db.session.commit()
        except Exception as inst: 
            print(inst)
            return render_template('create_incident.html', form = form)
        # print(str(db.session.query(func.count(Incident.id))))
        return redirect(url_for('search_list_incidents'))
    else:
        return render_template('create_incident.html', form = form)
    



@login_required
@app.route('/incidents/<int:id>',methods=['GET', 'POST'])
def update_incident(id):
    incident = Incident.query.get(id)
    form = IncidentUpdateForm(obj=incident)
    if form.validate_on_submit():
        incident.id=form.id.data
        incident.date=form.date.data
        incident.actor=form.actor.data
        incident.actor_type_code=form.actor_type_code.data
        incident.organization=form.organization.data
        incident.industry_code=form.industry_code.data
        incident.motive_code=form.motive_code.data
        incident.event_type_code=form.event_type_code.data
        incident.description=form.description.data
        incident.source_url=form.source_url.data
        incident.country_code=form.country_code.data
        incident.actor_country=form.actor_country.data
        db.session.commit()
        return redirect(url_for('list_facilities'))
    return render_template('update_incident.html', form=form)

@login_required
@app.route('/incidents/<int:id>/delete', methods=['GET', 'POST'])
def delete_incident(id):
    incident = Incident.query.get_or_404(id)
    
    if not current_user.admin: 
        flash('You do not have permission to delete this incident.')
        return redirect(url_for('search_list_incidents')) 

    if request.method == 'POST':
        db.session.delete(incident)
        db.session.commit()
        flash('Incident deleted successfully.')
        return redirect(url_for('search_list_incidents'))
    
    return render_template('delete_incident.html', incident=incident)

@login_required
@app.route('/incidents/report', methods=['GET', 'POST'])
def report_incidents():
    incidents = db.session.query(Incident).all()
    incidents_per_year = {}
    for incident in incidents:
        year = incident.date.year
        if year in incidents_per_year:
            incidents_per_year[year] += 1
        else:
            incidents_per_year[year] = 1
    sort_incidents_per_year = dict(sorted(incidents_per_year.items()))
    return render_template('report_incidents.html', incidents_per_year=sort_incidents_per_year)
