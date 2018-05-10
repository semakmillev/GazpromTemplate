# -*- coding: utf-8 -*-
import json

from flask import jsonify, request
from dblite import consts
from app import app
from dblite import session, create, people





@app.route("/company/<session_id>/<role>")
def get_admin_companies(session_id, role):
    user_id = session.get_user_id(session_id)
    user_role = None if role == "user" else role
    res = {}
    res['companies'] = people.get_user_items(consts.SQL_GET_USER_COMPANIES, user_id, user_role)
    return jsonify(res)


@app.route("/brand/<session_id>/<role>")
def get_admin_brands(session_id, role):
    company_id = request.args.get('company_id')
    user_id = session.get_user_id(session_id)
    user_role = None if role == "user" else role
    res = {}
    if company_id != None:
        print company_id
    res['brands'] = people.get_user_items(consts.SQL_GET_USER_BRANDS, user_id, user_role)
    return jsonify(res)


@app.route("/template/<session_id>/<role>")
def get_admin_templates(session_id, role):
    user_id = session.get_user_id(session_id)
    user_role = None if role == "user" else role
    res = {}
    res['templates'] = people.get_user_items(consts.SQL_GET_USER_TEMPLATES, user_id, user_role)
    return jsonify(res)


@app.route("/test/")
def test():
    return "!"
