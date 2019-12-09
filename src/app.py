"""Main Application."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-08 10:28:57
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-30 17:15:11

from .vend import PrettyVend as Vend
from .controller import format_data

from flask import Flask, request, redirect, render_template

app = Flask(__name__)


def connect_vend():
    """Instantiate Vend Instance, redirect if not authenitcated."""
    v = Vend()
    if not v.authenticated:
        return redirect('/authenticate')
    return v


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
    connect_vend()
    return render_template('index.html', message="TEST")


@app.route('/inventory_count', methods=['GET'])
def inventory_count():
    """Inventory Count Handler."""
    v = connect_vend()
    return render_template(
        'tables.html',
        data=format_data(v.get_inventory_count()))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
