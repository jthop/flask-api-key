# -*- coding: utf-8 -*-
"""
"""

from functools import wraps
from flask import current_app
from flask import request
from flask import _request_ctx_stack

from .exceptions import LocationNotImplemented
from .exceptions import AuthorizationHeaderMissing
from .exceptions import WrongAuthHeaderType
from .exceptions import HeaderMissingAPIKey
from .exceptions import HeaderContainsExcessParts
from .exceptions import InvalidAPIKey
from .api_key_manager import APIKeyManager
from .api_key_manager import APIKey

def api_key_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        location = current_app.config['FLASK_API_KEY_LOCATION']
        header_name = current_app.config['FLASK_API_KEY_HEADER_NAME'] # Authorization
        header_type = current_app.config['FLASK_API_KEY_HEADER_TYPE']

        if location.lower() not in APIKeyManager.POSSIBLE_LOCATIONS:
            raise LocationNotImplemented(f'Location: {location} not implemented yet.')
        
        auth = request.headers.get(header_name, None)
        if not auth:
            raise AuthorizationHeaderMissing()

        parts = auth.split()
        
        if parts[0] != header_type:
            raise WrongAuthHeaderType()
        elif len(parts) == 1:
            raise HeaderMissingAPIKey()
        elif len(parts) > 2:
            # Must be Bearer token?
            raise HeaderContainsExcessParts()

        unverified_key = parts[1] 
        ak = APIKey()
        legit = ak.verify_key(unverified_key)
        if not legit:
            raise InvalidAPIKey()

        return func(*args, **kwargs)
    return decorated_function
