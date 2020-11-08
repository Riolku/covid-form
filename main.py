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

class Organizations(db.Model):
    id = dbcol(dbint, primary_key = True)
    key = dbcol(dbstr(128), unique = True)
    name = dbcol(dbstr(1024), unique = True)

class FormResponses(db.Model):
    id = dbcol(dbint, primary_key = True)
    time = dbcol(dblong, nullable = False)
    name = dbcol(dbstr(128), nullable = False)
    organization = dbcol(dbint, db.ForeignKey(Organizations.id), nullable = True)
    
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

        if not name.strip():
            msg = "Please enter your name!"
            colour = errcolour
            status = "error"
        else:

            organization = form_val('organization')

            form_type = form_val('form_type')

            symptoms = form_val('symptoms')

            travel = check_form('travel')

            contact = check_form('contact')

            oid = None
            if form_type == "external":
                o = Organizations.query.filter_by(key = organization).first()
        
                if o is None:
                    msg = "No such organization!"
                    colour = errcolour
                    status = "error"

                else:
                    oid = o.id

            if status is None:

                r = FormResponses(name = name, organization = oid, symptoms = symptoms, travel = travel, contact = contact, time = int(time.time()))

                db.session.add(r)

                db.session.commit()

                msg = "Your response was recorded successfully!"

                colour = "green accent-2"
            
                status = "success"


    return render_template("form.html", msg = msg, status = status, colour = colour, dd = [(o.key, o.name) for o in Organizations.query.all()])

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
