#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, redirect, session, render_template, abort, request, flash, jsonify, g, url_for
from time import gmtime, strftime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from helper import tokenform
from helper import rule_rest_api 
import datetime
from . import user_controller


def List_table_rules():
    class TheForm(Form): 
        rule = TextField('id:', validators=[validators.required(), validators.Length(min=1, max=32)])

        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )

    if user_controller.check_auth() == False:
        return redirect("front/auth")

    obj=rule_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    obj.List_rules()
    rules=[]
    for rows in obj.json_output:
        rules.append(rows)
    return render_template('rule_forms/rule_list.html',form=form, rules=rules, title="Table of rules")



def insert_rule(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form): 
        title = TextField('title:', validators=[validators.required(), validators.Length(min=3, max=1024)])
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
                try:
                 d={}
                 d['title']=request.form['title']
                 d['lang']=request.form['lang']
                 d['description']=request.form['description']
                 d['level']=request.form['level']
                 d['match1']=request.form['match1']
                 d['match2']=request.form['match2']
                 obj=rule_rest_api
                 obj=obj.rest_call("","")
                 obj.token=session['userkey']
                 handler=obj.Insert_rule(**d)
                 flash(str(handler))
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('rule_forms/rule_insert.html', form=form, title="Insert rule")



def delete_rule(request):
    if user_controller.check_auth() == False:
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
                obj=rule_rest_api
                obj=obj.rest_call("","")
                obj.token=session['userkey']
                handler=obj.Delete_rule(id)
                flash(str(handler))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('rule_forms/rule_delete.html', form=form, title="Delete rule by ID")


def update_rule(rule_id):

    if user_controller.check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form): 
        title = TextField('title:', validators=[validators.required(), validators.Length(min=6, max=512)])
        class Meta:
            csrf = True
            csrf_class = tokenform.Ice_CSRF

    form = TheForm(
      request.form,
      meta={'csrf_context': request.remote_addr }
    )
    
    if request.method == 'POST': 
#"csrf_token" in request.form:
        if len(str(rule_id)) >=1 and len(request.form['csrf_token']) > 1 :
            token=request.form['csrf_token']
 
            if form.validate():
                if form.csrf_token.errors: 
                    flash('Error: form token invalid try to post again')
                else:
                    d={}
                    d['id']=rule_id
                    d['title']=request.form['title']
                    d['lang']=request.form['lang']
                    d['description']=request.form['description']
                    d['level']=request.form['level']
                    d['match1']=request.form['match1']
                    d['match2']=request.form['match2']
                    obj=rule_rest_api
                    obj=obj.rest_call("","")
                    obj.token=session['userkey']
                    handler=obj.Update_rule(**d)
                    flash(str(handler))
            else:
                flash('Error: All the form fields are required. ')
    obj=rule_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    obj.Return_rule_by_ID(str(rule_id))
    rules={}
    rows=[]
    rows= obj.json_output
    rules=rows
    return render_template('rule_forms/rule_update.html', form=form, item=rules, title="Update data of rule")

