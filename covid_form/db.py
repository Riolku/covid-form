from flask_sqlalchemy import SQLAlchemy

from covid_form import app

db = SQLAlchemy(app)

dbcol = db.Column
dbint = db.Integer
dbbool = db.Boolean
dblong = db.BigInteger
dbstr = db.String

class Employees(db.Model):
    id = dbcol(dbint, primary_key = True)
    name = dbcol(dbstr(1024), nullable = False)
    active = dbcol(dbbool, nullable = False)

    __tablename__ = "employees"

class FormResponses(db.Model):
    id = dbcol(dbint, primary_key = True)
    time = dbcol(dblong, nullable = False)

    employee = dbcol(db.ForeignKey(Employees.id), nullable = True)
    name = dbcol(dbstr(1024), nullable = True)
    organization = dbcol(dbstr(4096), nullable = True)

    symptoms = dbcol(dbbool, nullable = False)
    travel = dbcol(dbbool, nullable = False)
    contact = dbcol(dbbool, nullable = False)
    self_isolate = dbcol(dbbool, nullable = False) # intentionally null in the database, but not here, to perserve history
    covid_alert = dbcol(dbbool, nullable = False)
    test_results = dbcol(dbbool, nullable = False)

    __tablename__ = "form_responses"

db.create_all()
