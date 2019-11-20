"""Vend_test.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:11:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-19 19:32:09

from src.vend import Vend


def test_init():
    """Test Initialization Values of Vend Class."""
    v = Vend()
    assert v.credentials['client_id'] is not None
    assert v.credentials['client_secret'] is not None
    assert v.authenticated is not None
    assert type(v.authenticated) is bool

def test_authenticate():
    """Test Authenticate returns correct URL."""
    v = Vend()
    assert v.authenticate() is not None
    assert type(v.authenticate()) is str

def test_products():
    """TODO."""
    pass
