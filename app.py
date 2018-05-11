# -*- coding: utf-8 -*-
import json

import main
from flask import Flask, request, Response, jsonify, send_file
from werkzeug.utils import secure_filename
from dblite import *

import os

# prefix = d['SERVER-INFO']['PREFIX']
from dblite import people
from dblite import session
from dblite.consts import SQL_GET_USER_TEMPLATES
from model import parse_template_request

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/templates'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
verificationCodes = {}


# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','png', 'ttf'])


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__)) + "/pages"


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/client/', defaults={'path': ''})
@app.route('/client/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".png": "image/png",
        ".jpg": "image/jpeg"
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    return send_file(
        complete_path,
        mimetype,
        attachment_filename=complete_path,
        cache_timeout=0
    ), 200


@app.route('/server/templatelist/<session_id>', methods=['GET'])
def get_template_list(session_id):
    d = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    sql = "select * from template"
    connection = create()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    res = [{"id": row[0], "name": row[1]} for row in rows]
    # res = [{"NAME": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    return jsonify(res)


'''
@app.route('/server/templatecode/<template_name>', methods=['GET'])
def get_template_code(template_name):
    file = open(os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % template_name)
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    return file.read()
'''


@app.route('/server/templatecode/<session_id>', methods=['GET'])
def get_template_code(session_id):
    user_id = session.get_user_id(session_id)
    template_id = request.args.get("template_id")
    if template_id == None:
        return 500
    user_templates = people.get_user_items("select * from (" + SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
                                           template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    template = user_templates[0]
    file_path = os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % template["PATH"]
    file = open(file_path)
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    return file.read()


@app.route('/server/templatecode/<template_name>', methods=['POST'])
def set_template_code(template_name):
    print "%s" % request.data
    # params = json.loads(request.data)
    template_code = request.data
    file = open(os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % template_name, 'w+')
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    file.write(template_code)
    file.close()
    return "OK"  # file.read()


@app.route('/server/<template_name>', methods=['POST'])
def generate_template(template_name):
    params = json.loads(request.data)
    template_request = parse_template_request(params)
    file_name = main.generate_picture(template_name, template_request.width, template_request.height,
                                      template_request.format, float(template_request.dpi))
    return send_file(file_name)


@app.route('/server/upload/<session_id>', methods=['POST'])
def upload(session_id):
    user_id = session.get_user_id(session_id)
    template_id = request.args.get("template_id")
    if template_id == None:
        return "Empty template", 500
    user_templates = people.get_user_items("select * from (" + SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
                                           template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]
    # file_path = os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % user_template["PATH"]
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.abspath(os.path.dirname(__file__)) + "/templates/" + user_template["PATH"] + "/files/" + filename)
    return "OK", 200


@app.route('/login', methods=['POST'])
def login():
    params = json.loads(request.data)
    resp = {}
    email = params['email']
    password = params['password']
    session_id = people.login(email, password)
    if session_id == None:
        return "Wrong login", 500
    else:
        resp["session_id"] = session_id
        return jsonify(resp)


@app.route('/register', methods=['POST'])
def register():
    params = json.loads(request.data)
    resp = {}
    email = params['email']
    session_id = people.register(email, params['password'])
    resp["session_id"] = session_id
    verificationCodes[email] = {}
    verificationCodes[email]["code"] = "123123"
    verificationCodes[email]["session_id"] = session_id
    resp["verified"] = "0"
    return jsonify(resp)


@app.route('/verify', methods=['POST'])
def verify():
    params = json.loads(request.data)
    resp = {}
    email = params['email']
    verification_code = params['code']
    try:
        if verification_code == "123123":
            user_id = people.get_user_by_email(email)
            people.update_table_people(user_id, VERIFIED=1)
            resp = {}
            resp["result"] = "OK"
            # del verificationCodes[email]
            return jsonify(resp), 200
        else:
            return "Wrong code", 500
    except KeyError:
        return "Wrong session", 500


@app.route("/rules/<session_id>", methods=['GET'])
def rules(session_id):
    pass


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
