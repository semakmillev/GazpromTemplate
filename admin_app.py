# -*- coding: utf-8 -*-
import json
import os
import shutil

from flask import jsonify, request
from dblite import consts
from app import app
from dblite import session, create, people, template, rules

def send_invitation(email):
    pass

@app.route('/server/role/add/<source>/<session_id>/')
def add_role(source, session_id):
    params = json.loads(request.data)
    role = params["role"]
    email = params["email"]
    company_id = None
    brand_id = None
    template_id = None
    if source == "company":
        company_id = params["company_id"]
    if source == "brand":
        brand_id = params["brand_id"]
    if source == "company":
        template_id = params["template_id"]











        # return jsonify(res)


@app.route("/test/")
def test():
    return "!"
