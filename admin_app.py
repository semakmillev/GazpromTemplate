# -*- coding: utf-8 -*-
import json
import os
import shutil

from flask import jsonify, request
from dblite import consts
from app import app
from dblite import session, create, people, template, rules


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


@app.route("/template/<session_id>/<role>", methods=['GET'])
def get_admin_templates(session_id, role):
    user_id = session.get_user_id(session_id)
    user_role = None if role == "user" else role
    res = {}
    res['templates'] = people.get_user_items(consts.SQL_GET_USER_TEMPLATES, user_id, user_role)
    return jsonify(res)


@app.route("/template/add/<session_id>", methods=['POST'])
def add_template(session_id):
    user_id = session.get_user_id(session_id)
    brand_id = request.args.get('brand_id')
    if brand_id == None:
        return 500, 'Empty brand!'
    user_brands = people.get_user_items("select * from (" + consts.SQL_GET_USER_BRANDS + ") where ID = :brand_id",
                                        user_id, None, brand_id=brand_id)
    if len(user_brands) == 0:
        return 500, 'Access denied!'
    params = json.loads(request.data)
    template_name = params["template_name"]

    path = "company_%03d" % user_brands[0]["COMPANY_ID"] + "/brand_%04d" % int(brand_id)
    path = path + "/" + template_name
    main_path = os.path.abspath(os.path.dirname(__file__)) + "/templates/"
    directory = main_path + path

    print directory
    if not os.path.exists(directory):
        print "!!!"
        os.makedirs(directory)
        shutil.copyfile(main_path + "empty_template.py", main_path + path + "/template.py")
        f = file(main_path + path + "/__init__.py", 'w')
        f.close()
        template.insert_table_template(template_name, brand_id, path)
        return "OK", 200
    else:
        print "!"
        return "Name is busy!", 500



        # return jsonify(res)


@app.route("/test/")
def test():
    return "!"
