# -*- coding: utf-8 -*-
import json
import os
import shutil
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import jsonify, request
from dblite import consts
from app import app
from dblite import session, create, people, template, rules


@app.route("/template/filelist/<session_id>", methods=['GET'])
def get_file_list(session_id):
    user_id = session.get_user_id(session_id)
    template_id = request.args.get("template_id")
    if template_id == None:
        return 500
    user_templates = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
        template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]
    template_path = user_template["PATH"]
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/templates/%s" % template_path + "/files/"
    # path = u"%s" % path.decode('cp1251')
    # .encode('utf8').decode('utf8').replace(" ","_")
    # path = path.decode(sys.getfilesystemencoding())
    #print path
    #tmp = os.listdir(path.decode("unicode_escape"))
    #print "2"
    files = [f for f in os.listdir(path) if os.path.isfile(path + f)]
    res = {}
    res["files"] = files
    return jsonify(res)


@app.route("/template/filelist/delete/<session_id>", methods=['POST'])
def delete_file(session_id):
    print "!"
    print request.data
    print "!!"
    user_id = session.get_user_id(session_id)
    template_id = request.args.get("template_id")
    params = json.loads(request.data)
    if template_id == None:
        return 500
    user_templates = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
        template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/templates/" + user_template[
        "PATH"] + "/files/"
    os.remove(path + params['file_name'])
    res = {}
    res["files"] = [f for f in os.listdir(path) if os.path.isfile(path + f)]
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
    main_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/templates/"
    directory = main_path + path

    print directory
    if not os.path.exists(directory):
        print "!!!"
        os.makedirs(directory)
        shutil.copyfile(main_path + "empty_template.py", main_path + path + "/template.py")
        f = file(main_path + path + "/__init__.py", 'w')
        f.close()
        template.insert_table_template(template_name, brand_id, path)
        res = {}
        res['templates'] = people.get_user_items(consts.SQL_GET_USER_TEMPLATES, user_id, None)
        return jsonify(res)
    else:
        print "!"
        return "Name is busy!", 500


@app.route("/template/delete/<session_id>", methods=['POST'])
def delete_template(session_id):
    user_id = session.get_user_id(session_id)

    params = json.loads(request.data)
    template_id = params["template_id"]

    user_templates = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
        template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]
    template.delete_template(template_id)
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/templates/" + user_template["PATH"]
    shutil.rmtree(path)
    res = {}
    res['templates'] = people.get_user_items(consts.SQL_GET_USER_TEMPLATES, user_id, None)
    return jsonify(res)


@app.route("/template/save/<session_id>", methods=['POST'])
def save_template(session_id):
    user_id = session.get_user_id(session_id)

    params = json.loads(request.data)
    template_id = params["id"]

    user_templates = people.get_user_items(
        "select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id", user_id, None,
        template_id=template_id)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]

    # params = json.loads(request.data)
    template_code = params["code"].encode("utf-8")
    template_name = params["name"]
    template_project = params["project"]
    main_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    file = open(main_path + '/templates/%s/template.py' % user_template['PATH'], 'w+')
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    file.write(template_code)
    file.close()
    template.update_table_template(template_id, NAME=template_name, PROJECT=template_project)
    res = {}
    # res['templates'] = people.get_user_items(consts.SQL_GET_USER_TEMPLATES, user_id, None)
    return "OK"
