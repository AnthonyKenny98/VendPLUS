"""Vend_test.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:11:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-25 16:58:48

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
    result = v.authenticate()
    assert result is not None
    assert type(result) is str


def test_product():
    """TODO."""
    v = Vend()
    products = v.product()
    assert type(products) is list
    assert len(products) > 1


def test_get_inventory_count():
    """TODO."""
    v = Vend()
    inventory_counts = v.get_inventory_count()
    assert type(inventory_counts) is list
    assert len(inventory_counts) > 1
