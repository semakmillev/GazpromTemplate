# -*- coding: utf-8 -*-
import json
import main
from flask import Flask, request, Response, jsonify, send_file
import os

# prefix = d['SERVER-INFO']['PREFIX']


app = Flask(__name__)


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


@app.route('/server/templatelist/', methods=['GET'])
def get_template_list():
    d = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    return jsonify(res)


@app.route('/server/templatecode/<template_name>', methods=['GET'])
def get_template_code(template_name):
    file = open(os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % template_name)
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    return file.read()

@app.route('/server/templatecode/<template_name>', methods=['POST'])
def set_template_code(template_name):
    print "%s" % request.data
    #params = json.loads(request.data)
    template_code = request.data
    file = open(os.path.abspath(os.path.dirname(__file__)) + '/templates/%s/template.py' % template_name, 'w+')
    # res = [{"name": o} for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]
    file.write(template_code)
    file.close()
    return "OK" #file.read()


@app.route('/server/<template_name>', methods=['POST'])
def generate_template(template_name):
    params = json.loads(request.data)
    file_name = main.generate_picture(template_name, params['width'], params['height'])
    return send_file(file_name, mimetype="image/png")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    ## host='0.0.0.0'
    app.run(host='0.0.0.0', port=5005)
