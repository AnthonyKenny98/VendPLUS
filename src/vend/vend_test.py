"""Vend_test.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:11:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-10 14:51:08

from vend import Vend
from os import path


def test_init():
    """Test Initialization Values of Vend Class."""
    # Get filepath
    py_path = path.dirname(path.realpath(__file__))

    # Append credentials directory to filepath
    py_path += '/secure' if path.isdir(py_path + '/secure') else '/example'

    # Init Vend Instance
    v = Vend()

    with open(py_path + '/client_id.credentials', 'r') as f1, \
            open(py_path + '/client_secret.credentials', 'r') as f2:
        client_id = f1.read()
        client_secret = f2.read()

    assert v.client_id == client_id
    assert v.client_secret == client_secret
