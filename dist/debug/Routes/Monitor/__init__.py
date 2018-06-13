from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
from FlaskServer.Resources import en as resource
from FlaskServer.Routes.Monitor.modulation import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys
from FlaskServer.setting import *
from FlaskServer.serverstate import ServerState

from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#DEVICE_MODE = 'HBS'



class Monitor(Resource):

    if True:
        @jwt_required()
        def get(self):
            try:
                mode = ServerState.getDeviceMode(ServerState())
                if mode == 'HBS':
                   return onGetRequest_hbs()
                elif mode == 'HSU': 
                   return onGetRequest('monitor.json')
                else:
                   return onGetRequest('monitor_sn.json')
            except:
                return monitor_log_err("GET")




def monitor_route(req):
    if req.method == 'GET':
        try:
             return onGetRequest('monitor.json')
        except:
            return monitor_log_err("GET")

def monitor_route_hbs(req):
    if req.method == 'GET':
        try:
            return onGetRequest_hbs(req)
 
        except:
            return monitor_log_err("GET")

def monitor_route_SN(req):
    if req.method == 'GET':
        try:
            return onGetRequest('monitor_sn.json')
        except:
            return monitor_log_err("GET")



def onGetRequest(filename):
    #Load mapping JSON file
    #filename = 'monitor.json'
    data = load_mapping_json_file(os.path.join(__location__, filename))

    inflate_table(data['configMonitor']['wifiRssiTable'], 5)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))
            
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    # Config monitor values
    cast_to_int(ubus_attributes_dict,'maxEirp', 'totalTxPower')
            
    # Convert values in dict
    ubus_attributes_dict =  parse_and_convert_data(ubus_attributes_dict)
            
    # Build modulation string for hsu
    ubus_attributes_dict = build_modulation_string(ubus_attributes_dict)

    # Build response
    match_json(data, ubus_attributes_dict)

    parse_wifi_rssi_table(data['configMonitor'])

    parsed_data = None
    # Parse compressed data

    data = parse_hbs_compressed_static(ubus_attributes_dict , data)
    data = parse_hsu_compressed_monitor(ubus_attributes_dict , data)

    if parsed_data :
        data['installConfirmRequired'] = parsed_data['installConfirmRequired'] and parsed_data['installConfirmRequired'] == resource.unregistered
            
    if 'hsuCompressedMonitor' in ubus_attributes_dict and ubus_attributes_dict['hsuCompressedMonitor']:
        parsed_data = compresseddatahelper.parse_hbs_remote_monitor(data['hbsCompressedMonitor'])
          
    if parsed_data:
        for val in parsed_data:
            data[val] = parsed_data[val]


    data_to_clear_from_response = ['hsuCompressedMonitor' ,'hbsCompressedMonitor' , 'hbsCompressedStatic' , 'CurrentRateCBW' , 'CurrentRateGI']
    data = pop_data(data , data_to_clear_from_response)


    # Wrap data
    response_json = wrap_data(data)
    return response_json

def build_modulation_string(ubus_attributes_dict):
    if 'CurrentRateIdx' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateIdx'] and \
    'CurrentRateCBW' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateCBW'] and \
    'CurrentRateGI' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateGI']:
        currentRateIdx = ubus_attributes_dict['CurrentRateIdx']
        currentRateCBW = ubus_attributes_dict['CurrentRateCBW']
        currentRateGI = ubus_attributes_dict['CurrentRateGI']
        ubus_attributes_dict['CurrentRateIdx'] = createStringModulation(currentRateIdx, currentRateCBW, currentRateGI)
    return ubus_attributes_dict;

def onGetRequest_hbs():
    # Load mapping JSON file
    filename = 'monitor_hbs.json'
    data = load_mapping_json_file(os.path.join(__location__, filename))

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))
       
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json
            
    # Config monitor values
    cast_to_int(ubus_attributes_dict,'maxEirp', 'totalTxPower')
    # Convert values in dict
    ubus_attributes_dict =  parse_and_convert_data(ubus_attributes_dict)

    # Build response
    match_json(data, ubus_attributes_dict)

    parse_wifi_rssi_table(data['configMonitor'])

    parsed_data = None
    # Parse compressed data
       
    # Build modulation string for hsu
    if 'hbsAirLinkCompressedMonitor' in ubus_attributes_dict:
        parsed_data = compresseddatahelper.parse_HBS_monitor(data['hbsAirLinkCompressedMonitor'])
        parsed_data['CurrentRateIdx'] = get_current_rate_idx(parsed_data)
        parsed_data['hbsModulationRate'] = get_hbs_modulation_rate_for_hbs(parsed_data)

    if 'hsuCompressedMonitor' in ubus_attributes_dict and ubus_attributes_dict['hsuCompressedMonitor']:
        modulation_data = compresseddatahelper.parse_hbs_monitor_modulation(data['hbsAirLinkCompressedMonitor'])
        data['hbsModulationRate'] = modulation_data['hbsModulationRate']

    if 'hbsAirCompressedMonitor' in ubus_attributes_dict and ubus_attributes_dict['hbsAirCompressedMonitor']:
        parsed_air_data = compresseddatahelper.parse_HBS_air_monitor(data['hbsAirCompressedMonitor'])
                      
    if parsed_data:
        #data['installConfirmRequired'] = parsed_data['installConfirmRequired'] and parsed_data['installConfirmRequired'] == resource.unregistered
        for val in parsed_data:
            data[val] = parsed_data[val]

    if parsed_air_data:
        for val in parsed_air_data:
            data[val] = parsed_air_data[val]
            
    if 'hsuTput' in data:
        data['hsuTput'] = compresseddatahelper.calc_current_eth_tput(data['hsuTput'])

    if 'hsuLinkState' in data:
        data['hsuLinkState'] = converters.HSU_LINK_STATE[str(data['hsuLinkState'])]

    # Sanitize data
    data_to_clear_from_response = ['hbsAirLinkCompressedMonitor' , 'hsuCurrentRateCBW' , 'hsuCurrentRateGI' , 'hbsAirCompressedMonitor',
                                    'hsuCurrentRateIndex' , 'hbsCurrentRateCBW' , 'hbsCurrentRateGI' ,'hbsCurrentRateIndex' ]
    data = pop_data(data , data_to_clear_from_response)
    # Wrap data
    response_json = wrap_data(data)
    return response_json

def parse_wifi_rssi_table(raw_data):
    try:
        if raw_data['wifiRssiTable']:
            for idx, val  in enumerate(raw_data['wifiRssiTable']):
                if val['rssiAndMac']:
                    macAndRss = str(val['rssiAndMac'])
                    mac = macAndRss.split(',')[0]
                    rssi = macAndRss.split(',')[1]
                    raw_data['wifiRssiTable'][idx]['mac'] = mac
                    raw_data['wifiRssiTable'][idx]['rssi'] = rssi
    
                raw_data['wifiRssiTable'][idx].pop('rssiAndMac', None)
    except:
        radlogger.log('parse_wifi_rssi_table', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def parse_active_alarms_counter(indexes):
    if not indexes or indexes == 'none' or indexes == 'None':
        return 0
    return len(indexes.split(','))

def get_current_rate_idx(parsed_data):
    currentRateIdx = str(parsed_data['hsuCurrentRateIndex'])
    currentRateCBW = str(parsed_data['hsuCurrentRateCBW'])
    currentRateGI = str(parsed_data['hsuCurrentRateGI'])
    CurrentRateIdx = createStringModulation(currentRateIdx, currentRateCBW, currentRateGI)
    return CurrentRateIdx

def get_hbs_modulation_rate_for_hbs(parsed_data):
    currentRateIdxHBS = str(parsed_data['hbsCurrentRateIndex'])
    currentRateCBWHBS = str(parsed_data['hbsCurrentRateCBW'])
    currentRateGIHBS = str(parsed_data['hbsCurrentRateGI'])
    hbsModulationRate = createStringModulation(currentRateIdxHBS, currentRateCBWHBS, currentRateGIHBS)
    return hbsModulationRate

def get_hbs_modulation_rate(data) :
    modulation_data = compresseddatahelper.parse_hbs_monitor_modulation(data['hbsCompressedMonitor'])
    return modulation_data['hbsModulationRate']

def pop_data(data , names):
    for name in names:
        if name in data:
            data.pop(name)
    return data

def monitor_log_err(methodType):
    radlogger.log('monitor_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def parse_and_convert_data(ubus_attributes_dict):
     # Convert values in dict        
    if 'hbsAirState' in ubus_attributes_dict and ubus_attributes_dict['hbsAirState']:
        ubus_attributes_dict['hbsAirState'] = converters.HBS_AIR_STATE[ubus_attributes_dict['hbsAirState']]

    if 'realTimeAndDate' in ubus_attributes_dict and ubus_attributes_dict['realTimeAndDate']:
        ubus_attributes_dict['realTimeAndDate'] = compresseddatahelper.convert_oct_to_date(ubus_attributes_dict['realTimeAndDate'])

    if 'currentFrequency' in ubus_attributes_dict and ubus_attributes_dict['currentFrequency']:
        ubus_attributes_dict['currentFrequency'] = formatFrequency(ubus_attributes_dict['currentFrequency'])

    # Active Alarms Counter
    if 'activeAlarmsCounter' in ubus_attributes_dict:
        ubus_attributes_dict['activeAlarmsCounter'] = parse_active_alarms_counter(ubus_attributes_dict['activeAlarmsCounter'])

    if 'hsuLinkState' in ubus_attributes_dict and ubus_attributes_dict['hsuLinkState']:
        ubus_attributes_dict['hsuLinkState'] = converters.HSU_LINK_STATE[ubus_attributes_dict['hsuLinkState']]

    if 'hsuAirState' in ubus_attributes_dict and ubus_attributes_dict['hsuAirState']:
        ubus_attributes_dict['hsuAirState'] = converters.HSU_AIR_STATE[ubus_attributes_dict['hsuAirState']]

    if 'hsuTput' in ubus_attributes_dict and ubus_attributes_dict['hsuTput']:
        ubus_attributes_dict['hsuTput'] = compresseddatahelper.calc_current_eth_tput(ubus_attributes_dict['hsuTput'])


    if 'wifiApStatus' in ubus_attributes_dict and ubus_attributes_dict['wifiApStatus']:
        ubus_attributes_dict['wifiApStatus'] = converters.WIFI_AP_STATUS[ubus_attributes_dict['wifiApStatus']]


    return ubus_attributes_dict

def parse_hbs_compressed_static(ubus_attributes_dict , data): 
    # Parse compressed data
    if 'hbsCompressedStatic' in ubus_attributes_dict and ubus_attributes_dict['hbsCompressedStatic']:
        parsed_data = compresseddatahelper.parse_HBS_static(data['hbsCompressedStatic'])
        if parsed_data:
            for val in parsed_data:
                data[val] = parsed_data[val]

    return data

def parse_hsu_compressed_monitor(ubus_attributes_dict , data):
    if 'hsuCompressedMonitor' in ubus_attributes_dict and ubus_attributes_dict['hsuCompressedMonitor']:
        parsed_data = compresseddatahelper.parse_hsu_monitor(data['hsuCompressedMonitor'])
        data['hbsModulationRate'] = get_hbs_modulation_rate(data)
        if parsed_data:
            for val in parsed_data:
                data[val] = parsed_data[val]

    return data
