from flask import request, flash, render_template, Flask

app = Flask(__name__)

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
