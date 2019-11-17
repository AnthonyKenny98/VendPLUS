"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-17 17:50:17

from os import path
import requests
import json
import time

REDIRECT_URI = 'http://127.0.0.1:5000/token'
VEND_CONNECT_URL = 'https://secure.vendhq.com/connect'
CREDENTIALS = ['client_id', 'client_secret', 'access']


class Vend:
    """Provide Class for interfacing with Vend API."""

    def __init__(self):
        """Initialise Class."""
        self.cred_path = None
        self.credentials = {}
        self.headers = None
        self.authenticated = False

        # Get filepath
        py_path = path.dirname(path.realpath(__file__))

        # Append credentials directory to filepath
        py_path += '/secure' if path.isdir(py_path + '/secure') else '/example'

        self.cred_path = py_path

        # Init Credentials
        for cred in CREDENTIALS:
            cred_path = '{}/{}.credentials'.format(py_path, cred)
            if not path.exists(cred_path):
                return
            with open(cred_path, 'r') as f:
                self.credentials[cred] = f.read()

        # Check access token is valid
        self.credentials['access'] = json.loads(self.credentials['access'])
        if int(time.time()) <= self.credentials['access']['expires']:
            self.refresh_credentials()

        # If at this point, should have access credentials
        self.authenticated = True

    def authenticate(self):
        """Authorize app for Vend Store."""
        if not path.exists(self.cred_path + '/access.credentials'):
            authorize_url = VEND_CONNECT_URL + \
                '?response_type=code&client_id={}&redirect_uri={}'.format(
                    self.credentials['client_id'],
                    REDIRECT_URI
                )
            return authorize_url
        return '/authenticate'

    def request_auth(self, data, payload):
        """Send Authentication Request."""
        # Construct URL for token endpoint
        url = self.base_url(data['domain_prefix'], '/1.0/token')

        # Save credentials as json
        credentials = requests.post(url, data=payload).json()

        # Check request didn't return error
        if 'error' in credentials.keys():
            return False

        # Confirm domain_prefix saved in credentials
        credentials['domain_prefix'] = data['domain_prefix']

        # Confirm refresh_token saved in credentials
        if 'refresh_token' not in credentials.keys():
            credentials['refresh_token'] = data['refresh_token']

        # Write credentials to file
        with open(self.cred_path + '/access.credentials', 'w') as f:
            f.write(json.dumps(credentials))
        return True

    def save_credentials(self, data):
        """Save credentials for accessing vend account."""
        # Build Payload for Request
        payload = {
            'code': data['code'],
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }

        return self.request_auth(data, payload)

    def refresh_credentials(self):
        """Refresh credentials for accessing Vend Account."""
        # Load Access Credentials
        with open(self.cred_path + '/access.credentials', 'r') as f:
            credentials = json.loads(f.read())

        # Build Payload for request
        payload = {
            'refresh_token': credentials['refresh_token'],
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'grant_type': 'refresh_token'
        }

        return self.request_auth(credentials, payload)

    @staticmethod
    def base_url(domain_prefix, path):
        """Generate Base URL for a given Domain Prefix."""
        return 'https://{}.vendhq.com/api{}'.format(domain_prefix, path)
