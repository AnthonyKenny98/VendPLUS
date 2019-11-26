"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-25 19:48:33

from os import path
import requests
import json
import time

REDIRECT_URI = 'http://127.0.0.1:5000/token'
VEND_CONNECT_URL = 'https://secure.vendhq.com/connect'
CREDENTIALS = 'vend'


class Vend:
    """Provide Class for interfacing with Vend API."""

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
        url = self.base_url(
            self.credentials['domain_prefix'],
            '/1.0/token')

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

    def get(self, url, params={}):
        """Get all data associated with a request."""
        params['after'] = 0
        data = []
        while params['after'] >= 0:
            r = requests.get(url, headers=self.headers, params=params).json()
            if not r['data']:
                params['after'] = -1
            else:
                params['after'] = r['version']['max']
                data.extend(r['data'])
        return data

    def outlet(self):
        """Get Outlets."""
        url = self.base_url(self.credentials['domain_prefix'], '/2.0/outlets')
        return self.get(url)

    def product(self, product_id=None):
        """Get Products."""
        url = self.base_url(self.credentials['domain_prefix'], '/2.0/products')
        if product_id is not None:
            url += '/' + product_id
        return self.get(url)

    def get_inventory_count(self):
        """Get Inventory Counts."""
        url = self.base_url(self.credentials['domain_prefix'],
                            '/2.0/consignments')
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
        url = self.base_url(
            self.credentials['domain_prefix'], '/2.0/consignments')
        payload = {
            'outlet_id': self.outlet()[0]['id'],
            'name': 'TESTCOUNTANTHONY',
            'status': 'STOCKTAKE_SCHEDULED',
            'type': 'STOCKTAKE',
            'show_inactive': 1
        }
        return requests.post(url, data=payload, headers=self.headers)

    def start_inventory_count(self, inventory_count):
        """Start Inventory Count."""
        # url to create inventory count
        url = self.base_url(
            self.credentials['domain_prefix'],
            '/2.0/consignments/{}'.format(inventory_count['id']))
        payload = {
            'outlet_id': inventory_count['outlet_id'],
            'name': inventory_count['name'],
            'status': "STOCKTAKE_IN_PROGRESS",
            'type': "STOCKTAKE"
        }
        return requests.put(url, headers=self.headers, data=payload)

    @staticmethod
    def base_url(domain_prefix, path):
        """Generate Base URL for a given Domain Prefix."""
        return 'https://{}.vendhq.com/api{}'.format(domain_prefix, path)
