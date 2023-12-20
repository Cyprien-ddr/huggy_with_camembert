#!/usr/bin/env python3
import sys 
import os
import re
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../"))
from main import main

app = Flask(__name__)

@app.template_filter('replace_regexp')
def replace_regexp(s, find, replace):
    return re.sub(find, replace, s)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user_question = request.form['question']
        hat, result = main(user_question)
        return render_template('huggy.html', hat=hat, result=result, question=user_question)
    return render_template('huggy.html')


@app.route('/api', methods=['GET'])
def question():
    user_question = request.args.get('question')
    if user_question is None:
        return jsonify("Please ask me a question")
    answer = main(user_question)
    return "answer : " + answer


if __name__ == "__main__":
    app.run(debug=True, port=3006)
