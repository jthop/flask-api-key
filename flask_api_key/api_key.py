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
        self.friendly_uuid = None
        self.hashed_key = None

    def export(self):
        d = {
            'label': self.label,
            'uuid': self.uuid,
            'friendly_uuid': self.friendly_uuid,
            'hashed_key': self.hashed_key,
            'do_not_store_full_key': self.full_key
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
        """Internally used by verify_key().  Splits the key into prefix,
        uuid, and secret so we can lookup in db by uuid.
        Returns:
            Returns the db obj which was returned by the user-defined callback
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
        """62 character charset has 5.95 entropy per character
           64 character secret has ~380 bits entropy
        """

        uuid = uuid4()
        secret = self._genword(
            length=self._cfg['secret_length'],
            charset=self._cfg['secret_charset']
        )

        self.label = label
        self.uuid = uuid.hex
        self.friendly_uuid = str(uuid)
        self._secret = secret

        self.hashed_key = self._hash(self.full_key)

    @property
    def full_key(self):
        """If we have all the pieces, construct the full_key.  Only
        on the fly gives us less chance of compromise.
        """

        prefix = self._cfg['prefix']

        if self.prefix and self.uuid and self._secret:
            full_key = f'{prefix}_{self.uuid}.{self._secret}'
            return full_key
        return None
