# -*- coding: utf-8 -*-
"""
"""

from flask import current_app
from flask import _request_ctx_stack
from werkzeug.local import LocalProxy


# Magic access to apikey
current_api_key = LocalProxy(lambda: get_api_key())


def get_api_key():
    ak = getattr(_request_ctx_stack.top, 'api_key', None)
    return ak


def get_api_key_manager():
    try:
        return current_app.extensions['flask-api-key']
    except KeyError:
        raise RuntimeError(
            'You must first initializa Flask-API-Key with this'
            'application before using this method.'
        ) from None


def get_ext_config():
    mgr = get_api_key_manager()
    if mgr:
        return mgr.config
