from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys
from FlaskServer.setting import *
from FlaskServer.serverstate import ServerState

from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#HBS // HSU
#DEVICE_MODE = 'HBS'

class System(Resource):
    @jwt_required()
    def get(self):
        try:
            return onGetRequest()
        except:
            return system_log_err("GET")

    @jwt_required()
    def post(self):
        try:
            return onPostRequest()
        except:
            return system_log_err("POST")


def system_route(req):   
    if req.method == 'GET':
        try:
           return onGetRequest()
        except:
           return system_log_err("GET")

    if req.method == 'POST':
        try:
            return onPostRequest()
        except:
            return system_log_err("POST")



def onGetRequest():
    DEVICE_MODE = ServerState.getDeviceMode(ServerState())
    data = getJsonData(DEVICE_MODE)    
    flatten_data = flatten_json(data)
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    # Build response
    match_json(data, ubus_attributes_dict)

    # Parse *HBS* compressed data
    if DEVICE_MODE == 'HSU':
        data = compressHBS(data)

    # Parse *HSU* compressed data
    if DEVICE_MODE == 'HBS':
        data = compressHSU(data)
   
    # Sanitize data
    data['hbs'].pop('hbsCompressedStatic', None)
    data['hsu'].pop('hsuCompressedStatic', None)

    #  Installation Confirmation required for Radius mode. 1- true 2- false
    if 'installConfirmReq' in data and data['installConfirmReq']:
        val = ubus_attributes_dict['installConfirmReq']
        data['installConfirmReq'] = 'true' if int(val) == 1 else 'false'

    response_json = wrap_data(data)

    if 'sysObjectId' in  response_json['data']:
        response_json['data']['sysObjectId'] = parseSysObjectId(response_json)

    response_json['data']['flaskVersion'] = VERSION_NUMBER   
    return response_json
  
def onPostRequest():

    DEVICE_MODE = ServerState.getDeviceMode(ServerState())
    data = getJsonData(DEVICE_MODE)    
    flatten_data = flatten_json(data)

    # Get POST payload
    payload = request.get_json()
       
    flatten_data = getReadyForSetInUbus(payload , flatten_data)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    response_json = wrap_data(payload)

    return response_json


def system_log_err(methodType = 'unknow type'):
    radlogger.log('system_route ' + methodType + ' method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def compressHSU(data):
        parsed_data = compresseddatahelper.parse_HSU_static(data['hsu']['hsuCompressedStatic'])

        if parsed_data and not parsed_data == 'No Link':
            for val in parsed_data:
                if val == 'hsuAntennaType':
                    data['hsu'][val] = converters.ANTENNA_TYPE[str(parsed_data[val])]
                else:
                    data['hsu'][val] = parsed_data[val]

            mac = data['hsu']['hsuMACAddress']
            ServerState.setMacAdressHsu(ServerState(), mac)
        else:
            data['hsu'] = {}

        return data


def compressHBS(data):
        parsed_data = compresseddatahelper.parse_HBS_static(data['hbs']['hbsCompressedStatic'])
        if parsed_data:
            for val in parsed_data:
                if val == 'hsuAntennaType':
                    data['hbs'][val] = converters.ANTENNA_TYPE[parsed_data[val]]
                else:
                    data['hbs'][val] = parsed_data[val]
        else:
            data['hbs'] = {}
        return data


def getReadyForSetInUbus(payload , flatten_data):
    payload_dict = flatten_payload_to_dict(payload)
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data

def parseSysObjectId(response_json):
    sysObjId = response_json['data']['sysObjectId']
    convertId = sysObjId[20:21]
    return converters.SYSTEM_OBJECT_ID[convertId]


def getJsonData(mode):
    if mode == 'HBS':
        data = load_mapping_json_file(os.path.join(__location__, 'system_hbs.json'))
    elif mode == 'HSU':
        data = load_mapping_json_file(os.path.join(__location__, 'system.json'))
    else:
        data = load_mapping_json_file(os.path.join(__location__, 'system_sn.json'))

    return data



def flask_version_route(req):
    return VERSION_NUMBER

