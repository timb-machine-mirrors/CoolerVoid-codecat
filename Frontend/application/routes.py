#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from . import user_controller 
from . import rule_controller
from . import engine_controller


from time import gmtime, strftime
import datetime

##### ACL / AUTH

@app.route('/health')
def health():
        return user_controller.get_health()

def verify_pass(request):
    return user_controller.test_password(request)

def verify_token(request):
    return user_controller.test_token(request)

@app.route('/front/auth/', methods=['POST','GET'])
def show_auth():
    return user_controller.show_auth(request)

@app.route('/front/auth/logof', methods=['GET'])
def logof_auth():
    return user_controller.logof()

@app.route('/front/auth/admin', methods=['POST'])
def welcome_admin():
    user_controller.test_auth()
    return user_controller.show_admin()

@app.route('/front/auth/token')
def get_token():
    return user_controller.get_auth_token()

#### CRUD User
@app.route('/front/auth/users/index.html', methods=['GET'])
def show_index_start():
    return user_controller.show_index(request)

@app.route('/front/auth/users/list', methods=['GET'])
def list_table_of_users():
    return user_controller.List_table_users()

@app.route('/front/auth/users/insert', methods=['GET','POST'])
def insert_user_in_table():
    return user_controller.insert_user(request)

@app.route('/front/auth/users/delete', methods=['POST','GET'])
def delete_user_in_table():
    return user_controller.delete_user(request)

@app.route('/front/auth/users/update/<string:user_id>', methods=['POST','GET'])
def update_user_in_table(user_id):
    return user_controller.update_user(user_id)

@app.route('/front/auth/users/my_update/', methods=['POST','GET'])
def my_update_user_in_table():
    return user_controller.my_update_user()


############-----> CRUD rules
@app.route('/front/auth/rules/list', methods=['GET'])
def list_table_of_rules():
    return rule_controller.List_table_rules()

@app.route('/front/auth/rules/insert', methods=['GET','POST'])
def insert_rule_in_table():
    return rule_controller.insert_rule(request)

@app.route('/front/auth/rules/delete', methods=['POST','GET'])
def delete_rule_in_table():
    return rule_controller.delete_rule(request)

@app.route('/front/auth/rules/update/<string:rule_id>', methods=['POST','GET'])
def update_rule_in_table(rule_id):
    return rule_controller.update_rule(rule_id)


### home
@app.route('/front/auth/welcome', methods=['GET','POST'])
def welcome():
    return user_controller.home()

######========================    Engine
@app.route('/front/auth/engine/getsinks', methods=['GET','POST'])
def getsinks_option():
    return engine_controller.getsinks(request)

@app.route('/front/auth/engine/allsinks', methods=['GET','POST'])
def allsinks_option():
    return engine_controller.allsinks(request)

@app.route('/front/auth/engine/list_cache', methods=['GET'])
def cachesinks():
    return engine_controller.list_cache_lines()

@app.route('/front/auth/engine/clear', methods=['GET'])
def clear_all_sinks():
    return engine_controller.clear_cache()

@app.route('/front/auth/engine/open_code', methods=['POST'])
def show_code():
    return engine_controller.open_code(request)

@app.route('/front/auth/engine/uploadsource', methods=['GET','POST'])
def upload_file():
    return engine_controller.upload_source(request)

@app.route('/front/auth/engine/remove_source', methods=['GET','POST'])
def remove_file():
    return engine_controller.remove_source(request)
