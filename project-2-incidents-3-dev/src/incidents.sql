DROP TABLE IF EXISTS incidents;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    about VARCHAR,
    admin INT,
    passwd BYTEA
);

CREATE TABLE IF NOT EXISTS countries (
    code CHAR(2) PRIMARY KEY, 
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS actor_types (
    code INT PRIMARY KEY, 
    description VARCHAR(25) NOT NULL
);

INSERT INTO actor_types VALUES 
    (1, 'criminal'), 
    (2, 'hacktivist'), 
    (3, 'hobbyist'), 
    (4, 'nation-state'), 
    (5, 'terrorist'), 
    (6, 'other');

CREATE TABLE IF NOT EXISTS event_types (
    code INT PRIMARY KEY, 
    description VARCHAR(15) NOT NULL
);

INSERT INTO event_types VALUES 
    (1, 'exploitive'), 
    (2, 'disruptive'), 
    (3, 'mixed'), 
    (4, 'other');

CREATE TABLE IF NOT EXISTS motives (
    code INT PRIMARY KEY, 
    description VARCHAR(15) NOT NULL
);

INSERT INTO motives VALUES 
    (1, 'financial'), 
    (2, 'inustrial espionage'), 
    (3, 'personal attack'), 
    (4, 'political espionage'), 
    (5, 'protest'), 
    (6, 'sabotage'), 
    (7, 'other');

CREATE TABLE IF NOT EXISTS industries (
    code INT PRIMARY KEY, 
    description VARCHAR(100) NOT NULL
);

INSERT INTO industries VALUES 
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
    (22, 'Wholesale Trade');  

CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL, 
    actor VARCHAR(50) NOT NULL, 
    actor_type_code INT NOT NULL, 
    organization VARCHAR(100) NOT NULL,
    industry_code INT NOT NULL, 
    motive_code INT NOT NULL,
    event_type_code INT NOT NULL,
    description VARCHAR(250) NOT NULL,
    source_url VARCHAR(200) NOT NULL,
    country_code INT NOT NULL,
    actor_country VARCHAR(100) NOT NULL,
    FOREIGN KEY (actor_type_code) REFERENCES actor_types (code), 
    FOREIGN KEY (industry_code) REFERENCES industries (code)
    FOREIGN KEY (event_type_code) REFERENCES event_types (code), 
    FOREIGN KEY (motive_code) REFERENCES motives (code)
);
