import time, flask

from flask import request, flash, render_template, Response, redirect, json

from covid_form import app

from .db import db, Employees, FormResponses
from .config import CONF_DIR, ext_url, whitelisted_ip
from .oauth import get_oauth_uri, get_name_from_jwt


def form_val(key):
    return request.form.get(key)


def check_form(key):
    return form_val(key) == "on"


errcolour = "red accent-1"


def parse_form(name, employee, organization):
    msg = ""
    colour = None
    status = None

    symptoms = check_form("symptoms")
    travel = check_form("travel")
    contact = check_form("contact")
    self_isolate = check_form("self_isolate")
    covid_alert = check_form("covid_alert")
    test_results = check_form("test_results")

    r = FormResponses(
        name=name,
        organization=organization,
        employee=employee,
        symptoms=symptoms,
        travel=travel,
        contact=contact,
        self_isolate=self_isolate,
        covid_alert=covid_alert,
        test_results=test_results,
        time=int(time.time()),
    )

    db.session.add(r)
    db.session.commit()

    msg = "Your response was recorded successfully!"

    colour = "green accent-2"

    status = "success"

    return msg, colour, status


@app.route("/", methods=["GET", "POST"])
def serve():
    msg = ""
    colour = None
    status = None

    if "name" in flask.session:
        del flask.session["name"]

    if request.method == "POST":
        name = form_val("name")
        organization = form_val("organization")

        if name is None or not name.strip():
            msg = "Please enter your name!"
            colour = errcolour
            status = "error"

        elif organization is None or not organization.strip():
            msg = "Please enter your organization!"
            colour = errcolour
            status = "error"

        else:
            msg, colour, status = parse_form(name, None, organization)

    return render_template(
        "form.html", msg=msg, status=status, colour=colour, ext_url=ext_url
    )


@app.route("/internal", methods=["GET", "POST"])
def serve_internal():
    if flask.session.get("name") is None and request.remote_addr != whitelisted_ip:
        return redirect(get_oauth_uri(), code=303)

    msg = ""
    colour = None
    status = None

    if request.method == "POST":
        name = form_val("name")

        if not name.strip():
            msg = "Please select your name!"
            colour = errcolour
            status = "error"

        else:
            flask.session["name"] = Employees.query.filter_by(id=int(name)).first().name

            msg, colour, status = parse_form(None, int(name), None)

    employees = Employees.query.filter_by(active=True).order_by(Employees.name).all()

    name = flask.session.get("name", None)

    has_name = Employees.query.filter_by(name=name).first() is not None

    return render_template(
        "form.html",
        msg=msg,
        status=status,
        colour=colour,
        internal=True,
        ext_url=ext_url,
        employees=[(e.id, e.name) for e in employees],
        selected_name=name,
        has_name=has_name,
    )


@app.route("/authorize", methods=["POST"])
def serve_authorization():
    name = get_name_from_jwt(request.form["id_token"])

    flask.session["name"] = name

    return redirect("/internal", code=303)


imgresp = Response(open(CONF_DIR + "logo.png", "rb").read(), mimetype="image/png")


@app.route("/logo")
def serve_logo():
    return imgresp
