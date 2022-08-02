# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os

MONGO_URL = 'mongodb://' + os.environ['MONGODB_HOSTNAME'] +':27017/'
SDA_DB_NAME = os.environ['MONGODB_DATABASE']
ENCRYPT_DB=False
SDA_COLL_NAME = "sda_docs"
POLICY_DB_NAME = "policy_db"
POLICY_COLL_NAME = "policy_docs"
SQL_DB_NAME = "user_db"
ADMIN_USER_NAME = os.environ['MONGODB_USERNAME']
ADMIN_USER_PW = os.environ['MONGODB_PASSWORD']