import FlaskServer.ubuscontroller as ubuscontroller
from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import app
from flask import send_file
import os, sys
import glob


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def debug_device_route(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'devicedebug.json'))
        
    flatten_data = flatten_json(data)

    if req.method == 'POST':
        try:
            
            # Get POST payload
            payload = req.get_json()          

            payload_dict = flatten_payload_to_dict(payload)

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            radlogger.log('debug_device_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json