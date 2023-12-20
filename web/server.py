#!/usr/bin/env python3
import sys
import os
import re
from flask import Flask, request, render_template, jsonify, redirect, session
import google_auth_oauthlib.flow
import requests
from functools import wraps

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../"))

from main import main
from data_source.mysql import get_data
from init_model import init_model

vector_store = init_model(get_data())

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.template_filter('replace_regexp')
def replace_regexp(s, find, replace):
    return re.sub(find, replace, s)

# OAuth2 Configuration
CLIENT_SECRETS_FILE = './.client.json'
SCOPES = ['openid', 'email', 'profile']
REDIRECT_URI = 'https://huggy-ai.insign.agency/'

def create_oauth_flow():
    return google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def is_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect('/login')

        credentials = flow.credentials
        if not credentials.valid:
            return redirect('/login')

        return func(*args, **kwargs)
    return decorated_function

def login():
    flow = create_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return authorization_url, state

@app.route('/login')
def login_route():
    authorization_url, state = login()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = create_oauth_flow()
    flow.fetch_token(authorization_response=request.url)

    # Fetch user info
    credentials = flow.credentials
    userinfo_response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': f'Bearer {credentials.token}'})
    user_info = userinfo_response.json()

    # Store user info in session or database as needed
    session['user_info'] = user_info
    print(session['user_info'])
    return redirect('/')  # Redirect to the home page or a dashboard

@app.route('/', methods=['GET', 'POST'])
@is_auth
def form():
    if request.method == 'POST':
        user_question = request.form['question']
        result = main(user_question, vector_store)
        return render_template('huggy.html', result=result, question=user_question)
    return render_template('huggy.html')


@app.route('/api', methods=['GET'])
@is_auth
def question():
    user_question = request.args.get('question')
    if user_question is None:
        return jsonify("Please ask me a question")
    answer = main(user_question, vector_store)
    return "answer : " + answer


if __name__ == "__main__":
    app.run(debug=True, port=3006)