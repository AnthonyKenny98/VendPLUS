"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-12-19 13:15:55

from os import path
import requests
import json
import time
from datetime import datetime

REDIRECT_URI = 'http://127.0.0.1:5000/token'
VEND_CONNECT_URL = 'https://secure.vendhq.com/connect'
CREDENTIALS = 'vend'


class VendSuper:
    """Provide functionality for interfacing with Vend API."""

    def __init__(self):
        """Initialise, set self.authenticated True once authenticated."""
        self.credentials = {}
        self.authenticated = False

        # Get filepath
        py_path = path.dirname(path.realpath(__file__))
        py_path += '/secure' if path.isdir(py_path + '/secure') else '/example'

        # Init Credentials
        with open('{}/{}.credentials'.format(py_path, CREDENTIALS), 'r') as f:
            self.credentials = json.load(f)

        # Return unauthenticated if no access_token
        if 'access_token' not in self.credentials:
            return

        # Check access token is valid
        if int(time.time()) >= self.credentials['expires']:
            self.refresh_credentials()

        # If at this point, should have access credentials
        self.authenticated = True
        self.headers = {'Authorization': 'Bearer {}'.format(
            self.credentials['access_token'])}

    def authenticate(self):
        """Retrun url to authenticate app for Vend Domain."""
        authorize_url = VEND_CONNECT_URL + \
            '?response_type=code&client_id={}&redirect_uri={}'.format(
                self.credentials['client_id'],
                REDIRECT_URI
            )
        return authorize_url

    def request_auth(self, payload):
        """Send Authentication Request."""
        # Construct URL for token endpoint
        url = self.url('token')

        # Save credentials as json
        credentials = requests.post(url, data=payload).json()

        # Check request didn't return error
        if 'error' in credentials.keys():
            return False

        # Update self.credentials
        for key, val in credentials.items():
            self.credentials[key] = val

        # Write credentials to file
        py_path = path.dirname(path.realpath(__file__))
        py_path += '/secure' if path.isdir(py_path + '/secure') else '/example'
        with open('{}/{}.credentials'.format(py_path, CREDENTIALS), 'w') as f:
            f.write(json.dumps(self.credentials, indent=4))
        return True

    def save_credentials(self, data):
        """Save credentials for accessing vend account."""
        # Build Payload for Request
        self.credentials['domain_prefix'] = data['domain_prefix']
        payload = {
            'code': data['code'],
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }

        return self.request_auth(payload)

    def refresh_credentials(self):
        """Refresh credentials for accessing Vend Account."""
        # Build Payload for request
        payload = {
            'refresh_token': self.credentials['refresh_token'],
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'grant_type': 'refresh_token'
        }

        return self.request_auth(payload)

    def url(self, endpoint):
        """Generate URL for a given Domain Prefix and endpoint."""
        selector = {
            'token': '/1.0/token',
            'outlet': '/2.0/outlets',
            'product': '/2.0/products',
            'inventory_count': '/2.0/consignments',
        }
        return 'https://{}.vendhq.com/api{}'.format(
            self.credentials['domain_prefix'],
            selector[endpoint])

    def get(self, url, params={}):
        """Get all data associated with a request."""
        params['after'] = 0
        data = []
        while params['after'] >= 0:
            r = requests.get(url, headers=self.headers, params=params).json()
            if 'version' not in r.keys():
                return r['data']
            elif not r['data']:
                params['after'] = -1
            else:
                params['after'] = r['version']['max']
                data.extend(r['data'])
        return data

    def outlet(self, outlet_id=None):
        """Get Outlets."""
        url = self.url('outlet')
        if outlet_id is not None:
            url += '/' + outlet_id
        return self.get(url)

    def product(self, product_id=None):
        """Get Products."""
        url = self.url('product')
        if product_id is not None:
            url += '/' + product_id
        return self.get(url)

    def get_inventory_count(self):
        """Get Inventory Counts."""
        url = self.url('inventory_count')
        status_codes = [
            'STOCKTAKE_SCHEDULED',
            'STOCKTAKE_IN_PROGRESS',
            'STOCKTAKE_IN_PROGRESS_PROCESSED'
        ]
        consignments = []
        for code in status_codes:
            consignments.extend(self.get(url, params={
                "type": "STOCKTAKE",
                'status': code
            }))
        return consignments

    def create_inventory_count(self):
        """Create Inventory Count."""
        url = self.url('inventory_count')
        payload = {
            'outlet_id': self.outlet()[0]['id'],
            'name': 'TESTCOUNTANTHONY',
            'status': 'STOCKTAKE_SCHEDULED',
            'type': 'STOCKTAKE',
            'show_inactive': 1
        }
        return requests.post(
            url, data=payload, headers=self.headers).json()['data']

    def start_inventory_count(self, inventory_count):
        """Start Inventory Count."""
        url = self.url('inventory_count') + '/' + inventory_count['id']
        payload = {
            'outlet_id': inventory_count['outlet_id'],
            'name': inventory_count['name'],
            'status': "STOCKTAKE_IN_PROGRESS",
            'type': "STOCKTAKE"
        }
        return requests.put(url, headers=self.headers, data=payload)

    def delete_inventory_count(self, inventory_count):
        """Delete Inventory Count."""
        url = self.url('inventory_count') + '/' + inventory_count['id']
        return requests.delete(url, headers=self.headers)

    def update_inventory_count(self, count, product_id, inventory):
        """Update Product Count for an Inventory Count."""
        url = self.url('inventory_count') + '/{}/products'.format(count['id'])
        payload = {
            'product_id': product_id,
            'received': inventory
        }
        return requests.post(url, headers=self.headers, data=payload)


class Vend(VendSuper):
    """
    Provide functionality for interfacing with Vend API.

    Return UI friendly values.
    """

    def __init__(self):
        """Initialise. No added functionality."""
        super().__init__()

    def get_inventory_count(self):
        """Return user friendly inventory count data."""
        data = super().get_inventory_count()
        return [{
            'Outlet': self.outlet(d['outlet_id'])['name'],
            'Count Name': d['name'],
            'Count Status': d['status'],
            'Date Created': datetime.strptime(
                d['created_at'], '%Y-%m-%dT%H:%M:%S+00:00').date(),
            'href': 'https://{}.vendhq.com/inventory_count/{}'.format(
                self.credentials['domain_prefix'], d['id'])
        } for d in data]
