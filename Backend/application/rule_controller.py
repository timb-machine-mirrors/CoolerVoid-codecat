#!/usr/bin/env python
import os
from flask import current_app as app
from flask import Flask, abort, request, jsonify, g, url_for
from . rule_model import db, Rules
from time import gmtime, strftime
import datetime
import socket

def List_table_rules():
    Rules.to_dict = Rules.to_dict
    elements = Rules.query.all()
    Rules_Array = []

    for item in elements:
        line={}
        line["id"]=str(item.id)
        line["lang"]=str(item.lang)
        line["title"]=str(item.title)
        line["level"]=str(item.level)
        line["created_at"]=str(item.created_at)
        Rules_Array.append(line)
    return jsonify(Rules_Array)



def insert_rule():
    d={}
    d['lang']= request.json.get('lang')
    d['title'] = request.json.get('title')
    d['description']= request.json.get('description')
    d['level'] = request.json.get('level')
    d['match1']= request.json.get('match1')
    d['match2'] = request.json.get('match2')
    d['created_at'] = datetime.datetime.now()
    # TODO Improve validation
    if d['lang'] is None:
        abort(400)
    url = Rules(**d)
    db.session.add(url)
    db.session.commit()
    return ("True")


def return_rule(Rules_id):
    input=str(Rules_id)
    item = Rules.query.filter_by(id=input).first()
    #Rules.append(Rules.toDict()) 
    Rules_Array=[]
    line={}
    line['id']=str(item.id)
    line['lang']=str(item.lang)
    line['title']=str(item.title)
    line['description']=str(item.description)
    line['level']=str(item.level)
    line['match1']=str(item.match1)
    line['match2']=str(item.match2)
    line['update_at']=str(item.update_at)
    line['created_t']=str(item.created_at)
    Rules_Array.append(line)
    return jsonify(Rules_Array[0])


def delete_rule():
    input=request.json.get('id')
    if input is None:
        abort(400)   
    url = Rules.query.filter_by(id=input).first()
    db.session.delete(url)
    db.session.commit()
    return "True"

def update_rule():
    d={}
    id = request.json.get('id')
    if request.json.get('lang') is not None:
        d['lang'] = request.json.get('lang')

    if request.json.get('title') is not None:
        d['title'] = request.json.get('title')

    if request.json.get('description') is not None:
        d['description'] = request.json.get('description') 

    if request.json.get('level') is not None:
        d['level'] = request.json.get('level')

    if request.json.get('match1') is not None:
        d['match1'] = request.json.get('match1')

    if request.json.get('match2') is not None:
        d['match2'] = request.json.get('match2') 

    d['update_at']=datetime.datetime.now()
    url=Rules()
    db.session.query(Rules).filter(Rules.id == id).update(d) 
    db.session.flush()
    result= db.session.commit()
    return "True"





