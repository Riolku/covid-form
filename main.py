from flask import request, flash, render_template, Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = open("/srv/covid_form/database.pem").read()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

symptoms = dict(
    fever = "Fever or chills",
    breathing = "Difficulty breathing or shortness of breath",
    cough = "Cough",
    throat = " Sore throat, trouble swallowing ",
    nose = " Runny nose/stuffy nose or nasal congestion ",
    taste = " Decrease or loss of smell or taste ",
    nausea = " Nausea, vomiting, diarrhea, abdominal pain ",
    tired = " Not feeling well, extreme tiredness, sore muscles "
)

dbcol = db.Column
dbint = db.Integer
dbbool = db.Boolean
dblong = db.BigInteger
dbstr = db.String

class Organizations(db.Model):
    id = dbcol(dbint, primary_key = True)
    key = dbcol(dbstr(128), unique = True)
    name = dbcol(dbstr(1024), unique = True)

    __tablename__ = "organizations"

class FormResponses(db.Model):
    id = dbcol(dbint, primary_key = True)
    time = dbcol(dblong, nullable = False)
    name = dbcol(dbstr(128), nullable = False)
    organization = dbcol(dbint, db.ForeignKey(Organizations.id), nullable = True)
    
    for k in symptoms:
        vars()[k] = dbcol(dbbool, nullable = False)

    travel = dbcol(dbbool, nullable = False)
    contact = dbcol(dbbool, nullable = False)

    __tablename__ = "form_responses"

db.create_all()

def form_val(key):
    return request.form.get(key)

def check_form(key):
    return form_val(key) == 'on'

@app.route("/", methods = ["GET", "POST"])
def serve():
    if request.method == "POST":
        name = form_val('name')

        organization = form_val('organization')

        form_type = form_val('form_type')

        symptom_vals = { v : check_form(v) for v in symptoms.keys() }

        travel = check_form('travel')

        contact = check_form('contact')

        print(form_type, name, organization, symptom_vals, travel, contact)


    return render_template("form.html", dd = [
        ("a", "C. A"),
        ("b", "C. B"),
        ("c", "C. C")
    ], symptoms = symptoms)

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
