#!/usr/bin/env python
import re
import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from . rule_model import db, Rules
from . engine_model import db, Engine
from time import gmtime, strftime
import datetime
import socket


def find_extension_by_lang(lang):
    if "ruby" in lang:
        lang="rb"
    if "javascript" in lang:
        lang="js"     
    if "python" in lang:
        lang="py"
    return lang

def list_table_cache():
    Engine.to_dict = Engine.to_dict
    elements = Engine.query.all()
    Cache_Array = []

    for item in elements:
        line={}
        line["rule_id"]=str(item.rule_id)
        line["title"]=str(item.title)
        line["path"]=str(item.path)
        line["lines"]=str(item.lines)
        line["lang"]=str(item.lang)
        Cache_Array.append(line)
    return jsonify(Cache_Array)

def clear_cache_all():
    try:
        total = db.session.query(Engine).delete()
        db.session.commit()
    except:
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
           if re.search(regex1, line, re.M|re.I):
               if len(regex2) > 1:
                   if re.search(regex2, line, re.M|re.I):
                       match_lines+=str(cnt)+","
               else:
                   match_lines+=str(cnt)+","
           cnt += 1
   if len(match_lines) > 1:
       return match_lines[:-1]


def search_sinks(directory, extension,sink):
    total=0
    extension = extension.lower()
    lang_db = extension
    extension= find_extension_by_lang(lang_db)
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if extension and name.lower().endswith(extension):
                current_path=os.path.join(dirpath, name)
                Rules.to_dict = Rules.to_dict
                elements = Rules.query.filter_by(lang=lang_db) 
                for item in elements:
                    if sink == 0:
                        regex1=item.match1
                        regex2=item.match2
                        rule=item.title
                        rule_id=item.id
                        lines=test_match_regex(current_path,regex1,regex2)
                    else:
                        lines=test_match_regex(current_path,sink,"0")

                    if lines:
                        if len(lines)>1:
                            element={}
                            element['lines']=lines
                            element['path']=current_path
                            element['lang']=extension
                            if sink == 0:
                                element['rule_id']=rule_id
                                element['title']=rule
                               
                            code_sink = Engine(**element)
                            db.session.add(code_sink)
                            db.session.commit()
                            total+=1
                    lines=0
    return total

def getsinks():
    lang = request.json.get('lang')
    path = request.json.get('path')
    sink = request.json.get('sink')
    result=search_sinks(path,lang,sink)
    return ("True")

def all_sinks():
    lang = request.json.get('lang')
    path = request.json.get('path')
    result=search_sinks(path,lang,0)
    return ("True")

