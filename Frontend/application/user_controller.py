#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, redirect, session, render_template, abort, request, flash, jsonify, g, url_for
from time import gmtime, strftime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from helper import tokenform
from helper import user_rest_api 
import datetime

def logof():
    session.pop('userkey', None)
    return redirect("front/auth")

def test_password(request):
    password=request.form['password']
    email=request.form['email']
    obj=user_rest_api
    obj=obj.rest_call(email,password)
    obj.Get_Token()
    session['userkey']=obj.token 
    return obj.test

def test_token(token):
    obj=user_rest_api
    obj=obj.rest_call("","")
    obj.Change_Token(token) 
    return obj.test


def check_auth():
    if session.get('userkey'):
        if test_token(session['userkey']) == True:
            return True
    session['userkey']=" "
    return False

def test_auth(request):
    if session.get('userkey'):
        if test_token(session['userkey']) == True:
            return True  
    if(test_password(request) == True ):
        return True
    else:
        return False

def show_index(request):
    if check_auth() == False:
        return redirect("front/auth")


    img='<img src="/static/codecat1.png" height="400" width="400" >'
    return render_template('AuthAdmin.html',title="Welcome to Codecat",content=img)

def show_auth(request):
    if session.get('userkey') == True:
        if test_token(session['userkey'])==True:
            img='<img src="/static/codecat1.png" height="400" width="400" >'
            return render_template('AuthAdmin.html',title="Welcome to Codecat",content=img)

    class TheForm(Form):
        email = TextField('email:', validators=[validators.required(), validators.Length(min=4, max=35)])
        password = TextField('password:', validators=[validators.required(), validators.Length(min=4, max=35)])

        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )
    if request.method == 'POST':
        token=request.form['csrf_token']
 
        if form.validate():
            if form.csrf_token.errors: 
                flash('Error: form token invalid try to post again')
                return render_template('login.html',form=form)
            if test_auth(request) == True:
                img='<img src="/static/codecat1.png" height="400" width="400" >'
                return render_template('AuthAdmin.html',title="Welcome to Codecat",content=img)
            flash('Error user or password not found !')
        else:
            flash('Error: All the form fields are required. ')
# token in  form.csrf_token 
    return render_template('login.html',form=form)


def home():
    if check_auth() == False:
        return redirect("front/auth")

    img='<br><center><img src="/static/img/mage3.gif" height="200" width="300" ></center>'
    return render_template('AuthAdmin.html',title="Welcome to CodeCat",image=img)






def List_table_users():
    
    if check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form): 
        name = TextField('id:', validators=[validators.required(), validators.Length(min=1, max=9)])

        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )

    obj=user_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    obj.List_Users()
    users=[]
    for rows in obj.json_output:
        users.append({"id": rows[0],"name": rows[1],"email": rows[2],"owner": rows[3],"date": rows[4]})
    return render_template('user_forms/user_list.html',form=form, users=users, title="Table of Users")



def insert_user(request):
    if check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form): 
        name = TextField('name:', validators=[validators.required(), validators.Length(min=4, max=35)])
        email = TextField('email:', validators=[validators.required(), validators.Length(min=4, max=35)])
        password = TextField('password:', validators=[validators.required(), validators.Length(min=4, max=35)]) 
        # owner = TextField('owner:', validators=[validators.required(), validators.Length(min=4, max=12)])
        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )

    if request.method == 'POST':
        token=request.form['csrf_token']
 
        if form.validate():
            if form.csrf_token.errors: 
                flash('Error: form token invalid try to post again')
            else:
                name=request.form['name']
                email=request.form['email']
                owner=request.form['owner']
                password=request.form['password']
                obj=user_rest_api
                obj=obj.rest_call("","")
                obj.token=session['userkey']
                handler=obj.Insert_User(email,name,password,owner)
                flash(str(handler))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('user_forms/user_insert.html', form=form, title="Insert User")



def delete_user(request):
    if check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form): 
        id = TextField('id:', validators=[validators.required(), validators.Length(min=1, max=64)])

        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )

    if request.method == 'POST':
        token=request.form['csrf_token']
 
        if form.validate():
            if form.csrf_token.errors: 
                flash('Error: form token invalid try to post again')
            else:
                id=request.form['id']
                obj=user_rest_api
                obj=obj.rest_call("","")
                obj.token=session['userkey']
                handler=obj.Delete_User(id)
                flash(str(handler))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('user_forms/user_delete.html', form=form, title="Delete User by ID")



def update_user(user_id):
    if check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form): 
        name = TextField('name:', validators=[validators.required(), validators.Length(min=4, max=35)])
        email = TextField('email:', validators=[validators.required(), validators.Length(min=4, max=35)])
        password = TextField('password:', validators=[validators.required(), validators.Length(min=4, max=35)]) 
        # owner = TextField('owner:', validators=[validators.required(), validators.Length(min=4, max=12)])
        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )
    
    if request.method == 'POST': 
#"csrf_token" in request.form:
        if len(str(user_id)) >=1 and len(request.form['csrf_token']) > 1 :
            token=request.form['csrf_token']
 
            if form.validate():
                if form.csrf_token.errors: 
                    flash('Error: form token invalid try to post again')
                else:
                    name=request.form['name']
                    email=request.form['email']
                    owner=request.form['owner']
                    password=request.form['password']
                    obj=user_rest_api
                    obj=obj.rest_call("","")
                    obj.token=session['userkey']
                    handler=obj.Update_User(str(user_id),email,name,password,owner)
                    flash(str(handler))
            else:
                flash('Error: All the form fields are required. ')
    obj=user_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    obj.Return_User_by_ID(str(user_id))
    users={}
    rows=[]
    rows= obj.json_output
    users={"id": str(rows[0]),"name": str(rows[1]),"email": str(rows[2]),"owner": str(rows[3]),"date": str(rows[4]) }
    return render_template('user_forms/user_update.html', form=form, users=users, title="Update data of user")



def my_update_user():
    if check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form): 
        name = TextField('name:', validators=[validators.required(), validators.Length(min=4, max=35)])
        email = TextField('email:', validators=[validators.required(), validators.Length(min=4, max=35)])
        password = TextField('password:', validators=[validators.required(), validators.Length(min=4, max=35)]) 
        # owner = TextField('owner:', validators=[validators.required(), validators.Length(min=4, max=12)])
        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )
    
    if request.method == 'POST': 
#"csrf_token" in request.form:
        if len(str(user_id)) >=1 and len(request.form['csrf_token']) > 1 :
            token=request.form['csrf_token']
 
            if form.validate():
                if form.csrf_token.errors: 
                    flash('Error: form token invalid try to post again')
                else:
                    name=request.form['name']
                    email=request.form['email']
                    owner=request.form['owner']
                    password=request.form['password']
                    obj=user_rest_api
                    obj=obj.rest_call("","")
                    obj.token=session['userkey']
                    handler=obj.Update_User(str(user_id),email,name,password,owner)
                    flash(str(handler))
            else:
                flash('Error: All the form fields are required. ')
    obj=user_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    user_id=obj.Token_to_id(session['userkey'])
    obj.Return_User_by_ID(str(user_id))
    users={}
    rows=[]
    rows= obj.json_output
    users={"id": str(rows[0]),"name": str(rows[1]),"email": str(rows[2]),"owner": str(rows[3]),"date": str(rows[4]) }
    return render_template('user_forms/user_update.html', form=form, users=users, title="Update your data")


