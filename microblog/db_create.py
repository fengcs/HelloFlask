#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Xiaomi Inc. All rights reserved.
# @Date    : 17-10-20
# @Author  : meifeng@xiaomi.com

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRAATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRAATE_REPO):
    api.create(SQLALCHEMY_MIGRAATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO, api.version(SQLALCHEMY_MIGRAATE_REPO))