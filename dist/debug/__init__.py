"""
The flask application package.
"""
from flask import Flask
from flask_jwt import JWT
from werkzeug.contrib.cache import SimpleCache
from FlaskServer.BL.Factory import Factory
from FlaskServer.errorhandlers import configure_error_handlers

#from FlaskServer.config import configure_app
#from FlaskServer.BL.config import *
#from FlaskServer.setting import *

app = Flask(__name__)
app.cache = SimpleCache()

# Error handlers for 400, 404, 500 codes
configure_error_handlers(app)

# JWT
from FlaskServer.Authentication import authenticate, identity
jwt = JWT(app, authenticate, identity)

factory = Factory()
factory.create_app_instance(app)

