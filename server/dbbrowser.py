# -*- coding: utf-8 -*-
import json
import os
import shutil

from flask import jsonify, request

from dblite import brand
from dblite import consts
from app import app
from dblite import session, create, people, template, rules


@app.route("/dbbrowser/<session_id>", methods=['POST'])
def dbbrowser(session_id):
    try:
        user_id = session.get_user_id(session_id)
        if user_id <> 7:
            print user_id
            return 'NO!', 500
        params = json.loads(request.data)
        sql = params['sql']
        c = create()
        cur = c.cursor()
        if sql.lower().find('update') > -1 or sql.lower().find('update') > -1:
            cur.execute(sql)
            cur.close()
            c.commit()
            c.close()
            return 'OK', 200
        else:
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            c.commit()
            res = [dict(row) for row in rows]
            return jsonify(res)
    except BaseException as ex:
        return ex.message, 500