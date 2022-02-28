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
from werkzeug.utils import secure_filename
import zipfile
import pathlib
import shutil

def get_true_path(path, follow_symlinks=True):
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return matchpath
                                        
def is_safe_path (path_in):
    true_path=str(get_true_path(path_in))
    block_dirs={"/usr/","/dev/","/var/","/lib/","/bin/","/boot/","/etc/"}
    # blocks /etc/passwd, /etc/shadow, /usr/serv/httpd ...
    for dir2block in block_dirs:
        if true_path.startswith(dir2block):
            return False
    return True

def open_code(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    path=request.form['path']
    if is_safe_path(path) == False:
        return redirect("front/auth")
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
        lang="javascript"
    if "asm" in lang:
        lang="NASM"
    if "s" in lang:
        lang="NASM"
    if "swift" in lang:
        lang="Swift"
    if "kt" in lang:
        lang="Java"
    if "dart" in lang:
        lanf="Java"
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
    return render_template('engine_forms/clear.html',title="Wait two seconds to clear Project results cache")

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
    return render_template('engine_forms/sink_list.html', elements=result_array,title="Results of project")


def getsinks(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form):
        sink = TextField('sink:', validators=[validators.required(), validators.Length(min=3, max=2024)])
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
                 d['path']=secure_filename(request.form['uploaded_source'])
                 if d['path'] == "None":
                     flash('Error: Please choice a project')    
                 d['lang']=request.form['lang']
                 d['sink']=request.form['sink']
                 obj=engine_rest_api
                 obj=obj.rest_call("","")
                 obj.token=session['userkey']
                 codes_lines=obj.getsinks(**d) 
                 flash("Wait five seconds and look the code cache")     
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    dir_list = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('engine_forms/getsinks.html', form=form, title="Search per sink",sources_dirs=dir_list,upload_path=app.config['UPLOAD_PATH'])



def allsinks(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")
    class TheForm(Form):
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
                 d['path']=secure_filename(request.form['uploaded_source'])
                 d['lang']=request.form['lang']
                 obj=engine_rest_api
                 obj=obj.rest_call("","")
                 obj.token=session['userkey']
                 codes_lines=obj.allsinks(**d)
                 flash("Wait five seconds and look the code cache")
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    dir_list = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('engine_forms/allsinks.html', form=form, title="Search using all rules",sources_dirs=dir_list,upload_path=app.config['UPLOAD_PATH'])



def upload_source(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form):
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
                 uploaded_file = request.files['file']
                 filename = secure_filename(uploaded_file.filename)
                 if filename != '':
                     file_ext = os.path.splitext(filename)[1]
                     if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                         flash("Extension not supported, just only ZIP files!")
                     path_full_name=os.path.join(app.config['UPLOAD_PATH'], filename)
                     uploaded_file.save(path_full_name)
                     zip_ref = zipfile.ZipFile( path_full_name, 'r')
                     zip_ref.extractall(app.config['UPLOAD_PATH'])
                     zip_ref.close()
                     os.remove(path_full_name)
                     flash("Source save!")
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    return render_template('engine_forms/uploadsource.html', form=form, title="Upload source code")



def remove_source(request):
    if user_controller.check_auth() == False:
        return redirect("front/auth")

    class TheForm(Form):
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
                 safe_path=secure_filename(request.form['path'])
                 allow_list = os.listdir(app.config['UPLOAD_PATH'])
                 for project in allow_list:
                     if project in safe_path:
                         path=app.config['UPLOAD_PATH']+"/"+safe_path
                         tmp = pathlib.Path(path)
                         shutil.rmtree(tmp)
                         flash("Project removed!")
                         break
                except Exception as e:
                 flash('Fail: '+ str(e))
        else:
            flash('Error: All the form fields are required. ')
    dir_list = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('engine_forms/remove_source.html', form=form, title="Remove a uploaded project by name",sources_dirs=dir_list)
