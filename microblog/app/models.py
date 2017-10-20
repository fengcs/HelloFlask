#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Xiaomi Inc. All rights reserved.
# @Date    : 17-10-20
# @Author  : meifeng@xiaomi.com

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.String(120), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
