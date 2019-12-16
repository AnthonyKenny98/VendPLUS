"""Provide Main App Functionality."""

# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2019-11-29 12:21:17
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2019-11-29 12:26:12

INTEREST_KEYS = ['id', 'outlet_id', 'name', 'type', 'status']


def format_data(data):
    """Transform list of dicts into UI presentable format."""
    return [{key: val for key, val in d.items() if key in INTEREST_KEYS}
            for d in data]
