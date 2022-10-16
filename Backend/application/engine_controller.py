#!/usr/bin/env python
# anti REDOS library https://github.com/google/re2
try:
    import re2 as re
except ImportError:
    import re

import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from . rule_model import db, Rules
from . engine_model import db, Engine
from time import gmtime, strftime
import datetime
import socket
from sqlalchemy import exc
from werkzeug.utils import secure_filename

def get_true_path(path, follow_symlinks=True):
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return matchpath
                                        
def is_safe_path (path_in):
    true_path=str(get_true_path(path_in))
    clear_list={"..","\\","./","...","%2e","%252e","%c0%ae","%uff0e","..%5c","%255c","%","%252f"}
    block_dirs={"/usr/","/dev/","/var/","/lib/","/bin/","/boot/","/etc/"}
    # blocks /etc/passwd, /etc/shadow, /usr/serv/httpd ...
    for dir2block in block_dirs:
        if true_path.startswith(dir2block):
            return False
    for n in clear_list:
        if n in path_in:
            return False
    return True


def find_extension_by_lang(lang):
    if "ruby" in lang:
        lang="rb"
    if "javascript" in lang:
        lang="js"     
    if "python" in lang:
        lang="py"
    if "all_langs" in lang:
        lang="*"
    if "csharp" in lang:
        lang="cs"
    return lang

def list_table_cache():
    try:
     Engine.to_dict = Engine.to_dict
     elements = Engine.query.all()
     Cache_Array = []

     for item in elements:
        line={}
        line["rule_id"]=str(item.rule_id)
        line["title"]=str(item.title)
        line["path"]=str(item.path)
        line["lines"]=str(item.lines)
        line["risk"]=str(item.risk)
        line["lang"]=str(item.lang)
        Cache_Array.append(line)
     return jsonify(Cache_Array)
    except exc.SQLAlchemyError as e:
     print(e)
     return "Error"

def clear_cache_all():
    try:
        total = db.session.query(Engine).delete()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        total=0
        db.session.rollback()
    return jsonify(total)

def test_match_regex(filepath,regex1,regex2):
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       return "Path error: "+filepath+"\n"

   with open(filepath,encoding='utf-8', errors='ignore') as fp:
       cnt = 1
       match_lines=" "
       for line in fp:
           try:
               if re.search(regex1, line): #, re.M|re.I):
                   if len(regex2) > 1:
                       if re.search(regex2, line): # re.M|re.I):
                           match_lines+=str(cnt)+","
                   else:
                       match_lines+=str(cnt)+","
               cnt += 1
           except:
               print("Regex rule error: "+regex1 +" "+regex2)
               return 0        
   if len(match_lines) > 1:
       return match_lines[:-1]


def search_sinks(directory, extension,sink):
    total=0
    extension = extension.lower()
    lang_db = extension
    extension= find_extension_by_lang(lang_db)
    if sink  != 0:
        risk="Warning"
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if (extension and name.lower().endswith(extension)) or ("*" in extension ) :
                current_path=os.path.join(dirpath, name)
                Rules.to_dict = Rules.to_dict
                try:
                 elements = Rules.query.filter_by(lang=lang_db) 
                 for item in elements:
                    if sink == 0:
                        regex1=item.match1
                        regex2=item.match2
                        rule=item.title
                        rule_id=item.id
                        if sink != 0:
                            risk=item.level
                        else:
                            risk="Warning"
                        lines=test_match_regex(current_path,regex1,regex2)
                    else:
                        lines=test_match_regex(current_path,sink,"0")

                    if lines:
                        if len(lines)>1:
                            element={}
                            element['lines']=lines
                            element['path']=current_path
                            element['lang']=extension
                            element['risk']=risk
                            if sink == 0:
                                element['rule_id']=rule_id
                                element['title']=rule
                            else:    
                                element['rule_id']="Custom"
                                element['title']="Search sink \""+str(sink)+"\""
                            code_sink = Engine(**element)
                            db.session.add(code_sink)
                            db.session.commit()
                            total+=1
                    lines=0
                except exc.SQLAlchemyError as e:
                    print(e)
                    return "Error"
    return total

def getsinks():
    lang = request.json.get('lang')
    path = app.config['UPLOAD_PATH']+"/"+secure_filename(request.json.get('path'))
    sink = request.json.get('sink')
    if is_safe_path(request.json.get('path')) == False:
        return "Error in path"
    result=search_sinks(path,lang,sink)
    return ("True")

def all_sinks():
    lang = request.json.get('lang')
    path = app.config['UPLOAD_PATH']+"/"+secure_filename(request.json.get('path'))
    if is_safe_path(request.json.get('path')) == False:
        return "Error in path"
    result=search_sinks(path,lang,0)
    return ("True")

