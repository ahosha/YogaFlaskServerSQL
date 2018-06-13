from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
from FlaskServer.Resources import en as resource
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def security_route(req):

    if req.method == 'POST':
        try:
            return onPostRequest(req)
        except:
            return security_log_err("POST")




def onPostRequest(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'security.json'))     
    flatten_data = flatten_json(data)
             
    # Get POST payload
    payload = req.get_json()          

    flatten_data = getReadyForSetInUbus(payload)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    success = bool(ubus_attributes_dict)

    if success:
        response_json = wrap_data(payload, msg="success")
    else: 
        response_json = wrap_data(payload, msg="unsuccess")
        
    return response_json


def getReadyForSetInUbus(payload):
    payload_dict = flatten_payload_to_dict(payload)
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data

def security_log_err(methodType):
    radlogger.log('security_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

