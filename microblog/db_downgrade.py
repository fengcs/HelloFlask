#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Xiaomi Inc. All rights reserved.
# @Date    : 17-10-20
# @Author  : meifeng@xiaomi.com

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRAATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO, v-1)
print('Current database version:{}'.format(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO)))