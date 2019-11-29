"""Main Application."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-08 10:28:57
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-28 14:59:32

from .vend import Vend

from flask import Flask, request, redirect, render_template

app = Flask(__name__)


@app.route('/authenticate', methods=['GET'])
def authenticate():
    """Authorize."""
    return redirect(Vend().authenticate())


@app.route('/token', methods=['GET'])
def token():
    """Authorize."""
    Vend().save_credentials(request.args.to_dict())
    return redirect('/')


@app.route('/')
def index():
    """Basic Respond."""
    v = Vend()
    if not v.authenticated:
        return redirect('/authenticate')
    return render_template('index.html', message="TEST")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
