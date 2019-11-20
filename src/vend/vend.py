"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-19 19:33:14

from os import path
import requests
import json
import time
from flask import redirect

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

    def products(self):
        """Get Products."""
        url = self.base_url(self.credentials['domain_prefix'], '/2.0/products')
        return requests.get(url, headers=self.headers).json()

    @staticmethod
    def base_url(domain_prefix, path):
        """Generate Base URL for a given Domain Prefix."""
        return 'https://{}.vendhq.com/api{}'.format(domain_prefix, path)
