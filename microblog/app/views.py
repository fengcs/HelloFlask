import datetime

import flask
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from .forms import LoginForm, EditForm
from .models import User


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [
        {'author': {'nickname': 'Jhon'},
         'body': 'Beautiful day in Portland'},
        {'author': {'nickname': 'Susan'},
         'body': 'The Avengers movie was so cool!'}
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.info('username:{}, password:{}'.format(form.username.data, form.password.data))
        user = User.query.filter_by(nickname=form.username.data).first()
        app.logger.info('user :{}'.format(user))
        if user is None or form.password.data != '123':
            flash('Invalid login. Please try again')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# @lm.request_loader
# def request_loader(request):
#     id = request.form.get('id')
#     user = User.query.get(int(id))
#     if user is None:
#         return
#
#     user.is_authenticated = request.form['email'] == user['email']
#     return user



@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['get', 'post'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@lm.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
