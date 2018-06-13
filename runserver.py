from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from werkzeug.contrib.cache import SimpleCache
#from FlaskServer.errorhandlers import configure_error_handlers
from os import environ
from FlaskServer import app
from FlaskServer.setting import *





if __name__ == '__main__':
    from FlaskServer.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
