'''
CS 3700 - Networking & Distributed Computing - Fall 2024
Instructor: Thyago Mota
Student:
Description: Project 2 - Db initialization
'''

import sqlite3
import csv
import os

def get_actor_type_code(actor_type):
    if actor_type.startswith('Criminal'):
        return 1
    if actor_type.startswith('Hack'):
        return 2
    if actor_type.startswith('Hobb'):
        return 3
    if actor_type.startswith('Nation'):
        return 4
    if actor_type.startswith('Terr'):
        return 5
    return 6

def get_motive_code(motive):
    if motive.startswith('Finan'):
        return 1
    if motive.startswith('Industr'):
        return 2
    if motive.startswith('Personal'):
        return 3
    if motive.startswith('Politi'):
        return 4
    if motive.startswith('Protes'):
        return 5
    if motive.startswith('Sabot'):
        return 6    
    return 7

def get_event_type_code(event):
    if event.startswith('Explo'):
        return 1
    if event.startswith('Disru'):
        return 2
    if event.startswith('Mixe'):
        return 3
    return 4

def get_industry_code(industry):
    if industry.startswith('Accomod'):
        return 1
    if industry.startswith('Administrative'):
        return 2
    if industry.startswith('Agriculture'):
        return 3
    if industry.startswith('Arts'):
        return 4   
    if industry.startswith('Constru'):
        return 5
    if industry.startswith('Edu'):
        return 6
    if industry.startswith('Finan'):
        return 7
    if industry.startswith('Health'):
        return 8
    if industry.startswith('Infor'):
        return 9
    if industry.startswith('Manage'):
        return 10
    if industry.startswith('Manuf'):
        return 11
    if industry.startswith('Medusa'):
        return 12
    if industry.startswith('Minin'):
        return 13
    if industry.startswith('Other'):
        return 14
    if industry.startswith('Profes'):
        return 15
    if industry.startswith('Publ'):
        return 16
    if industry.startswith('Real'):
        return 17
    if industry.startswith('Retai'):
        return 18
    if industry.startswith('Trans'):
        return 19
    if industry.startswith('Whole'):
        return 22
    if industry.startswith('Util'):
        return 21
    return 20

def get_country_code_from_description(countries, description):
    for country in countries: 
        if country.startswith(description[:10]): 
            return countries[country]
    if description.startswith('Moldova (the Republic of)'):
        return 'MD'
    if description.startswith('Venezuela'):
        return 'VE'
    if description.startswith('Taiwan'):
        return 'TW'
    if description.startswith('Korea (the Republic of)'):
        return 'KR'
    if description.startswith('Iran (Islamic Republic of)'):
        return 'IR'
    if description.startswith('Czechia'):
        return 'CZ'
    if description.startswith('Bolivia (Plurinational State of)'):
        return 'BO'
    if description.startswith('Korea (the Democratic'):
        return 'KP'
    if description.startswith('Lebanon'):
        return 'LB'
    if description.startswith('Cabo Verde'):
        return 'CV'
    if description.startswith('Republic of North Macedonia'):
        return 'MK'
    if description.startswith('Islamic Republic of Iran'):
        return 'IR'
    if description.startswith('Undetermined'):
        return 'ZZ'
    print(f'{description} not found!!!')
    return 'ZZ'

if __name__ == '__main__':

    try: 
        os.makedirs('instance')
    except: 
        pass

    conn = sqlite3.connect('instance/incidents.db')

    with open('incidents.sql') as f:
        conn.executescript(f.read())

    conn.commit()

    # populate the countries table
    cur = conn.cursor()
    countries = {}
    with open('../data/countries.csv', 'rt') as f: 
        for row in csv.DictReader(f, delimiter=',', quotechar='"'):
            sql = 'INSERT INTO countries VALUES (?, ?)'
            cur.execute(sql, [row['Code'], row['Name']])
            countries[row['Name']] = row['Code']
    conn.commit()

    # add some initial incidents
    with open('../data/incidents.csv', 'rt', encoding='latin-1') as f: 
        for row in csv.DictReader(f, delimiter=',', quotechar='"'):
            actor_type_code = get_actor_type_code(row['actor_type'])

            sql = 'INSERT INTO incidents (date, actor, actor_type_code, organization, industry_code, motive_code, event_type_code, description, source_url, country_code, actor_country) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )'
            cur.execute(sql, [row['event_date'], row['actor'], get_actor_type_code(row['actor_type']), row['organization'], get_industry_code(row['industry']), get_motive_code(row['motive']), get_event_type_code(row['event_type']), row['description'], row['source_url'], get_country_code_from_description(countries, row['country']), row['actor_country']])
            conn.commit()

    sql = 'SELECT COUNT(*) FROM incidents'
    cur.execute(sql)
    row = cur.fetchone()
    print(row[0], 'incidents inserted!')

    os.chdir('..')
    conn.close()