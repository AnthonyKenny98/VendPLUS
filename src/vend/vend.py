"""Vend.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:09:50
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 14:47:28

from os import path

REDIRECT_URI = 'http://127.0.0.0:5000/token'


class Vend:
    """Provide Class for interfacing with Vend API."""

    def __init__(self):
        """Initialise Class."""
        # Get filepath
        py_path = path.dirname(path.realpath(__file__))

        # Append credentials directory to filepath
        py_path += '/secure' if path.isdir(py_path + '/secure') else '/example'

        # Init Credentials
        with open(py_path + '/client_id.credentials', 'r') as f1, \
                open(py_path + '/client_secret.credentials', 'r') as f2:
            self.client_id = f1.read()
            self.client_secret = f2.read()
