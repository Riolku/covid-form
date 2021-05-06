from base64 import b64encode
from urllib.parse import urlencode

import flask, os, requests, jwt
from flask import json

from covid_form import app
from .config import conf_json

oauth_conf = conf_json['oauth']

org_guid = oauth_conf['org_guid']
client_id = oauth_conf['client_id']
redirect_uri = oauth_conf['redirect_uri']
oauth_domain = oauth_conf['oauth_domain']

cached_config = requests.get(f"https://login.microsoftonline.com/{org_guid}/v2.0/.well-known/openid-configuration").json()
jwk_client = jwt.PyJWKClient(cached_config['jwks_uri'])

def get_name_from_jwt(tk):
    return decode_jwt(tk)['name']

def get_oauth_uri():
    nonce = get_nonce()

    flask.session['nonce'] = nonce

    return f'https://login.microsoftonline.com/{org_guid}/oauth2/v2.0/authorize?' + urlencode(dict(
        client_id = client_id,
        response_type = "id_token",
        redirect_uri = redirect_uri,
        scope = "openid profile",
        nonce = nonce,
        response_mode = "form_post",
        domain_hint = oauth_domain
    ))

def get_nonce():
    return b64encode(os.urandom(16)).decode("utf-8")

def decode_jwt(tk):
    headers = jwt.get_unverified_header(tk)

    body = jwt.decode(
        tk,
        jwk_client.get_signing_key(headers['kid']).key,
        algorithms = [headers['alg']],
        audience = client_id
    )

    if body['nonce'] != flask.session['nonce']:
        raise RuntimeError("nonce mismatch")

    del flask.session['nonce']

    return body
