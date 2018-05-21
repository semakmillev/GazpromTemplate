import json
import os
import shutil

from flask import jsonify, request
from dblite import consts
from app import app
from dblite import session, create, people, template, rules




@app.route("/rules/company/list/<session_id>", methods=['GET'])
def company_rule_list(session_id):
    company_id = request.args.get('company_id')
    user_id = session.get_user_id(session_id)
    if company_id == None:
        return 500, 'Empty company!'
    user_companies = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_COMPANIES + ") where ID = :company_id",
        user_id, None, company_id=company_id)
    if len(user_companies) == 0:
        return 500, 'Access denied!'
    res = {}
    res["users"] = rules.get_company_rules(company_id)
    return jsonify(res)


@app.route("/rules/brand/list/<session_id>", methods=['GET'])
def brand_rule_list(session_id):
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


@app.route("/rules/template/list/<session_id>", methods=['GET'])
def template_rule_list(session_id):
    template_id = request.args.get('template_id')
    user_id = session.get_user_id(session_id)
    if template_id == None:
        return 500, 'Empty template!'
    user_brands = people.get_user_items("select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id",
                                        user_id, None, template_id=template_id)
    if len(user_brands) == 0:
        return 500, 'Access denied!'
    res = {}
    res["users"] = rules.get_template_rules(template_id)
    return jsonify(res)


@app.route("/rules/delete/<source>/<session_id>", methods=['POST'])
def delete_rule(source, session_id):
    # template_id = request.args.get('template_id')
    item_id = request.args.get('item_id')
    user_id = session.get_user_id(session_id)
    if not rules.check_rule_access(user_id, source, item_id):
        return 500, 'Access denied!'

    params = json.loads(request.data)
    rules.delete_rule(params['rule_id'])
    res = {}
    if source == 'template':
        res["users"] = rules.get_template_rules(item_id)
    elif source == 'brand':
        res["users"] = rules.get_brand_rules(item_id)
    elif source == 'company':
        res["users"] = rules.get_company_rules(item_id)
    return jsonify(res)


@app.route("/rules/add/<source>/<session_id>", methods=['POST'])
def add_rule(source, session_id):
    # template_id = request.args.get('template_id')
    item_id = request.args.get('item_id')
    user_id = session.get_user_id(session_id)

    if not rules.check_rule_access(user_id, source, item_id):
        return 500, 'Access denied!'
    params = json.loads(request.data)
    email = params['email']
    new_user_id = people.get_user_by_email(email)
    if new_user_id is None:
        new_user_id = people.insert_table_people("", email, "", "", "", "", "", 0)

    params = json.loads(request.data)
    rules.insert_table_rules(new_user_id, params['template_id'], params['brand_id'], params['company_id'],
                             params['role'])
    res = {}
    if source == 'template':
        res["users"] = rules.get_template_rules(item_id)
    elif source == 'brand':
        res["users"] = rules.get_brand_rules(item_id)
    elif source == 'company':
        res["users"] = rules.get_company_rules(item_id)
    rules.send_invitation(new_user_id)
    return jsonify(res)
