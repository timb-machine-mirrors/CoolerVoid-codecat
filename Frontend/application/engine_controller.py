#!/usr/bin/env python
import os
import flask
from flask import current_app as app
from flask import Flask, redirect, session, render_template, abort, request, flash, jsonify, g, url_for
from time import gmtime, strftime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from helper import tokenform
from helper import engine_rest_api 
import datetime
from . import user_controller

def open_code(request):
    path=request.form['path']
    lines=request.form['lines']
    lang=request.form['lang']
    if "c" in lang:
        lang="C"
    if "rb" in lang:
        lang="Ruby"
    if "py" in lang:
        lang="Python"
    if "cpp" in lang:
        lang="C++"
    if "go" in lang:
        lang="Go"
    if "pl"in lang:
        lang="Perl"
    if "java" in lang:
        lang="Java"
    if "php" in lang:
        lang="PHP"
    if "asp" in lang:
        lang="ASP"
    if "js" in lang:
        lang="Javascript"
    if "asm" in lang:
        lang="NASM"
    if "s" in lang:
        lang="NASM"
    if "swift" in lang:
        lang="Swift"
    #TODO improve validate here...
    if not os.path.isfile(path):
        return render_template('engine_forms/clear.html',title="File path not exist")
    code_content=""
    with open(path) as fp:
        content = fp.read()
        codes= ''.join(content)
    code_content=str(flask.Markup.escape(codes))
    info="<br><b>Path: "+path+"<br>Lines: "+lines+"</b><br>"
    highlight=info+'<pre class="line-numbers" data-line="'+lines+'"> <code class="language-'+lang+'">'+code_content+'</code></pre>'
    return render_template('engine_forms/code_view.html',title="Code view",code_highlight=highlight)


def clear_cache():
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    obj=engine_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    result=obj.clear_sinks()
    return render_template('engine_forms/clear.html',title="Wait two seconds to clear cache")

def list_cache_lines():
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    obj=engine_rest_api
    obj=obj.rest_call("","")
    obj.token=session['userkey']
    obj.list_sinks()
    result_array=[]
    for rows in obj.json_output:
        result_array.append(rows)
    return render_template('engine_forms/sink_list.html', elements=result_array,title="Cache of result")


def getsinks(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form):
        sink = TextField('sink:', validators=[validators.required(), validators.Length(min=1, max=1024)])
        path = TextField('path:', validators=[validators.required(), validators.Length(min=1, max=2048)])
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
                 d['lang']=request.form['lang']
                 d['sink']=request.form['sink']
                 d['path']=request.form['path']
                 obj=engine_rest_api
                 obj=obj.rest_call("","")
                 obj.token=session['userkey']
                 codes_lines=obj.getsinks(**d) 
                 flash("Wait five seconds and look the code cache")     
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('engine_forms/getsinks.html', form=form, title="Search sink")



def allsinks(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form):
        path = TextField('path:', validators=[validators.required(), validators.Length(min=1, max=2048)])
        lang = TextField('lang:', validators=[validators.required(), validators.Length(min=1, max=32)])
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
                 d['lang']=request.form['lang']
                 d['path']=request.form['path']
                 obj=engine_rest_api
                 obj=obj.rest_call("","")
                 obj.token=session['userkey']
                 codes_lines=obj.allsinks(**d)
                 flash("Wait five seconds and look the code cache")
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('engine_forms/allsinks.html', form=form, title="Search using all rules")


