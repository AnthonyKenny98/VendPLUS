"""Main Application."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-08 10:28:57
# @Last Modified by:   AnthonyKenny98

from .vend import Vend
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, render_template
# send_from_directory)
import os
import csv


app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['TEMP_PATH'] = dir_path + '/temp'


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
        return redirect('authenticate')
    return render_template('index.html')


@app.route('/inventory_count', methods=['GET'])
def inventory_count():
    """Inventory Count Handler."""
    v = Vend()
    if not v.authenticated:
        return redirect('authenticate')
    return render_template(
        'tables.html',
        data={
            'breadcrumbs': [
                ('Inventory', '/inventory_count'),
                ('Inventory Counts', '/inventory_count')],
            'table': {
                'name': 'Active Inventory Counts',
                'data': v.get_inventory_count()
            }
        })


def allowed_file(filename):
    """Check if file is a csv."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv']


@app.route('/inventory_count/create', methods=['GET', 'POST'])
def new_inventory_count():
    """Create Inventory Count."""
    v = Vend()
    data = {
        'outlets': v.outlet(),
        'breadcrumbs': [
            ('Inventory', '/inventory_count'),
            ('New Count', '/inventory_count/create')]
    }
    if not v.authenticated:
        return redirect('authenticate')
    if request.method == 'GET':
        return render_template(
            'newCount.html',
            data=data)
    else:
        file = request.files['fileUpload']
        if file.filename == '':
            data['message'] = 'No File Uploaded'
            return render_template(
                'newCount.html', outlets=v.outlet(), data=data)
        if not allowed_file(file.filename):
            data['message'] = 'File must be a CSV'
            return render_template(
                'newCount.html', outlets=v.outlet(), data=data)

        # Save file to temp folder
        filename = os.path.join(app.config['TEMP_PATH'],
                                secure_filename(file.filename))
        file.save(filename)

        products = {p['sku']: p['id'] for p in v.product()}

        # Create Inventory Count
        count = v.create_inventory_count(request.form['inventoryCountName'],
                                         request.form['outlet'])
        v.start_inventory_count(count)

        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            if 'sku' not in reader.fieldnames or \
                    'quantity' not in reader.fieldnames:
                data['message'] = 'CSV has incorrect columns'
                return render_template(
                    'newCount.html', outlets=v.outlet(), data=data)
            for row in reader:
                v.update_inventory_count(
                    count, products[row['sku']], row['quantity'])

        os.remove(filename)
        return redirect('/inventory_count')


@app.errorhandler(404)
def not_found(e):
    """Inbuilt function which takes error as parameter."""
    return render_template('404.html')


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
