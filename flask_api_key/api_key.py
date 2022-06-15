# -*- coding: utf-8 -*-
"""
"""
import secrets
import string
from uuid import uuid4
from flask import _request_ctx_stack

from .exceptions import MalformedAPIKey
from .exceptions import YouMustBeLost
from .exceptions import APIKeyNotFound
from .utils import get_api_key_manager
from .utils import get_ext_config


DEFAULT_CHARSET = string.ascii_letters + string.digits
CHARSETS = {
    'ascii_62': DEFAULT_CHARSET
}


#########################
#
#    ApiKey
#
#########################


class APIKey(object):
    """
    The primary purpose of this class is to create and parse api_keys

    key = oil_<uuid>.<secret>
    hashed_key = hash(key)
    lookup(uuid)

    Example of creating:
    ak = APIKey()
    ak.gen_key('MY_NEW_KEY')
    print(ak.secret) # WRITE THIS DOWN, NEVER AGAIN

    Example of parsing:
    unverified = request.extract('X-Api-Key')
    ak = APIKey()
    ak.parse(unverified)

    """

    CHARSET = 'ascii_62'

    def __init__(self):
        """
        """

        self._mgr = get_api_key_manager()
        self._cfg = get_ext_config()

        self.label = None
        self.uuid = None
        self.uuid_str = None
        self.hashed_key = None

        self._full_key = None

    def to_dict(self):
        d = {
            'label': self.label,
            'uuid': self.uuid,
            'uuid_str': self.uuid_str,
            'hashed_key': self.hashed_key,
            'do_not_store_full_key': self._full_key
        }
        return d

    def _genword(length=64, _charset='ascii_62'):
        """Signature should be compatible with passlib.pwd.genword
        Args:
            length: Number of characters long the word will be
            charset: Choices of characters for use in the word
        Returns:
            Returns a random string of <length> made up of <charset>
        """

        # obviously a defaultdict works here but it just isn't worth it
        charset = CHARSETS.get(_charset)
        if charset is None:
            charset = DEFAULT_CHARSET
        rando = ''.join(secrets.choice(charset) for i in range(length))

        return rando

    def _hash(self, full_key):
        """Function to hash the key for storage in a db.  Any hash could be
        used, we should take care to protect this just as we would a password.
        """

        return self._mgr._hash_api_key_callback(full_key)

    def _parse_key(self):
        """
        """

        parts = self._full_key.replace('_', '.').split('.')

        if len(parts) != 3:
            raise MalformedAPIKey()
        if parts[0] != self._cfg['prefix']:
            raise YouMustBeLost()

        self._uuid = parts[1]

        obj = self._mgr._fetch_api_key_callback(self._uuid) or None
        if obj is None:
            raise APIKeyNotFound()

        _request_ctx_stack.top.api_key = obj
        return obj

    def verify_key(self, unverified_key):
        """Parse an apikey found in request
        Args:
            unverified_key: This is the full, unhashed, unverified key found in
            the request.
        Returns:
            True/False if the key is valid
        """

        self._full_key = unverified_key
        obj = self._parse_key()

        return self._mgr._verify_api_key_callback(unverified_key, obj)

    def gen_key(self, label):
        """
        62 character charset has 5.95 entropy per character
        64 character secret has ~380 bits entropy
        """

        prefix = self._cfg['prefix']
        length = self._cfg['secret_length']
        charset = self._cfg['secret_charset']

        uuid = uuid4()
        secret = self._genword(length=length, charset=charset)
        full_key = f'{prefix}_{uuid.hex}.{secret}'
        hashed_key = self._hash(full_key)

        self.label = label

        self.uuid = uuid.hex
        self.uuid_str = str(uuid)
        self.hashed_key = hashed_key
        self._full_key = full_key

    @property
    def not_to_save_on_server(self):
        if hasattr(self, '_full_keuy'):
            temp = self._full_key
            del self._full_key
            return temp

        return 'SORRY_THE_SECRET_HAS_SELF_DESTRUCTED'
