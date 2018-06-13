"""
Routes for the flask application. DEV!! DEV!! DEV!! DEV!!
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from FlaskServer.Dev import mockedDataRequest
from FlaskServer.Routes.Monitor import monitor_route
from FlaskServer.Routes.System import system_route
from FlaskServer.Routes.Radio import radio_route_hsu
from FlaskServer.Routes.Network import network_route
from FlaskServer.Routes.RecentEvents import recent_events_route
from FlaskServer.Routes.ActiveAlarms import active_alarms_route
from FlaskServer.Routes.TrapsDestinations import trapsdestinations_route
from FlaskServer.Routes.Debug import debug_log_route, debug_attribute_route
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.ChangeBand import *
from FlaskServer.Routes.Operations.spectrum import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Alignment.Training import training_action_invoker
from FlaskServer.Routes.Alignment import *
from FlaskServer.Routes.Wifi import wifi_route
from FlaskServer.Routes.Battery import battery_route
from FlaskServer.Routes.Sensor import sensor_route
from FlaskServer.Routes.Port import port_route
import FlaskServer.consts as consts

from FlaskServer.Routes.Alignment.alignmnetmockup import *
from FlaskServer.Routes.Alignment.Training import *
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Debug import *


