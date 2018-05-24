import json
import os
import shutil

from celery.result import AsyncResult
from flask import jsonify, request, send_file
from dblite import consts
from app import app
from dblite import session, create, people, template, rules, task
from dblite.consts import SQL_GET_USER_TEMPLATES
from model import parse_template_request
from queue import tasks
from celery_run import app as celery_app

@app.route('/server/async/tasks/<template_id>/<session_id>', methods=['POST'])
def generate_async_template(template_id, session_id):
    user_id = session.get_user_id(session_id)
    print user_id, template_id
    user_templates = people.get_user_items("select * from (" + SQL_GET_USER_TEMPLATES + ") where ID = :template_id",
                                           user_id, None,
                                           template_id=template_id)

    params = json.loads(request.data)
    template_request = parse_template_request(params)
    if len(user_templates) == 0:
        return "Access denied", 500
    user_template = user_templates[0]
    process_task = tasks.generate_picture.apply_async((
        user_template["PATH"],
        template_request.width,
        template_request.height,
        template_request.format,
        float(template_request.dpi),
        user_id), queue='TEMPLATE.Q')
    task_id = process_task.id
    task_info = "%s, %sx%s dpi:%s, format: %s" % (user_template["NAME"],
                                                  template_request.width,
                                                  template_request.height,
                                                  template_request.dpi,
                                                  template_request.format)
    task.insert_table_task(task_id, user_id, task_info)
    return jsonify(task.get_user_tasks(int(user_id))), 200


@app.route('/server/async/tasks/<session_id>', methods=['GET'])
def get_task_list(session_id):
    user_id = session.get_user_id(session_id)
    res = task.get_user_tasks(user_id)
    return jsonify(res)


@app.route('/server/async/tasks/refresh/<session_id>', methods=['GET'])
def refresh_task(session_id):
    user_id = session.get_user_id(session_id)
    user_tasks = task.get_user_tasks(int(user_id))
    task_id = request.args.get("task_id")
    user_tasks = [t for t in user_tasks if t['task_id'] == task_id]

    if len(user_tasks) == 0:
        return "Access denied", 500

    user_task = user_tasks[0]
    res = AsyncResult(user_task['task_id'], app=celery_app)
    if res.status == "SUCCESS":
        print str(res.get())
        task.set_status(user_task['task_id'], 'SUCCESS', str(res.get()))
        user_task['status'] = 'SUCCESS'
        user_task['result'] = str(res.get())
    return jsonify(user_task), 200




@app.route('/server/async/tasks/download/<session_id>', methods=['POST'])
def download_template(session_id):
    user_id = session.get_user_id(session_id)
    user_tasks = task.get_user_tasks(int(user_id))
    params = json.loads(request.data)
    task_id = params['task_id']
    user_tasks = [t for t in user_tasks if t['task_id'] == task_id]
    if len(user_tasks) == 0:
        return "Access denied", 500
    user_task = user_tasks[0]
    return send_file(user_tasks[0]['result']), 200
