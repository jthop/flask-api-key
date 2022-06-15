[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![PyPI version](https://badge.fury.io/py/flask-api-key.svg)](https://badge.fury.io/py/flask-api-key)

# flask-api-key

Simple Flask Extension to easily add api auth using the good tried and tested api key model.

## Why ##

JWTs can be great.  Especially if you have 100 microservices and are growing at the rate of Facebook.  

But for those of us that are not scaling at the rate of Facebook or Google, JWTs may be unnecessary.  Api Keys can be instantly revoked.  No refresh-token policies to worry about (is there a secure refresh standard yet?). With just a little caching(Redis), many of the DB round-trips can be avoided as well.  But most of all, api keys are easy to use.  Your developers can get started in no time.  

So obviously, we believe.  However, while there are tons of JWT/JWS/JWE,JWABC token extensions, very few api key extensions exist.  So, this is my attempt to fill that void.


## Install ##


First things first, install it.
    
`pip install flask-api-key`


## Use ##


1.  Add to your flask project **without** the *app factory* pattern

```python
from flask import Flask
from flask_api_key import APIKeyManager

app = Flask(__name__)
my_key_manager = APIKeyManager(app)
```

Or **with** the *app factory* pattern

```python
my_key_manager = APIKeyManager()
...
def create_app():
    app = Flask(__name__)
    my_key_manager.init_app(app)
    return app
```

2.  Create an api-key

```python
my_key = my_key_manager.create('MY_FIRST_KEY')
print(my_key.secret)
```

3.  Decorate an endpoint

```python
from flask_api_key import api_key_required

@route('/api/v1/secure')
@api_key_required
def my_endpoint():
    return jsonify({'foo': 'bar'})
```

4.  Fetch your endpoint with your key in the Auth header

```shell
curl https://yoursite.com/api/v1/secure
   -H "Accept: application/json"
   -H "Authorization: Bearer INSERT_YOUR_API_KEY_HERE"
```

## Extension Configuration ##


| Variable | Default | Type | Description |
| --- | --- | --- | --- |
| FLASK_API_KEY_LOCATION | `'Header'` | String | Location of the key in the request |
| FLASK_API_KEY_HEADER_NAME | `'Authorization'` | String | Which header to use |
| FLASK_API_KEY_HEADER_TYPE | `'Bearer'` | String | Which header type to use |
| FLASK_API_KEY_PREFIX | `'my_api'` | String | Used to identify your site's keys in a breach [^1] |
| FLASK_API_KEY_SECRET_LENGTH | `64` | Int | Length in characters of the key's secret portion |
| FLASK_API_KEY_SECRET_CHARSET | `'ascii_62'` | String | Passlib compliant charset name to use |


The extension is configured via Flask's built-in config object, app.config.  If unfamiliar with Flask's app.config, it's time to read up on flask: 
<https://flask.palletsprojects.com/en/2.0.x/>

All configuration writing should be done in flask.  However, often times it is necessary to read the config.  We have included multiple ways to access a read-only version of the config.  This read-only config has normalized keys.  The FLASK_API_KEY_ namespace has been removed and the remainder is lower case. 

Example [^2]

```python
loc = my_key_manager.config['location']
print(loc)    # will print 'Header'
```

Also

```python
from flask-api-key.utils import get_ext_config

cfg = get_ext_config()
loc = cfg['location']
print(loc)    # will print 'Header'
```

[^1]: Prefix has many options to explore.  You could use a prefix that unquestionably identifies your keys, such as real_sitename_com_.  Or, if you want to be more vague, you could make up a prefix such as acFFC128jlk_.  As long as you can write a regex to identify your keys, sites such as github will assist you in identifying compromised keys.
[^2]: Both of the examples should print 'Header' only if the config is default and has not been changed.
