from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import FlaskServer.attributeshelper as attributeshelper
import os, sys
from FlaskServer.setting import *

from FlaskServer.serverstate import ServerState
from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
NUM_OF_EXISTING_SBW = 7   # 5,10,20,40,80,7,14
EXISTING_CBW = [5,10,20,40,80,7,14]

class Radio(Resource):
    @jwt_required()
    def get(self):
        try:
            mode = ServerState.getDeviceMode(ServerState())
            if mode == 'HBS':
               return radio_route_hbs(request)  
            else:
               return radio_route_hsu(request)  
        except:
            return radio_log_err("GET")

    @jwt_required()
    def post(self):
        flatten_data = get_flatten_data('radio_hsu.json')
        try:
            return onPostRequest(request , flatten_data)
        except:
            return radio_log_err("POST")


def radio_route_hsu(req):
    flatten_data = get_flatten_data('radio_hsu.json')
    if req.method == 'GET':
        try:
            return onGetRequest_hsu(req , flatten_data)
        except:
            return radio_log_err("GET")
    if req.method == 'POST':
        try:  
            return onPostRequset(req , flatten_data)
        except:
             return radio_log_err("POST")

def radio_route_hbs(req):
    flatten_data = get_flatten_data('radio_hbs.json')
    if req.method == 'GET':
        try:
            return onGetRequest_hbs(req , flatten_data)
        except:
            return radio_log_err("GET")
    if req.method == 'POST':
        try:
            return onPostRequset(req , flatten_data)
        except:
            return radio_log_err("POST")

def onGetRequest_hsu(req , flatten_data):
    # Load mapping JSON file
    data = get_data('radio_hsu.json')
    attributes_list = [attributeshelper.CAPABILITY_BITMASK]             
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    latitude = '0'
    longitude = '0'

    capabilityBitmask     = ubus_attributes_dict[attributeshelper.CAPABILITY_BITMASK[ubuscontroller.NAME_KEY]]
    isDynamicCbwSupported = getFetureSupportByCapability(capabilityBitmask, consts.CAPABILITY_INDEX_DYNAMIC_CHANNEL_BANDWIDTH)

    available_cbw = get_available_cbw()

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    # Casting
    cast_to_int_divide_by_factor(ubus_attributes_dict, 1000, 'currentCbw')
    cast_to_int_divide_by_factor(ubus_attributes_dict, 10, 'antennaGain', 'cableLoss', 'maxAntennaGain', 'minAntennaGain')
    cast_to_int(ubus_attributes_dict, 'minTxPower', 'maxTxPower', 'desiredTxPower')

    if isDynamicCbwSupported:
       ubus_attributes_dict = set_dynamic_cbw_support(ubus_attributes_dict , available_cbw)

    data = get_converters_data_for_ubus(ubus_attributes_dict , data)
   
    response_json = wrap_data(data)
    return response_json

def onGetRequest_hbs(req , flatten_data):
    # Load mapping JSON file
    data = get_data('radio_hbs.json')
    attributes_list = [attributeshelper.CAPABILITY_BITMASK]   
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    latitude = '0'
    longitude = '0'

    capabilityBitmask     = ubus_attributes_dict[attributeshelper.CAPABILITY_BITMASK[ubuscontroller.NAME_KEY]]
    isDynamicCbwSupported = getFetureSupportByCapability(capabilityBitmask, consts.CAPABILITY_INDEX_DYNAMIC_CHANNEL_BANDWIDTH)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    # Casting
    cast_to_int_divide_by_factor(ubus_attributes_dict, 1000, 'currentCbw')
    cast_to_int_divide_by_factor(ubus_attributes_dict, 10, 'antennaGain', 'cableLoss', 'maxAntennaGain', 'minAntennaGain')
    cast_to_int(ubus_attributes_dict, 'minTxPower', 'maxTxPower', 'desiredTxPower')

    data = get_converters_data_for_ubus(ubus_attributes_dict , data)
        
    response_json = wrap_data(data)
    return response_json

def onPostRequset(req , flatten_data):               
    # Get POST payload
    payload = req.get_json()
    payload_dict = flatten_payload_to_dict(payload)

    # Automatic CBW support
    if 'currentCbw' in payload_dict and 'Auto' in payload_dict['currentCbw']:
        payload_dict['currentCbw'] = 20
    # End Of Automatic CBW support

    cast_to_int_multiply_by_factor(payload_dict, 10, 'cableLoss', 'antennaGain')
    cast_to_int_multiply_by_factor(payload_dict, 1000, 'currentCbw')

    flatten_data = getReadyForSetInUbus(payload_dict , flatten_data)

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

    if 'frequencies' in payload_dict:
        isSetSuccess = setBandFreq(payload_dict)
            
    response_json = wrap_data(payload)

    return response_json

def getReadyForSetInUbus(payload_dict , flatten_data):
    for attr in flatten_data:
        if attr[ubuscontroller.NAME_KEY] in payload_dict:
            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
    return flatten_data

#this function will return object that contain :
#minFreq : represent the min value of the possible freq
#maxFreq : represent the max value of the possible freq
#resolution : represent the step value between possible freq
#numOfFreq :represent the total freq number
def get_min_max_and_resolution():
    attributes_list = [attributeshelper.alignment_min_freq,
                    attributeshelper.alignment_max_freq,
                    attributeshelper.alignment_resolution]

    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    minFreq    = ubus_attributes_dict[attributeshelper.alignment_min_freq['name']]
    maxFreq    = ubus_attributes_dict[attributeshelper.alignment_max_freq['name']]
    resolution = ubus_attributes_dict[attributeshelper.alignment_resolution['name']]

    data = {}
    data['minFreq']    = int(minFreq)
    data['maxFreq']    = int(maxFreq)
    data['resolution'] = int(resolution)
    data['numOfFreq']  = ((data['maxFreq'] - data['minFreq'])/data['resolution']) + 1

    return data

#this function will return array of all the possible freq
def create_freq_array(min , numOfFreq , resulation):
    freqArray = []
    for i in range(0, numOfFreq):
        freq = min + (i * resulation)
        freqArray.append(str(freq))

    return freqArray

#this function pasre the '00101001010' string value from ODU to arary of selected freqs.
def parse_acs_freq(data_raw):
    data = get_min_max_and_resolution()
    all_freq_array = create_freq_array(data['minFreq'] , data['numOfFreq'] , data['resolution'])

    possible_freq_list = []

    for idx, val in enumerate(data_raw):
        if val == '1':
            possible_freq_list.append(all_freq_array[idx])

    return possible_freq_list

def setBandFreq(req):

    payload_dict =  {}

    payload = req
    payload_dict = payload

    frequenciesList = payload_dict['frequencies']
    if "," in frequenciesList:
      frequenciesList = frequenciesList.split(",")
    else:
      frequenciesList = [frequenciesList]

    isShouldResync  = payload_dict['isShouldResync']


    data = get_min_max_and_resolution()
    resolution = data['resolution']
    numOfFreq = data['numOfFreq']
    minFreq = data['minFreq']
   
    newAllowableChannelsStr = build_allowable_channels_str(numOfFreq , frequenciesList , minFreq)

    attributes_list = [attributeshelper.alignment_available_channels_str]
            
    attributes_list[0]['value'] = newAllowableChannelsStr

    # Sent list to ubus
    ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)

    if isShouldResync:
        resync()

    success = bool(ubus_attributes_dict)

    return success

def resync():
    try:
        command = attributeshelper.RESYNC_COMMAND
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        response_json = wrap_data({}, "Done")
        return response_json

    except:
        radlogger.log('resync method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def build_allowable_channels_str(numOfFreq , frequenciesList, minFreq ):
    currentIterationChannel = minFreq
    channelFound = FALSE
    if frequenciesList == "all":
        for channelIndex in range(0, numOfFreq):
            newAllowableChannelsStr += '1'
    else:
        for channelIndex in range(0, numOfFreq):
            channelFound = FALSE
            for desiredChannelIndex in range(0, len(frequenciesList)):
                if int(frequenciesList[desiredChannelIndex]) == currentIterationChannel:
                    channelFound = TRUE
                    break
            currentIterationChannel = currentIterationChannel + resolution
            newAllowableChannelsStr += '1' if channelFound else '0'

    return newAllowableChannelsStr;

def get_converters_data_for_ubus(ubus_attributes_dict , data):

    if 'currentFrequency' in ubus_attributes_dict and ubus_attributes_dict['currentFrequency']:
        currentFrequencyAsNumber = ubus_attributes_dict['currentFrequency']
        ubus_attributes_dict['currentFrequency'] = formatFrequency(ubus_attributes_dict['currentFrequency'])
                
    if 'antennaType' in ubus_attributes_dict and ubus_attributes_dict['antennaType']:
        ubus_attributes_dict['antennaType'] = converters.ANTENNA_TYPE[ubus_attributes_dict['antennaType']]

    if 'antennaConnectionType' in ubus_attributes_dict and ubus_attributes_dict['antennaConnectionType']:
        ubus_attributes_dict['antennaConnectionType'] = converters.ANTENNA_CONNECTION_TYPE[ubus_attributes_dict['antennaConnectionType']]

    if 'attachedAntennaIndication' in ubus_attributes_dict and ubus_attributes_dict['attachedAntennaIndication']:
        ubus_attributes_dict['attachedAntennaIndication'] = converters.ATTACHED_ANTENNA_INDICATION[ubus_attributes_dict['attachedAntennaIndication']]
             
    if 'alignmentAvailableChannelsStr' in ubus_attributes_dict:
        ubus_attributes_dict['alignmentAvailableChannelsStr'] = parse_acs_freq(ubus_attributes_dict['alignmentAvailableChannelsStr'])

    if 'HbsAirConfBEPercentage' in ubus_attributes_dict:
        down_link = ubus_attributes_dict['HbsAirConfBEPercentage'].split('|')[0]
        ubus_attributes_dict['HbsAirConfBEPercentage'] = HbsAirConfBEPercentage_converter(down_link)
                     
    tx_ratio = ''
    if 'hsuCompressedMonitor' in ubus_attributes_dict:
        parsed_data = compresseddatahelper.parse_hbs_remote_monitor(ubus_attributes_dict['hsuCompressedMonitor'])
        tx_ratio = parsed_data['txRatio']


    if 'hsuType' in ubus_attributes_dict and ubus_attributes_dict['hsuType']:

        if ubus_attributes_dict['hsuType'] == '1':
            data['options']['hsuAvailableTypes'] = ['Mobility']

        if ubus_attributes_dict['hsuType'] == '2' or ubus_attributes_dict['hsuType'] == '7':
            data['options']['hsuAvailableTypes'] = ['Fixed' , 'Nomadic']

        if ubus_attributes_dict['hsuType'] == '8':
            data['options']['hsuAvailableTypes'] = ['Fixed']

        ubus_attributes_dict['hsuType'] = converters.SERVICE_HSU_TYPE[ubus_attributes_dict['hsuType']]
                
    if 'geoLocation' in ubus_attributes_dict and ubus_attributes_dict['geoLocation']:
        latLon = ubus_attributes_dict['geoLocation'].split(',')
        if (len(latLon) > 1):
            latitude = latLon[0]
            longitude = latLon[1]
            data['latitude'] = latitude
            data['longitude'] = longitude

    match_json(data, ubus_attributes_dict)
    available_cbw = get_available_cbw()
    data['options']['cbwList'] = available_cbw
            
    data.pop('geoLocation', None)
    data.pop('hsuCompressedMonitor', None)

    if tx_ratio != '':
        data['txRatio'] = tx_ratio

    if currentFrequencyAsNumber:
        data['currentFrequencyAsNumber'] = currentFrequencyAsNumber
   
    return data

def HbsAirConfBEPercentage_converter(val):
    res = 'Mixed CIR/BE';
    if (val == 100):
        res = 'BE Only'
    if (val == 0):
        res = 'CIR Only'
    return res

def set_dynamic_cbw_support(ubus_attributes_dict , available_cbw ):
    cbw_in_auto_mode = ''
    for cbw in available_cbw:
        if cbw > 10:
            cbw_in_auto_mode = cbw_in_auto_mode + str(cbw) + "/"
    cbw_in_auto_mode =  cbw_in_auto_mode[:-1]
    cbw_in_auto_mode = 'Auto(' + cbw_in_auto_mode +')'
    available_cbw = ['10', cbw_in_auto_mode]
    # Set current CBW in auto mode
    if ubus_attributes_dict['currentCbw'] > 10:
        ubus_attributes_dict['currentCbw'] = cbw_in_auto_mode
    return ubus_attributes_dict

def radio_log_err(methodType):
    radlogger.log('radio_route ' + methodType + 'method.', sys.exc_info())
    response_json = wrap_data({}, error="Error occurred")
    return response_json

def get_flatten_data(file_name):
    data = load_mapping_json_file(os.path.join(__location__, file_name))  
    flatten_data = flatten_json(data)
    return flatten_data

def get_data(file_name):
    data = load_mapping_json_file(os.path.join(__location__, file_name))  
    return data

def get_available_cbw():
    available_cbw = []
    cbw_table_data = load_mapping_json_file(os.path.join(__location__, 'cbwTable.json'))
    inflate_table(cbw_table_data, NUM_OF_EXISTING_SBW, 1)
    flatten_cbw_table_data = flatten_json(cbw_table_data)
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_cbw_table_data)
    for index in range(1, NUM_OF_EXISTING_SBW):
        key = 'cbwAvailable_' + str(index)
        if key in ubus_attributes_dict:
            val = int(ubus_attributes_dict[key])
            if (val > 1):
                available_cbw.append(EXISTING_CBW[index-1])
    return available_cbw