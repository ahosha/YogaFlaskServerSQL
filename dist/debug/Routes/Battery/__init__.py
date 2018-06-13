from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
from FlaskServer.Resources import en as resource
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def battery_route(req):

    if req.method == 'GET':
        try:
            return onGetRequest(req)
        except:
            return battery_log_err("GET")

    if req.method == 'POST':
        try:
            return onPostRequest(req);
        except:
            return battery_log_err("POST")


def onPostRequest(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'battery.json'))
    flatten_data = flatten_json(data)
    # Get POST payload
    payload = req.get_json()          

    flatten_data = getReadyForSetInUbus(payload)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    response_json = wrap_data(payload)

    return response_json


def onGetRequest(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'battery.json'))
    flatten_data = flatten_json(data)
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    # Build response
    match_json(data, ubus_attributes_dict)
    response_json = wrap_data(data)
            
    return response_json

def getReadyForSetInUbus(payload):
    payload_dict = flatten_payload_to_dict(payload)
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data


def battery_log_err(methodType):
    radlogger.log('battery_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json