import os

from flask import Flask, jsonify
from flask import url_for

from dotenv import load_dotenv
load_dotenv()

import requests

from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['LICHESS_CLIENT_ID'] =  os.getenv("LICHESS_CLIENT_ID")
app.config['LICHESS_CLIENT_SECRET'] = os.getenv("LICHESS_CLIENT_SECRET")
app.config['LICHESS_ACCESS_TOKEN_URL'] = 'https://oauth.lichess.org/oauth'
app.config['LICHESS_AUTHORIZE_URL'] = 'https://oauth.lichess.org/oauth/authorize'

oauth = OAuth(app)
oauth.register('lichess')

@app.route('/')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.lichess.authorize_access_token()
    bearer = token['access_token']
    headers = {'Authorization': f'Bearer {bearer}'}
    response = requests.get("https://lichess.org/api/account", headers=headers)
    return jsonify(**response.json())

if __name__ == '__main__':
    app.run()
