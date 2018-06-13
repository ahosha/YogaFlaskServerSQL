from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
from FlaskServer.Resources import en as resource
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def systemhbs_route(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'systemhbs.json'))
            
    flatten_data = flatten_json(data)


    if req.method == 'GET':
        try:

            data.pop('PortReset0')
            data.pop('PortReset1')
            data.pop('PortReset2')
            data.pop('PortReset3')
            data.pop('PortReset4')

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Build response
            match_json(data, ubus_attributes_dict)
            response_json = wrap_data(data)
            
            return response_json

        except:
            radlogger.log('port_route GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            
            # Get POST payload
            payload = req.get_json()          

            payload_dict = flatten_payload_to_dict(payload)

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]


            dict = {}
            if 'PortVlanMode0' in payload_dict and payload_dict['PortVlanMode0']:
                dict =  {'attr': 2097, 'index': 0, 'name': 'PortVlanMode0', 'object': 50688, 'value': payload_dict['PortVlanMode0']}
                ubus_attributes_dict_vlan = ubuscontroller.set_attributes_ubus(dict)
            if 'PortVlanMode1' in payload_dict and payload_dict['PortVlanMode1']:
                dict =  {'attr': 2097, 'index': 1, 'name': 'PortVlanMode1', 'object': 50688, 'value': payload_dict['PortVlanMode1']}
                ubus_attributes_dict_vlan = ubuscontroller.set_attributes_ubus(dict)
            if 'PortVlanMode2' in payload_dict and payload_dict['PortVlanMode2']:
                dict =  {'attr': 2097, 'index': 2, 'name': 'PortVlanMode2', 'object': 50688, 'value': payload_dict['PortVlanMode2']}
                ubus_attributes_dict_vlan = ubuscontroller.set_attributes_ubus(dict)
            if 'PortVlanMode3' in payload_dict and payload_dict['PortVlanMode3']:
                dict =  {'attr': 2097, 'index': 3, 'name': 'PortVlanMode3', 'object': 50688, 'value': payload_dict['PortVlanMode3']}
                ubus_attributes_dict_vlan = ubuscontroller.set_attributes_ubus(dict)
            if 'PortVlanMode4' in payload_dict and payload_dict['PortVlanMode4']:
                dict =  {'attr': 2097, 'index': 4, 'name': 'PortVlanMode4', 'object': 50688, 'value': payload_dict['PortVlanMode4']}
                ubus_attributes_dict_vlan = ubuscontroller.set_attributes_ubus(dict)



            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            radlogger.log('port_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

