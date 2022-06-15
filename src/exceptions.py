# -*- coding: utf-8 -*-
"""
"""

from http import HTTPStatus
from werkzeug.exceptions import HTTPException

from .utils import get_ext_config


class APIKeyError(Exception):
    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.title = self.__class__.__name__
        self.render_template()

    def render_template(self):
        # Simple templating since we can't do this without app_context
        cfg = get_ext_config()
        if '{{HEADER_NAME}}' in self.message:
            self.message = self.message.replace(
                '{{HEADER_NAME}}', cfg['header_name'])
        if '{{HEADER_TYPE}}' in self.message:
            self.message = self.message.replace(
                '{{HEADER_TYPE}}', cfg['header_type'])


class AuthorizationHeaderMissing(APIKeyError):
    status_code = 401
    message = 'Missing {{HEADER_NAME}} header.'


class WrongAuthHeaderType(APIKeyError):
    status_code = 401
    message = 'Authorization header must start with {{HEADER_TYPE}}.'


class HeaderMissingAPIKey(APIKeyError):
    status_code = 401
    message = 'Missing api-key.  Expected "{{HEADER_NAME}}: {{HEADER_TYPE}} <API-KEY>".'


class HeaderContainsExcessParts(APIKeyError):
    status_code = 401
    message = 'Malformed header.  Expected "{{HEADER_NAME}}: {{HEADER_TYPE}} <API-KEY>".'


class InvalidAPIKey(APIKeyError):
    # Very generic error to use when needed or to be purposefully vague
    message = 'api-key invalid.'
    status_code = 401


class APIKeyLookupError(APIKeyError):
    message = 'Exception during user-supplied api-key lookup.'
    status_code = 502


class LocationNotImplemented(APIKeyError):
    message = 'api-key location not yet implemented.'
    status_code = 502


class APIKeyNotFound(APIKeyError):
    message = 'APIKey record not found.'
    status_code = 404


class MalformedAPIKey(APIKeyError):
    message = 'Cannot parse this api-key.  Is this even an api-key?'
    status_code = 502


class YouMustBeLost(APIKeyError):
    message = 'You must be lost.  This sure does not look like one of our api-keys.'
    status_code = 502
