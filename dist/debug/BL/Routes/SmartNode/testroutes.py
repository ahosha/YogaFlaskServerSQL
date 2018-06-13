"""
Routes for the flask application. DEV!! DEV!! DEV!! DEV!!
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from FlaskServer.Dev import mockedDataRequest
import FlaskServer.consts as consts
from FlaskServer.Routes.Alignment import *
from FlaskServer.Routes.Alignment.alignmnetmockup import *
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.Operations.spectrum import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Debug import *

