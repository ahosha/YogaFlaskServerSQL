from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys
from FlaskServer.serverstate import ServerState

from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Hss(Resource):
      @jwt_required()
      def get(self):
        try:
            return onGetRequest()
        except:
            return hss_log_err("GET")

def hss_route(req):
    try:
        return onGetRequest()
    except:
        return hss_log_err("GET")



def onGetRequest():
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'hss.json'))
    flatten_data = flatten_json(data)
    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    #Error case
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json     
    
    flatten_data = flatten_json(data)
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

    if 'HssCurrentOpState' in  ubus_attributes_dict:
       ubus_attributes_dict['HssCurrentOpState'] = converters.HSS_CURRENT_OP_STATE[ubus_attributes_dict['HssCurrentOpState']]

    if 'HssPulseType' in  ubus_attributes_dict:
       ubus_attributes_dict['HssPulseType'] = converters.HSS_PULSE_TYPE[ubus_attributes_dict['HssPulseType']]

    if 'HssPulseStatus' in  ubus_attributes_dict:
       ubus_attributes_dict['HssPulseStatus'] = converters.HSS_PULSE_STATUS[ubus_attributes_dict['HssPulseStatus']]

    if 'HssDesiredOpState' in  ubus_attributes_dict:
       ubus_attributes_dict['HssDesiredOpState'] = converters.HSS_DESIRED_OP_STATE[ubus_attributes_dict['HssDesiredOpState']]

    if 'HssSyncStatus' in  ubus_attributes_dict:
       ubus_attributes_dict['HssSyncStatus'] = converters.HSS_SYNCP_STATUS[ubus_attributes_dict['HssSyncStatus']]

    if 'HssDesiredPulseType' in  ubus_attributes_dict:
       ubus_attributes_dict['HssDesiredPulseType'] = converters.HSS_PULSE_TYPE[ubus_attributes_dict['HssDesiredPulseType']]

    #Build response
    match_json(data, ubus_attributes_dict)
    response_json = wrap_data(data)
    return response_json



def hss_log_err(methodType):
    radlogger.log('hss_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json
