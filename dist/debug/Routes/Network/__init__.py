from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import FlaskServer.attributeshelper as attributeshelper
import os, sys
#from FlaskServer.setting import *
from FlaskServer.serverstate import ServerState
from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#HBS // HSU
#DEVICE_MODE = 'HBS'


class Network(Resource):
    @jwt_required()
    def get(self):
        DEVICE_MODE = ServerState.getDeviceMode(ServerState())
        data = getData(DEVICE_MODE) 
        flatten_data = flatten_json(data)
        try:
            return onGetRequest(data ,flatten_data)
        except:
            return network_log_err("GET")

    @jwt_required()
    def post(self):
        DEVICE_MODE = ServerState.getDeviceMode(ServerState())
        data = getData(DEVICE_MODE) 
        flatten_data = flatten_json(data)
        try:
            return onPostRequest(request , flatten_data)
        except:
            return network_log_err("POST")


def network_route(req):
    DEVICE_MODE = ServerState.getDeviceMode(ServerState())
    data = getData(DEVICE_MODE) 
    flatten_data = flatten_json(data)
    if req.method == 'GET':
        try:    
            return onGetRequest(data ,flatten_data)
        except:
            return network_log_err("GET")

    if req.method == 'POST':
        try:
            return onPostRequest(req , flatten_data)
        except:
            return network_log_err("POST")


def onGetRequest(data ,flatten_data):
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
    if not bool(ubus_attributes_dict):
        return None

    cast_to_int(ubus_attributes_dict, 'vlanId', 'vlanPriority', 'crcErrors')

    # Convert values in dict          
    if 'currentPortState' in ubus_attributes_dict and ubus_attributes_dict['currentPortState'] and ubus_attributes_dict['currentPortState'] != '0':
        ubus_attributes_dict['currentPortState'] = converters.LAN_CURRENT_STATUS[ubus_attributes_dict['currentPortState']]

    if 'desiredPortState' in ubus_attributes_dict and ubus_attributes_dict['desiredPortState'] and ubus_attributes_dict['desiredPortState'] != '0':
        ubus_attributes_dict['desiredPortState'] = converters.LAN_DESIRED_STATUS[ubus_attributes_dict['desiredPortState']]

    if 'GeneralSNMPSupport' in ubus_attributes_dict:
        ubus_attributes_dict['GeneralSNMPSupport'] = converters.SNMP_SUPPORT[ubus_attributes_dict['GeneralSNMPSupport']]

    if 'GeneralTelnetSupport' in ubus_attributes_dict:
        ubus_attributes_dict['GeneralTelnetSupport'] = converters.TELNET_SUPPORT[ubus_attributes_dict['GeneralTelnetSupport']]

    # Build response
    match_json(data, ubus_attributes_dict)

    response_json = wrap_data(data)
            
    return response_json

def onPostRequest(req , flatten_data):         
    # Get POST payload
    payload = req.get_json()          
    payload_dict = flatten_payload_to_dict(payload)

    vlanDict = {}
    if 'vlanId' in payload_dict and payload_dict['vlanId']:
        ubus_attributes_dict_vlan = setVlanId(payload_dict['vlanId'])
    if 'vlanPriority' in payload_dict and payload_dict['vlanPriority']:
        ubus_attributes_dict_vlan = setVlanPriority(payload_dict['vlanPriority'])
               
    #flatten_data =getReadyForSetInUbus(payload_dict)

    _full_ip_param = changeIpParamsFormatBeforeSet(payload_dict)
    payload_dict = pop_data(payload_dict , ['hsuIp' ,'hsuSubnetMask' ,'hsuDefaultGateway'])


    if 'desiredPortState' in payload_dict and payload_dict['desiredPortState'] != '0':
        payload_dict['desiredPortState'] = converters.LAN_DESIRED_STATUS[payload_dict['desiredPortState']]

    flatten_data = getReadyForSetInUbus(payload_dict , flatten_data)

    # Add ip param config
    if _full_ip_param:
        ip_attr = attributeshelper.IP_PARAMS_CONFIG
        ip_attr['value'] = _full_ip_param
        flatten_data.append(ip_attr)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)
    response_json = wrap_data(payload)
    return response_json

def changeIpParamsFormatBeforeSet(payload_dict):
    if ('hsuIp' in payload_dict and payload_dict['hsuIp'] and
    'hsuSubnetMask' in payload_dict and payload_dict['hsuSubnetMask'] and
    'hsuDefaultGateway' in payload_dict and payload_dict['hsuDefaultGateway']):
        full_ip_param = '{0}|{1}|{2}|'.format(payload_dict['hsuIp'], payload_dict['hsuSubnetMask'], payload_dict['hsuDefaultGateway'])
        return full_ip_param
    else:
        return ''

def pop_data(data , names):
    for name in names:
        if name in data:
            data.pop(name)
    return data

def getReadyForSetInUbus(payload_dict , flatten_data):
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data

def setVlanId(vlan_id):
    vlanDict =  {'attr': 890, 'index': 0, 'name': 'vlanId', 'object': 36352, 'value': vlan_id}
    return ubuscontroller.set_attributes_ubus(vlanDict)

def setVlanPriority(vlan_priority):
    vlanDict =  {'attr': 891, 'index': 0, 'name': 'vlanPriority', 'object': 36352, 'value': vlan_priority}
    return ubuscontroller.set_attributes_ubus(vlanDict)

def network_log_err(methodType = 'unknow type'):
    radlogger.log('network_route ' + methodType + ' method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def getData(mode):
    if mode == 'HBS':
        data = load_mapping_json_file(os.path.join(__location__, 'network_hbs.json'))
    elif mode == 'HSU': 
        data = load_mapping_json_file(os.path.join(__location__, 'network_hsu.json'))
    else:
        data = load_mapping_json_file(os.path.join(__location__, 'network_sn.json'))

    return data 