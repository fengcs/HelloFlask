#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Custom. All rights reserved.
# @Date    : 2017/10/21
# @Author  : meifengcs@outlook.com

from datetime import datetime

import flask
from flask import Flask, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import wtforms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    response = flask.make_response('<h1>Bad Request</h1>')
    response.set_cookie('anwser', '42')
    return flask.render_template('index.html',
                                 current_time=datetime.now())


@app.route('/user/<name>')
def user(name):
    return flask.render_template('user.html')


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return flask.render_template('500.html'), 500


def NameForm(FlaskForm):
    name = wtforms.StringField('What is your name?', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
