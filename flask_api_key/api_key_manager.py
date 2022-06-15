# -*- coding: utf-8 -*-
"""
"""
from flask import jsonify

from .exceptions import APIKeyError
from .exceptions import APIKeyNotFound
from .api_key import APIKey


#########################
#
#    APIKeyManager
#
#########################


class APIKeyManager(object):

    POSSIBLE_LOCATIONS = ['header']

    def __init__(self, app=None):
        """ApiKey Manager init.  Since we comply with app factory,
        the constructor is put off until init_app()
        Args:
            app: Flask app beinging initialized from.
        """

        self.app = None

        # Set default callbacks - user can change these to their own
        self._create_api_key_callback = APIKeyManager.default_create_api_key_callback
        self._hash_api_key_callback = APIKeyManager.default_hash_api_key_callback
        self._fetch_api_key_callback = APIKeyManager.default_fetch_api_key_callback
        self._verify_api_key_callback = APIKeyManager.default_verify_api_key_callback
        self._error_handler_callback = APIKeyManager.default_error_handler_callback

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Second half of init to support app factory pattern
        Args:
            app: Flask app beinging initialized from.
        """
        self.app = app

        # Save this so we can use it later in the extension
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['flask-api-key'] = self

        self._set_default_config(app)
        self._set_error_handler_callback(app)
        self.config = self.app.config.get_namespace('FLASK_API_KEY_')

    def _set_default_config(self, app):
        """Default config for our flask extension.
        """
        app.config.setdefault('FLASK_API_KEY_LOCATION', 'Header')
        app.config.setdefault('FLASK_API_KEY_HEADER_NAME', 'Authorization')
        app.config.setdefault('FLASK_API_KEY_HEADER_TYPE', 'Bearer')
        app.config.setdefault('FLASK_API_KEY_PREFIX', 'oil')
        app.config.setdefault('FLASK_API_KEY_SECRET_LENGTH', 64)
        app.config.setdefault('FLASK_API_KEY_SECRET_CHARSET', 'ascii_62')

    def _set_error_handler_callback(self, app):
        """Simple method to register a default errorhandler.  Mainly
        a placeholder for potentially more handlers in the future.
        """
        @app.errorhandler(APIKeyError)
        def handle_api_key_error(e):
            return self._error_handler_callback(e)

    def create_api_key_loader(self, callback):
        """Decorator to provide user defined function to save api_keys
        created by the api_key manager.

        See the default for func signature details
        """

        self._create_api_key_callback = callback
        return callback

    def fetch_api_key_loader(self, callback):
        """Decorator to fetch user defined apikeys from
        the db.

        See the default for func signature details
        """

        self._fetch_api_key_callback = callback
        return callback

    def hash_api_key_loader(self, callback):
        """Decorator to provide user defined function to hash the
        apikey for safe storage.

        See the default for func signature details
        """

        self._hash_api_key_callback = callback
        return callback

    def verify_api_key_loader(self, callback):
        """Decorator to provide user defined key verifications

        See the default for func signature details
        """

        self._verify_api_key_callback = callback
        return callback

    def error_handler_loader(self, callback):
        """Decorator to provide a user defined function to be the
        default error handler.

        See the default for func signature details
        """

        self._error_handler_callback = callback
        return callback

    @staticmethod
    def default_create_api_key_callback(apikey):
        """This empty callback is a placeholder.

        Args:
            apikey - an ApiKey object created by this manager
            with a unique and secure key.
        Returns:
            Return the obj which the user just created.

        -EXAMPLE CALLBACK-

        @mgr.create_api_key_loader
        def create_api_key(apikey):
            user_api_key = models.UserAPIKey(**api_key)
            user_api_key.save()

        # WHICH IS THE SAME AS
        @mgr.create_api_key_loader
        def create_api_key(api_key):
            user_api_key = models.UserAPIKey()
            user_api_key.label = api_key.label
            user_api_key.hashed_key = api_key.hashed_key
            user_api_key.save()

            # and finally
            show_user(api_key.secret)
            return user_api_key
        """

        return None

    @staticmethod
    def default_fetch_api_key_callback(uuid):
        """THIS CALLBACK MUST BE IMPLEMENTED FOR THE DEFAULT CODE TO WORK.
        WITHOUT THIS CB NO APIKEY WILL EVER AUTHENTICATE.

        Args:
            uuid: This is the id portion of the key which your db can use to
            search for the record
        Returns:
            obj: The user created obj representing the apikey is returned.  If
            the lookup fails or the key is invalid for any reason return None
            or raise an exception.

        -EXAMPLE CALLBACK-

        @mgr.fetch_api_key_loader
        def fetch_api_key(uuid):
            try:
                obj = models.APIKey.lookup(uuid)
            except models.APIKey.DoesNotExist:
                return None
            if obj.revoked:
                return None
            return obj.hashed_api_key
        """
        return None

    @staticmethod
    def default_hash_api_key_callback(full_key):
        """This default uses the battle-tested passlib library.  Most
        apps will be perfectly fine with this hashlib.
        Args:
            full_key: String - a full, clear unhashed api_key
        Returns:
            Return: String - the hashed version of the entire api_key
        """
        from passlib.apps import custom_app_context

        return custom_app_context.hash(full_key)

    @staticmethod
    def default_verify_api_key_callback(unverified_key, obj):
        """This callback will work unmodified as long as you hash your keys
        using the supplied default and use the hashed_apikey attribute to store
        them in your db model.

        Args:
            uuid: This is the id portion of the key which your db can use to
            search for the record
        Returns:
            obj: The user created obj representing the api_key is returned.

        """
        from passlib.apps import custom_app_context

        hashed = obj.hashed_key
        return custom_app_context.verify(unverified_key, hashed)

    @staticmethod
    def default_error_handler_callback(e):
        """Simple JSON errror handler

        Args:
            e - The error, inherited from ApiKeyError.  Will have 3 attributes.
                message - Simple error message.
                title - Error title which is the error class's name
                status_code - HTTP Status code.  Typically in the response header.
        Returns:
            A werkzeug Response object.

        """

        response = jsonify({
            'title': e.title,
            'message': e.message,
            'status_code': e.status_code
        })
        response.status_code = e.status_code
        return response

    def create(self, label):
        """Using this wrapper is the recommended way to create your apikeys.

        Attr:
            label - required.  Simple label for the key.

        -EXAMPLE USAGE-

        mgr = get_apikey_manager()
        my_key = mgr.create('MY_SECURE_APIKEY')

        # Optionally
        my_key.my_other_attribute = 'foo'
        my_key.save()
        """

        ak = APIKey()
        ak.gen_key(label)
        return self._create_api_key_callback(ak)
