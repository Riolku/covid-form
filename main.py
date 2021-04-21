from flask import request, flash, render_template, Flask, Response

from flask_sqlalchemy import SQLAlchemy

import time

app = Flask(__name__)

CONF_DIR = "/srv/covid_form/"

app.config['SQLALCHEMY_DATABASE_URI'] = open(CONF_DIR + "database.pem").read()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

iframe = open(CONF_DIR + "iframe.txt").read()
ext_url = open(CONF_DIR + "url.txt").read()

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

def form_val(key):
    return request.form.get(key)

def check_form(key):
    return form_val(key) == 'on'

errcolour = "red accent-1"

def parse_form(name, employee, organization):
    msg = ""
    colour = None
    status = None

    symptoms = check_form('symptoms')
    travel = check_form('travel')
    contact = check_form('contact')
    self_isolate = check_form('self_isolate')
    covid_alert = check_form('covid_alert')
    test_results = check_form('test_results')

    r = FormResponses(name = name,
                        organization = organization,
                        employee = employee,

                        symptoms = symptoms,
                        travel = travel,
                        contact = contact,
                        self_isolate = self_isolate,
                        covid_alert = covid_alert,
                        test_results = test_results,

                        time = int(time.time()))

    db.session.add(r)
    db.session.commit()

    msg = "Your response was recorded successfully!"

    colour = "green accent-2"

    status = "success"

    return msg, colour, status


@app.route("/", methods = ["GET", "POST"])
def serve():
    msg = ""
    colour = None
    status = None

    if request.method == "POST":
        name = form_val('name')
        organization = form_val("organization")

        if not name.strip():
            msg = "Please enter your name!"
            colour = errcolour
            status = "error"

        if not organization.strip():
            msg = "Please enter your organization!"
            colour = errcolour
            status = "error"

        else:
            msg, colour, status = parse_form(name, None, organization)

    return render_template("form.html", msg = msg, status = status, colour = colour, iframe = iframe, ext_url = ext_url)

@app.route("/internal", methods = ['GET', 'POST'])
def serve_internal():
    msg = ""
    colour = None
    status = None

    if request.method == "POST":
        name = form_val('name')

        if not name.strip():
            msg = "Please select your name!"
            colour = errcolour
            status = "error"

        else:
            msg, colour, status = parse_form(None, int(name), None)

    employees = Employees.query.filter_by(active = True).order_by(Employees.name).all()

    return render_template("form.html", msg = msg, status = status, colour = colour, internal = True, iframe = iframe, ext_url = ext_url, employees = [(e.id, e.name) for e in employees])

imgresp = Response(open(CONF_DIR + "logo.png", "rb").read(), mimetype = "image/png")

@app.route("/logo")
def serve_logo():
    return imgresp


if __name__ == "__main__":
    app.run(port = 8000, debug = True)
