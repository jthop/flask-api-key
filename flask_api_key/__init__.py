# -*- coding: utf-8 -*-
"""
"""

from .api_key_manager import APIKeyManager
from .api_key_manager import APIKey
from .decorators import api_key_required
from .utils import current_api_key


__semantic_version__ = '0.1.5'
__build__ = 232
__version__ = f'{__semantic_version__}+build.{__build__}'
__author__ = '@jthop'
__copyright__ = f'Copyright 2022 {__author__}'


__all__ = [
    '__version__',
    '__author__',
    '__copyright__',
    'APIKeyManager',
    'APIKey',
    'api_key_required',
    'current_api_key'
]
