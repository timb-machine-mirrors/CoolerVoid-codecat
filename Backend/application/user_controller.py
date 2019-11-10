#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from .user_model import db, User
from time import gmtime, strftime
import datetime


def test_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def test_token(username_or_token):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def get_token2id():
    token = request.json.get('token')
    user=User.verify_auth_token(token)
    return str(user.id)


def new_user():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(login=username).first() is not None:
        abort(400)    
    current_time = datetime.datetime.now()
    user = User(login=username,mail=email,created_at=current_time)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return "True"


def get_auth_token():
    token = g.user.generate_auth_token(60000)
    return jsonify({'token': token.decode('ascii'), 'duration': 60000})


def List_table_users():
    users = User.query.all()
    Users_Array = []
    for user in users:
        line=[]
        line.append(user.id)
        line.append(user.login)
        line.append(user.mail)
        line.append(user.owner)
        line.append(user.created_at)
        Users_Array.append(line)
# to return all data     Users_Array.append(user.toDict()) 
    return jsonify(Users_Array)



# Insert User
def insert_user():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    permission = request.json.get('owner') # admin or user
    remote_ip = request.remote_addr
    current_time = datetime.datetime.now()
    # TODO Improve validation
    if username is None or password is None or email is None:
        abort(400)
    if User.query.filter_by(login=username).first() is not None:
        abort(400)    
    user = User(login=username,mail=email,owner=permission,last_ip=remote_ip,created_at=current_time,update_at=current_time)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return ("True")


# Return a user by ID
def return_user(user_id):
    input=str(user_id)
    user = User.query.filter_by(id=input).first()
    Users_Array=[]
#    Array.append(user.toDict()) 
    line=[]
    line.append(user.id)
    line.append(user.login)
    line.append(user.mail)
    line.append(user.owner)
    line.append(user.created_at)
    Users_Array.append(line)
# to return all data     Users_Array.append(user.toDict()) 
    return jsonify(Users_Array[0])
#    return jsonify(Array)


# Delete user by ID
def delete_user():
    input=request.json.get('id')
    if input is None:
        abort(400)
    user=User.query.filter_by(id=input).first()
    db.session.delete(user)
    db.session.commit()
    return "True"

# Update User
def update_user():
    d={}
    d['id'] = request.json.get('id')
    d['mail'] = request.json.get('email')
    d['login'] = request.json.get('username')
    password = request.json.get('password')
    d['owner'] = request.json.get('owner') # admin or user
    d['last_ip'] = request.remote_addr
    d['update_at']= datetime.datetime.now()
    # TODO Improve validation
    if d['login'] is None or password is None or d['mail'] is None:
        abort(400)
    user=User()
    user.hash_password(password)
    d['passhash']=user.passhash
    db.session.query(User).filter(User.id == d['id']).update(d) 
    # synchronize_session = False
    db.session.commit()
    return "True"

