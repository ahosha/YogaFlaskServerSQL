from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os

from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TrapsDestinations(Resource):
    @jwt_required()
    def get(self):
        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'trapsdestinations.json'))
        number_of_traphosts = 10       
        # Add rows to table and update proper index
        inflate_table(data, int(number_of_traphosts))
        flatten_data = flatten_json(data)
        try:
            return onGetRequest(data , flatten_data)
        except:
            return trapsdestinations_log_err("GET")

    @jwt_required()
    def post(self):
        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'trapsdestinations.json'))
        number_of_traphosts = 10       
        # Add rows to table and update proper index
        inflate_table(data, int(number_of_traphosts))
        flatten_data = flatten_json(data)
        try:
            return onPostRequest(request , flatten_data)
        except:
            return trapsdestinations_log_err("POST")
        

def trapsdestinations_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'trapsdestinations.json'))

    number_of_traphosts = 10       
    # Add rows to table and update proper index
    inflate_table(data, int(number_of_traphosts))
    flatten_data = flatten_json(data)

    if req.method == 'GET':
        attributes_list = []
        try:
            return onGetRequest(data , flatten_data)
        except:
            return trapsdestinations_log_err("GET")

    if req.method == 'POST':
        try:
            return onPostRequest(req , flatten_data)
        except:
            return trapsdestinations_log_err("POST")

def onGetRequest(data , flatten_data):
    # Send list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    # Go over json data and match values received from ubus
    match_json(data, ubus_attributes_dict)

    # Wrap data
    response_json = wrap_data(data)

    return response_json

def onPostRequest( req , flatten_data):
    # Get POST payload
    payload = req.get_json()
    payload_dict = flatten_payload_to_dict(payload)
    flatten_data = getReadyForSetInUbus(payload_dict , flatten_data)
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    response_json = wrap_data(payload)
    return response_json

def trapsdestinations_log_err(methodType):
    radlogger.log('trapsdestinations_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def getReadyForSetInUbus(payload_dict , flatten_data):
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data