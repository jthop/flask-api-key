# flask-api-key

Simple Flask Extension to easily add api auth using the good tried and tested api-key model.  

JWTs can be great.  Especially if you have 100 microservices and are growing at the rate of Facebook.  But
for those of us that don't measure our hits in the millions/sec the api-key method is still the best.  All 
joking aside if you can afford a db OR redis round-trip per request this method is for you.  No worrys about 
refresh token security.  Tokens can be instantly revoked.  No complexity added to worry about tokens expiring a
nd how to swap for a new one, while also worrying how to protect the refresh-token.

Let's look at the pros of each

## JWTs ##

- **Can share credentials across thousands of microservices within an organization**
- **Great when sharing claims between completely different organizations**
- **DB lookup only needed when issuing token, not on each request**

## API-Keys ##

- **Instant revokation**
- **Using a cache most db round-trips can be eliminated**
- **NO need to worry about time period an access-token is revoked but not expired**
- **If key is leaked, key itself gives no indication where/how to use it**
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

Configure as you would any other flask extension.  Currently the config variables available are:

    FLASK_API_KEY_HEADER_NAME = 'Authorization'
    FLASK_API_KEY_HEADER_TYPE = 'Bearer'
    FLASK_API_KEY_PREFIX = 'oil'
    FLASK_API_KEY_SECRET_LENGTH = 64
    FLASK_API_KEY_SECRET_CHARSET = 'ascii_62'
