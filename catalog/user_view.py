#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 18:27:36 2022

@author: dineshverma
"""

from flask import Blueprint, current_app, request, flash, render_template



from catalog.sql_db import UserEntry, UserSQLDBase
from catalog.errors import MissingArgumentException, DuplicateEntryException
from catalog.errors import WebException, MissingIdentity, ItemNotFound

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')
user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/user')

ID_TERM = "_id"
USER_DB = "SQL_DB"

def _initialize_user_views(app):
    app.register_blueprint(user_blueprint)
    initialize_user_db(app)
    
    
def initialize_user_db(app):
    user_url = app.config["SQL_DB_NAME"]
    app.config[USER_DB] = UserSQLDBase(user_url)
    

def get_user_db():
    answer = current_app.config.get(USER_DB, None)
    if answer is None: 
        initialize_user_db(current_app)
        answer = current_app.config[USER_DB]
    return answer


#User Management functions 
#All user management is done through the add, remove, list and update interfaces


@user_blueprint.route("/add", methods=['POST'])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        db = get_user_db()

        if not name:
            raise WebException(MissingArgumentException("name", "User"))
        elif not password:
            raise WebException(MissingArgumentException("password", "User"))
        elif not email:
            raise WebException(MissingArgumentException("email", "User"))
            
        #Check if user already exists 
        existing_users = db.search("name", name)
        if len(existing_users) > 0:
            raise WebException(DuplicateEntryException("User", "name", name ))


        user = UserEntry(-1, name, password, email)
        db.create(user)
        return render_template("user/index.html")
            
    
@user_blueprint.route("/remove", methods=['POST'])
def retrieve_request():
    if request.method == "POST":
        name = request.form["name"]
        db = get_user_db()
        error = None
        
        if not name:
            error = "User name is required."
            
        existing_users = db.search("name", name)
        if len(existing_users) == 0:
            error = "No such User"
        if error is None:
            for user in existing_users:
                db.delete(user._id)
        else:
            flash(error)
            
@user_blueprint.route("/list", methods=['GET', 'POST'])
def list_request():
    db = get_user_db()
    users = db.get_all()
    return render_template("user/list.html", users = users)

@user_blueprint.route("/index", methods=['GET', 'POST'])
def index_request():
    return render_template("user/index.html")

@user_blueprint.route("/add_page", methods=['GET', 'POST'])
def add_page_request():
    return render_template("user/add.html")

@user_blueprint.route("/remove", methods=['GET'])
def del_request():
    if request.method == "GET":
        print(request.args.keys())
        identity = request.args.get('id')
        int_id = -1
        if identity is None:
            raise WebException(MissingIdentity("remove"))
        try:
            int_id = int(identity)
        except ValueError:
            raise WebException(message="Identity should be an integer", code=500)
        db = get_user_db()
        user = db.retrieve(int_id)
        if user is None:
            raise WebException(ItemNotFound(identity))
        db.delete(int_id)
        return render_template("user/list.html", users = db.get_all())
        

@user_blueprint.route("/test", methods=['GET', 'POST'])
def test_request():
    return render_template("base.html")
    
    
    

    