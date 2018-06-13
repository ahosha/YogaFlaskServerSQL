from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

from FlaskServer.serverstate import ServerState

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DeviceMode(Resource):
      @jwt_required()
      def get(self):
        try:
            return onGetRequest()
        except:
            return devicemode_log_err("GET")

def devicemode_route():
    try:
        return onGetRequest()
    except:
        return devicemode_log_err("GET")



def onGetRequest():
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'devicemode.json'))
    flatten_data = flatten_json(data)
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    #Error case
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    if 'sysObjectId' in  ubus_attributes_dict:
        sysObjId = ubus_attributes_dict['sysObjectId']
        convertId = sysObjId[20:21]
        ubus_attributes_dict['sysObjectId'] = converters.SYSTEM_OBJECT_ID[convertId]
        deviceMode = ubus_attributes_dict['sysObjectId']
            
    data = get_data_mode(deviceMode)

    flatten_data = flatten_json(data)
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    if 'ActualConnectMode' in  ubus_attributes_dict:
        ubus_attributes_dict['ActualConnectMode'] = converters.ACTUAL_CONNECT_MODE[ubus_attributes_dict['ActualConnectMode']]

    if 'SwCapabilities' in  ubus_attributes_dict: 
        swCapa = compresseddatahelper.convert_sw_capabilities(ubus_attributes_dict['SwCapabilities'])

    if deviceMode == 'HSU':
        cookie =  ubus_attributes_dict['Cookie'][1:2]
        #if the link state are not connected
        if ubus_attributes_dict['hsuLinkState'] == "1" and cookie == '2':
            ubus_attributes_dict['ActualConnectMode'] = 'p2p'
          
    #Build response
    match_json(data, ubus_attributes_dict)
    data.pop('hsuLinkState', None)
    data.pop('Cookie', None) 
    data.pop('SwCapabilities', None)
    response_json = wrap_data(data)
    response_json['data']['sysObjectId'] = deviceMode
    response_json['data']['SwCapabilities'] = swCapa

    return response_json



def devicemode_log_err(methodType):
    radlogger.log('devicemode_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def get_data_mode(deviceMode):
    if deviceMode == 'HBS':
        data = load_mapping_json_file(os.path.join(__location__, 'devicemode_hbs.json'))
        ServerState.setDeviceMode( ServerState() , 'HBS')
    else:
        data = load_mapping_json_file(os.path.join(__location__, 'devicemode_hsu.json'))
        ServerState.setDeviceMode( ServerState() ,'HSU')
    return data