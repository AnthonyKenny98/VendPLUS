"""Vend_test.py."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-10 14:11:36
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-28 14:07:02

import time
import pytest
import os

from src.vend import Vend


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_init():
    """Test Initialization Values of Vend Class."""
    v = Vend()
    assert v.credentials['client_id'] is not None
    assert v.credentials['client_secret'] is not None
    assert v.authenticated is not None
    assert type(v.authenticated) is bool
    assert v.authenticated
    assert int(time.time()) < v.credentials['expires']


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_authenticate():
    """Test Authenticate returns correct URL."""
    v = Vend()
    result = v.authenticate()
    assert result is not None
    assert type(result) is str


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_url():
    """Test url method returns correct url."""
    v = Vend()
    base_url = 'https://' + v.credentials['domain_prefix'] + '.vendhq.com/api'
    assert v.url('token') == base_url + '/1.0/token'
    assert v.url('outlet') == base_url + '/2.0/outlets'
    assert v.url('product') == base_url + '/2.0/products'
    assert v.url('inventory_count') == base_url + '/2.0/consignments'


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_get():
    """Test Get."""
    v = Vend()
    url = v.url('outlet')
    result = v.get(url)
    assert type(result) is list
    assert len(result) > 0
    assert type(result[0]) is dict


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_product():
    """Test product."""
    # v = Vend()
    # url = v.url('product')
    # result = v.get(url)
    # assert type(result) is list
    # assert len(result) > 0
    # assert type(result[0]) is dict
    pass


@pytest.mark.skipif('TRAVIS' in os.environ, reason='No Real Credentials')
def test_get_inventory_count():
    """TODO."""
    # v = Vend()
    # url = v.url('inventory_count')
    # result = v.get(url)
    # assert type(result) is list
    # assert len(result) > 0
    # assert type(result[0]) is dict
    pass
