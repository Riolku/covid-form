from flask import Flask, json

app = Flask('covid_form')

CONF_DIR = "/srv/covid_form/"

conf_json = json.load(open(CONF_DIR + "conf.json"))

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = conf_json['database_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS = False,

    SESSION_COOKIE_HTTPONLY = False,
    SESSION_COOKIE_SAMESITE = 'None',
    SESSION_COOKIE_SECURE = True,
))

app.secret_key = conf_json['secret_key']

ext_url = conf_json['ext_url']

whitelisted_ip = conf_json['whitelisted_ip']
