import json
import os
import shutil

from flask import jsonify, request

from dblite import brand
from dblite import consts
from app import app
from dblite import session, create, people, template, rules


def get_list_of_brands(user_id, user_role, archived):
    res = {}
    res['brands'] = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_BRANDS + ") where (ARCHIVED = 0 or ARCHIVED = :archived)", user_id, user_role,
        archived=archived)
    return jsonify(res)


@app.route("/brand/<session_id>/<role>")
def get_brands(session_id, role):
    print "!"
    company_id = request.args.get('company_id')
    archived = request.args.get('archived')
    if archived is None:
        archived = 0
    user_id = session.get_user_id(session_id)
    user_role = None if role == "user" else role
    return get_list_of_brands(user_id, user_role, archived)


@app.route("/brand/delete/<session_id>", methods=['POST'])
def delete_brand(session_id):
    company_id = request.args.get('company_id')
    user_id = session.get_user_id(session_id)
    archived = request.args.get('archived')
    if archived is None:
        archived = 0
    if company_id is None:
        return 500, 'Empty brand!'
    user_companies = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_COMPANIES + ") where ID = :company_id",
        user_id, "ADMIN", company_id=company_id)
    if len(user_companies) == 0:
        return 500, 'Access denied!'
    params = json.loads(request.data)
    brand_id = params["brand_id"]
    brand.update_table_brand(brand_id, ARCHIVED=1)
    return get_list_of_brands(user_id, "ADMIN", archived)
    # path = "company_%03d" % user_companies[0]["ID"] + "/brand_%04d" % int(brand_id)
    # main_path = os.path.abspath(os.path.dirname(__file__)) + "/templates/"
    # directory = main_path + path

@app.route("/brand/add/<session_id>", methods=['POST'])
def add_brand(session_id):
    company_id = request.args.get('company_id')
    archived = request.args.get('archived')
    user_id = session.get_user_id(session_id)
    if company_id is None:
        return 500, 'Empty brand!'
    user_companies = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_COMPANIES + ") where ID = :company_id",
        user_id, "ADMIN", company_id=company_id)
    if len(user_companies) == 0:
        return 500, 'Access denied!'
    if archived is None:
        archived = 0
    params = json.loads(request.data)
    brand_name = params["brand_name"]
    brand.insert_table_brand(brand_name, company_id)
    return get_list_of_brands(user_id, "ADMIN", archived)

@app.route("/brand/roles/list/<session_id>", methods=['GET'])
def brand_role_list(session_id):
    brand_id = request.args.get('brand_id')
    user_id = session.get_user_id(session_id)
    if brand_id == None:
        return 500, 'Empty brand!'
    user_brands = people.get_user_items("select * from (" + consts.SQL_GET_USER_BRANDS + ") where ID = :brand_id",
                                        user_id, None, brand_id=brand_id)
    if len(user_brands) == 0:
        return 500, 'Access denied!'
    res = {}
    res["users"] = rules.get_brand_rules(brand_id)
    return jsonify(res)