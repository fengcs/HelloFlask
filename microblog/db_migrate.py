#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) 2017, Xiaomi Inc. All rights reserved.
# @Date    : 17-10-20
# @Author  : meifeng@xiaomi.com

import types
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRAATE_REPO

migration = SQLALCHEMY_MIGRAATE_REPO + '/version/%03d_migration.py'.format(
    api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO) + 1)

tmp_module = types.ModuleType('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO)
eval(old_model in tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO, tmp_module.meta,
                                          db.metadata)
print('New migration saved as  ' + migration)
print('Current database version:' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRAATE_REPO)))
