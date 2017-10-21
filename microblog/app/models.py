#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Xiaomi Inc. All rights reserved.
# @Date    : 17-10-20
# @Author  : meifeng@xiaomi.com

from app import db, app
import hashlib


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(40))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        hash_code = hashlib.md5(self.nickname.encode('utf-8')).hexdigest()
        app.logger.info('email:{}, hash:{}'.format(self.email, hash_code))
        return 'http://www.gravatar.com/avatar/{}?d=mm&s={}'\
            .format(hash_code, size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User {}>'.format(self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.String(120), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
