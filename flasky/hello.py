#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Custom. All rights reserved.
# @Date    : 2017/10/21
# @Author  : meifengcs@outlook.com

from datetime import datetime
import os
from threading import Thread

import flask
from flask import Flask, request
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
import wtforms

basedir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # response = flask.make_response('<h1>Bad Request</h1>')
    # response.set_cookie('anwser', '42')

    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            flask.session['konwn'] = False
        else:
            flask.session['konwn'] = True

        flask.session['name'] = form.name.data
        form.name.data = ''
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('index.html',
                                 form=form,
                                 name=flask.session.get('name'),
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


class NameForm(FlaskForm):
    name = wtforms.StringField('What is your name?', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Role {}>'.format(self.username)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = flask.render_template(template + '.txt', **kwargs)

    # msg.html = flask.render_tempalte(template + '.html', **kwargs)

    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread


manager.add_command('shell', Shell(make_context=make_shell_context))
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
