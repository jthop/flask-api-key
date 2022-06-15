[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![PyPI version](https://badge.fury.io/py/flask-api-key.svg)](https://badge.fury.io/py/flask-api-key)

# flask-api-key

Simple Flask Extension to easily add api auth using the good tried and tested api-key model.

JWTs can be great.  Especially if you have 100 microservices and are growing at the rate of Facebook.  But
for those of us that are not scaling at the rate of Facebook or Google, JWTs may be unnecessary.  Tokens
can be instantly revoked.  No complexity added to worry about tokens expiring and how to swap for a new
one, while also worrying about how to protect the refresh-token.

Let's look at the pros of each

## JWTs ##

- **Can share credentials across thousands of microservices within an organization**
- **Great when sharing claims between completely different organizations**
- **DB lookup only needed when issuing token, not on each request**
- **Short lifespan of access_token means compromise only presents a risk for a brief time**

## API-Keys ##

- **Instant revokation**
- **Using a cache most db round-trips can be eliminated**
- **NO need to worry about the time period an access-token is revoked/compromised but hasn't expired**
- **If a key is leaked, key itself gives no indication where/how to use it**
- **Simple to use - offers flexibility how to present the api-key**
- **Simple to use - no worry about key expiration, refreshing, or refresh-key storage**
- **Obviously this is our favorite so how many more pros can we come up with?**

## Use ##

First step install the extension.

    pip install flask-api-key

Now add to your flask project with or without the *app factory* pattern

    from flask import Flask
    from flask_api_key import APIKeyManager

    app = Flask(__name__)
    mgr = APIKeyManager(app)

    -OR-

    mgr = APIKeyManager()
    ...
    def create_app():
        app = Flask(__name__)
        mgr.init_app(app)
        return app

Create an api-key

    my_key = mgr.create('MY_FIRST_KEY')
    print(my_key.secret)

Decorate an endpoint

    from flask_api_key import api_key_required

    @route('/api/v1/secure')
    @api_key_required
    def my_endpoint():
        return jsonify({'foo': 'bar'})

Fetch your endpoint with your key in the Auth header


## Configuration ##

The extension is configured via Flask's built-in config object, app.config.  If unfamiliar with Flask's app.config, you can read more at:
<https://flask.palletsprojects.com/en/2.0.x/api/?highlight=app%20config#configuration>


- **FLASK_API_KEY_LOCATION** - Where to look for the api_key **'Header'**
- **FLASK_API_KEY_HEADER_NAME** - Which header to use (only for location=Header) **'Authorization'**
- **FLASK_API_KEY_HEADER_TYPE** - Which sub-header to use in HEADER_NAME (only for location=Header) **'Bearer'**
- **FLASK_API_KEY_PREFIX** - api_key prefix - can be used to identify your sites keys in a breach **'oil'**
- **FLASK_API_KEY_SECRET_LENGTH** - How many characters long the secret key portion will be **64**
- **FLASK_API_KEY_SECRET_CHARSET** - Passlib compliant charset name to use **'ascii_62'**
