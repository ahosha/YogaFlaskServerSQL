from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer.Resources import en as resource
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os

from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Wifi(Resource):
    @jwt_required()
    def get(self):
        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'wifi.json'))
        flatten_data = flatten_json(data)
        try:
            return onGetRequest(data , flatten_data)
        except:
            return wifi_log_err("GET")

    @jwt_required()
    def post(self):
        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'wifi.json'))
        flatten_data = flatten_json(data)
        try:
            return onPostRequest(request , flatten_data)
        except:
            return wifi_log_err("POST")



def wifi_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'wifi.json'))
    flatten_data = flatten_json(data)

    if req.method == 'GET':
        try:    
            return onGetRequest(data , flatten_data)
        except:
            return wifi_log_err("GET")

    if req.method == 'POST':
        try:
            return onPostRequest( req , flatten_data)
        except:
            return wifi_log_err("POST")




def onGetRequest(data , flatten_data):
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    #cast_to_int(ubus_attributes_dict,'wifiChannel', 'wifiTxPower')
    cast_to_int(ubus_attributes_dict,'wifiChannel')

    if 'wifiMode' in ubus_attributes_dict and ubus_attributes_dict['wifiMode']:
        ubus_attributes_dict['wifiMode'] = converters.WIFI_POWER_MODES[ubus_attributes_dict['wifiMode']]
        if ubus_attributes_dict['wifiMode'] == resource.wifi_power_on:
            ubus_attributes_dict['wifiMode'] = resource.wifi_auto

    if 'wifiSecurityType' in ubus_attributes_dict and ubus_attributes_dict['wifiSecurityType']:
        ubus_attributes_dict['wifiSecurityType'] = converters.WIFI_SECURITY_TYPE[ubus_attributes_dict['wifiSecurityType']]

    # Moved to monitor
    #if 'wifiApStatus' in ubus_attributes_dict and ubus_attributes_dict['wifiApStatus']:
    #    ubus_attributes_dict['wifiApStatus'] = converters.WIFI_AP_STATUS[ubus_attributes_dict['wifiApStatus']]

    # Build response
    match_json(data, ubus_attributes_dict)

    #pop WiFi password
    data.pop('wifiPassword', None)

    response_json = wrap_data(data)
            
    return response_json


def onPostRequest( req ,flatten_data):
    # Get POST payload
    payload = req.get_json()

    payload_dict = flatten_payload_to_dict(payload)

    if 'wifiMode' in payload_dict and payload_dict['wifiMode'] != '0':
        payload_dict['wifiMode'] = converters.WIFI_POWER_MODES[payload_dict['wifiMode']]

    flatten_data = getReadyForSetInUbus(payload_dict , flatten_data)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    response_json = wrap_data(payload)

    return response_json

def wifi_log_err(methodType):
    radlogger.log('wifi_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def getReadyForSetInUbus(payload_dict , flatten_data ):
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data