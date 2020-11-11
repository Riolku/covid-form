from flask import request, flash, render_template, Flask

from flask_sqlalchemy import SQLAlchemy

import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = open("/srv/covid_form/database.pem").read()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

dbcol = db.Column
dbint = db.Integer
dbbool = db.Boolean
dblong = db.BigInteger
dbstr = db.String

class FormResponses(db.Model):
    id = dbcol(dbint, primary_key = True)
    time = dbcol(dblong, nullable = False)
    name = dbcol(dbstr(1024), nullable = False)
    organization = dbcol(dbstr(4096), nullable = False)

    symptoms = dbcol(dbbool, nullable = False)
    travel = dbcol(dbbool, nullable = False)
    contact = dbcol(dbbool, nullable = False)

    __tablename__ = "form_responses"

db.create_all()

def form_val(key):
    return request.form.get(key)

def check_form(key):
    return form_val(key) == 'on'

errcolour = "red accent-1"

@app.route("/", methods = ["GET", "POST"])
def serve():
    msg = ""
    colour = None
    status = None

    if request.method == "POST":
        error = False

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
            symptoms = check_form('symptoms')

            travel = check_form('travel')

            contact = check_form('contact')

            r = FormResponses(name = name, organization = organization, symptoms = symptoms, travel = travel, contact = contact, time = int(time.time()))

            db.session.add(r)
            db.session.commit()

            msg = "Your response was recorded successfully!"

            colour = "green accent-2"

            status = "success"

    return render_template("form.html", msg = msg, status = status, colour = colour)

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
