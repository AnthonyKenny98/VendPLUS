"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 14:30:36

import os

REDIRECT_URI = 'http://127.0.0.0:5000/token'


class Vend:
    """Provide Class for interfacing with Vend API."""

    def __init__(self):
        """Initialise Class."""
        # Get filepath
        pyfile_path = os.path.dirname(os.path.realpath(__file__))

        # Init Credentials
        with open(pyfile_path + '/client_id.credentials', 'r') as f1, \
                open(pyfile_path + '/client_secret.credentials', 'r') as f2:
            self.client_id = f1.read()
            self.client_secret = f2.read()
