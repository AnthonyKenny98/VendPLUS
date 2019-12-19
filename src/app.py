"""Main Application."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-08 10:28:57
# @Last Modified by:   AnthonyKenny98

from .vend import Vend

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
    return render_template('index.html')


@app.route('/inventory_count', methods=['GET'])
def inventory_count():
    """Inventory Count Handler."""
    v = connect_vend()
    return render_template(
        'tables.html',
        data={
            'table': {
                'name': 'Active Inventory Counts',
                'data': v.get_inventory_count()
            }
        })


@app.errorhandler(404)
def not_found(e):
    """Inbuilt function which takes error as parameter."""
    return render_template("404.html")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
