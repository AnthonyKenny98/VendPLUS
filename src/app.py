"""Main Application."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-08 10:28:57
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 17:01:44

from vend.vend import Vend

from flask import Flask, jsonify, request, redirect
app = Flask(__name__)


@app.route('/authenticate', methods=['GET'])
def authenticate():
    """Authorize."""
    return redirect(Vend().authorize())


@app.route('/token', methods=['GET'])
def token():
    """Authorize."""
    return str(Vend().save_credentials(request.args.to_dict()))


@app.route('/refresh', methods=['GET'])
def refresh():
    """Authorize."""
    return str(Vend().refresh_credentials())


@app.route('/')
def index():
    """Basic Respond."""
    return jsonify({"Message": "Response"})

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
