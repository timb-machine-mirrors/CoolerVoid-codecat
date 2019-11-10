#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from .user_model import db, User
from . import user_controller 
from . import rule_controller
from . import engine_controller
from time import gmtime, strftime
import datetime
from flask_httpauth import HTTPTokenAuth,HTTPBasicAuth,MultiAuth

auth = HTTPBasicAuth()
auth_token = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(auth, auth_token) 

@auth.verify_password
def verify_password(username_or_token, password):
    return user_controller.test_password(username_or_token, password)

@auth_token.verify_token
def verify_token(username_or_token):
    return user_controller.test_token(username_or_token)

@app.route('/api/users', methods=['POST'])
def add_new_user():
    return user_controller.new_user()

@app.route('/api/token')
@multi_auth.login_required
def get_token():
    return user_controller.get_auth_token()

@app.route('/api/users/all')
@multi_auth.login_required
def list_table_of_users():
    return user_controller.List_table_users()

@app.route('/api/users/insert', methods=['POST'])
@multi_auth.login_required
def insert_user_in_table():
    return user_controller.insert_user()

@app.route('/api/users/view/<string:user_id>')
@multi_auth.login_required
def view_user_by_id(user_id):
    return user_controller.return_user(user_id)

@app.route('/api/users/delete', methods=['POST'])
@multi_auth.login_required
def delete_user_in_table():
    return user_controller.delete_user()

@app.route('/api/users/update', methods=['POST'])
@multi_auth.login_required
def update_user_in_table():
    return user_controller.update_user()


@app.route('/api/users/token2id', methods=['POST'])
@multi_auth.login_required
def token2id():
    return user_controller.get_token2id()



##=========== --->>> rules ROutes

@app.route('/api/rules/all')
@multi_auth.login_required
def list_table_of_rules():
    return rule_controller.List_table_rules()

@app.route('/api/rules/insert', methods=['POST'])
@multi_auth.login_required
def insert_rule_in_table():
    return rule_controller.insert_rule()

@app.route('/api/rules/view/<string:rule_id>')
@multi_auth.login_required
def view_rule_by_id(rule_id):
    return rule_controller.return_rule(rule_id)

@app.route('/api/rules/delete', methods=['POST'])
@multi_auth.login_required
def delete_rule_in_table():
    return rule_controller.delete_rule()

@app.route('/api/rules/update', methods=['POST'])
@multi_auth.login_required
def update_rule_in_table():
    return rule_controller.update_rule()

#### =============== >>>>> ENgine responses

@app.route('/api/engine/getsinks', methods=['POST'])
@multi_auth.login_required
def sink_table():
    return engine_controller.getsinks()

@app.route('/api/engine/allsinks', methods=['POST'])
@multi_auth.login_required
def sink_all():
    return engine_controller.all_sinks()

@app.route('/api/engine/clear', methods=['GET'])
@multi_auth.login_required
def clear_all():
    return engine_controller.clear_cache_all()

@app.route('/api/engine/list_cache', methods=['GET'])
@multi_auth.login_required
def cache_all():
    return engine_controller.list_table_cache()




