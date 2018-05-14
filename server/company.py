import json
import os
import shutil

from flask import jsonify, request

from dblite import brand
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