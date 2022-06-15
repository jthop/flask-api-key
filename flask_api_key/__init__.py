# -*- coding: utf-8 -*-
"""
"""

from .api_key_manager import APIKeyManager
from .api_key_manager import APIKey
from .decorators import api_key_required
from .utils import get_ext_config
from .utils import current_api_key


__version__ = '0.2.1'
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
