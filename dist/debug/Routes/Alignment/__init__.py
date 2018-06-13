import string, random, uuid, os, sys
import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import converters
from threading import Timer
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.Monitor.modulation import *
from FlaskServer.Resources import en as resource
from FlaskServer.serverstate import ServerState
from flask import request
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


# Alignment routes
ALIGNMNET_MEASURING_URL         = 'measuring'
ALIGNMNET_BEST_POSITION_URL     = 'best-position'
ALIGNMNET_POINTER_LOCATION_URL  = 'pointer-location'
ALIGNMNET_ACTION_URL            = 'action'
ALIGNMNET_FINE_ALIGNMNET_URL    = 'fine-alignment'
ALIGNMNET_GET_ALL_BANDS_URL     = 'get-bands'
ALIGNMNET_SET_BANDS_URL         = 'set-band'
ALIGNMNET_LINK_EVAL_URL         = 'evaluation'
ALIGNMNET_EVAL_RESULTS_URL      = 'evaluation-results'
ALIGNMNET_INIT_VALUES           = 'init-values'
ALIGNMNET_LINK_DATA             = 'link-data'
ALIGNMNET_SPEED_TEST            = 'speed-test'


class Alignment(Resource):
    @jwt_required()
    def get(self , op_name , action=None):
        name = op_name
        mode = ServerState.getDeviceMode(ServerState())
        if name == ALIGNMNET_MEASURING_URL:
            return alignmentTable(request)

        if name == ALIGNMNET_BEST_POSITION_URL:
            return getBestPosition(request)

        if name == ALIGNMNET_POINTER_LOCATION_URL:
            return pointerLocation(request) 

        if name == ALIGNMNET_GET_ALL_BANDS_URL:
            return alignmentGetAllBands(request) 

        if name == ALIGNMNET_FINE_ALIGNMNET_URL:
            return getFineAligmentResults(request) 

        if name == ALIGNMNET_EVAL_RESULTS_URL:
            return getAlignmentEvalResults(request) 
         
        if name == ALIGNMNET_INIT_VALUES:
            if mode == 'HBS':
                return getInitialValues_hbs(request)
            else:
                return getInitialValues_hsu(request)
        if name == ALIGNMNET_LINK_DATA:
            return getLinkData(request)
        
        if name == ALIGNMNET_SPEED_TEST:
            return alignment_speed_test(action , request)   

    @jwt_required()
    def post(self , op_name , action=None):
        name = op_name
        if name == ALIGNMNET_ACTION_URL:
            return alignmentActionInvoker(action , request)

        if name == ALIGNMNET_LINK_EVAL_URL:
            return evaluationActionInvoker(action , request) 

        if name == ALIGNMNET_SET_BANDS_URL:
            return alignmentSetBand(request) 

        if name == ALIGNMNET_SPEED_TEST:
            return alignment_speed_test(action , request) 
         


GEN3 = 'Gen3'
GEN4 = 'Gen4'

#Do not change order !
HBS_PARAMS_ARRAY = ['sectorType',             #0
                    'antennaAngle',           #1
                    'antennalElevation',      #2
                    'sectorDirection',        #3
                    'antennaBeamwidth',       #4
                    'channel',                #5
                    'channelBw',              #6
                    'bestRSS',                #7
                    'sectorID',               #8
                    'availableResourcesDL',   #9
                    'availableResourcesUL',   #10
                    'bestEffortEnabled',      #11
                    'longitude',              #12
                    'latitude',               #13
                    'sectorIdMatched']        #14

alignmentSamplesState = {'AllChannelsScanned'                    : 1,
                         'AnySectorsExist'                       : 2,
                         'SectorWithNetworkIdExists'             : 4,
                         'SectorWithSpecificSectorIdExists'      : 8,
                         'RequiredSectorHasFreeAssuredResources' : 16,
                         'RequiredSectorHasFreeBEEntries'        : 32 }

alignmentChangeBandCbwArray = [ 'channelBW5Freq', 
                                'channelBW10Freq',
                                'channelBW20Freq',
                                'channelBW40Freq',
                                'channelBW80Freq',
                                'channelBW7Freq',
                                'channelBW14Freq']

linkStatesHash = {1 : 'noSync',
                  2 : 'violated',
                  3 : 'syncUnregistered',
                  4 : 'syncRegistered',
                  5 : 'authenticationError',
                  6 : 'swUpgradeRequired',
                  7 : 'syncRegisteredPassive',
                  8 : 'syncRegisteredALP' }

#1: Start Raw Alignment
#2: Finish Raw Alignment
#3: Restart Alignment
#4: Skip Alignment
#5: Start Sync Alignment
#6: Complete Alignment
#7: Start GYRO
#8: Stop GYRO
#9: Set Antenna
ALIGNMENT_COMMANDS = {'start': 1, 'finish': 2, 'restart': 3, 'skip': 4, 'startSync': 5, 'complete': 6, 'startGyro': 7, 'stopGyro': 8, 'setAntenna': 9 , 'startSpeedTest': 10, 'stopSpeedTest': 11}
EVALUATION_COMMANDS = {'start': 1, 'stop': 2}
ANTENNA_TX_MODES = {'mimo': 1, 'diversity': 2, 'autoSelection': 3}
VERTICAL_CELLS_NAMES = {1: 'high', 2: 'middle', 3: 'low'}
NUM_OF_ELEVATION_COUNT = 3
VERTICAL_START_ANGLE = -15
VERTICAL_END_ANGLE = 15
VERTICAL_SCAN_STEP = 10

GLOBAL_HASH = {}
GLOBAL_HASH['tableCellCount'] = 0
GLOBAL_HASH['horizontalStartAngle'] = 0
GLOBAL_HASH['horizontalEndAngle'] = 0
GLOBAL_HASH['horizontalScanStep'] = 0
GLOBAL_HASH['elevationBeamwidth'] = 10

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#interfaces definitions, add here for every new call
############## TRUE DATA ##############

# /api/v1/alignment/pointer-location
def pointerLocation(req):
    if req.method == 'GET':

        if GLOBAL_HASH['tableCellCount'] == 0:
            print('pointerLocation - tableCell Count is 0')
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        cursorLocation = calculateCursorLocation()
        if not cursorLocation:
            print('pointerLocation - unable to calculate cursor Location')
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        responceDict = {}
        responceDict['cursorLocation'] = cursorLocation

        response_json = wrap_data(responceDict)
        return response_json

# /api/v1/alignment/best-position
def getBestPosition(req):
    if req.method == 'GET':
        attributes_list = []
        attributes_list = [attributeshelper.alignment_num_of_sectors_found]
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        respStr = ubus_attributes_dict[attributeshelper.alignment_num_of_sectors_found['name']]
        numberOfHbsDevices = int(respStr)

        if numberOfHbsDevices == 0:
            return None

        attributes_list = []
        for index in range(1, numberOfHbsDevices + 1):
            tempAttr = copy.deepcopy(attributeshelper.alignment_full_sectors_stats)
            tempAttr['index'] = index
            tempAttr['name'] = tempAttr['name'] + '_' + str(index)
            attributes_list.append(tempAttr)

        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if ubus_attributes_dict == 0:
            return None

        responceDict = {}
        responceDict['HBS'] = []
        for index in range(1, numberOfHbsDevices + 1):
            hbs = ubus_attributes_dict[attributeshelper.alignment_full_sectors_stats['name'] + '_' + str(index)]
            hbsData = []
            hbsData = hbs.split(',')
            tempDict = {}
            for count in range(0, len(hbsData)):
                tempDict[HBS_PARAMS_ARRAY[count]] = hbsData[count]
            
            #sectorType
            tempDict[HBS_PARAMS_ARRAY[0]]  = GEN3 if  tempDict[HBS_PARAMS_ARRAY[0]] == 1 else GEN4
            #bestEffortEnabled
            tempDict[HBS_PARAMS_ARRAY[11]] = bool(int(tempDict[HBS_PARAMS_ARRAY[11]]))
            #sectorIdMatched
            tempDict[HBS_PARAMS_ARRAY[14]] = bool(int(tempDict[HBS_PARAMS_ARRAY[14]]))

            #antennaAngle           #1
            tempDict[HBS_PARAMS_ARRAY[1]] = int(tempDict[HBS_PARAMS_ARRAY[1]])
            #antennalElevation      #2
            tempDict[HBS_PARAMS_ARRAY[2]] = int(tempDict[HBS_PARAMS_ARRAY[2]])
            #sectorDirection        #3
            tempDict[HBS_PARAMS_ARRAY[3]] = int(tempDict[HBS_PARAMS_ARRAY[3]])
            #antennaBeamwidth       #4
            tempDict[HBS_PARAMS_ARRAY[4]] = int(tempDict[HBS_PARAMS_ARRAY[4]])
            #channel                #5
            tempDict[HBS_PARAMS_ARRAY[5]] = int(tempDict[HBS_PARAMS_ARRAY[5]])
            #channelBw              #6
            tempDict[HBS_PARAMS_ARRAY[6]] = int(tempDict[HBS_PARAMS_ARRAY[6]])
            #bestRSS                #7
            tempDict[HBS_PARAMS_ARRAY[7]] = int(tempDict[HBS_PARAMS_ARRAY[7]])
            #availableResourcesDL   #9
            tempDict[HBS_PARAMS_ARRAY[9]] = int(tempDict[HBS_PARAMS_ARRAY[9]])
            #availableResourcesUL   #10
            tempDict[HBS_PARAMS_ARRAY[10]] = int(tempDict[HBS_PARAMS_ARRAY[10]])
            #latitude               #12
            tempDict[HBS_PARAMS_ARRAY[12]] = float(tempDict[HBS_PARAMS_ARRAY[12]])
            #longitude              #13
            tempDict[HBS_PARAMS_ARRAY[13]] = float(tempDict[HBS_PARAMS_ARRAY[13]])

            #Get cursor location using antennaAngle and antennalElevation 
            tempDict['cursorLocation'] = getCursorLocation(tempDict[HBS_PARAMS_ARRAY[1]], tempDict[HBS_PARAMS_ARRAY[2]])

            #remove antennaAngle and antennalElevation
            tempDict.pop(HBS_PARAMS_ARRAY[1])
            tempDict.pop(HBS_PARAMS_ARRAY[2])

            responceDict['HBS'].append(tempDict)

        response_json = wrap_data(responceDict)
        return response_json

# /api/v1/alignment/action/<action>
def alignmentActionInvoker(action, req):
    if req.method != 'POST':
        response_json = wrap_data({}, error="Invalid command")
        return response_json

    radlogger.log(req.data, None)


    if action == 'set-antenna':

        success = setAntenna(req.get_json())
        if success:
            response_json = wrap_data({}, "Done")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set antenna")
            return response_json

    if action == 'set-final-data':
        success = setFinalData(req.get_json())
        if success:
            response_json = wrap_data({}, "Done")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set final data")
            return response_json

    if action == 'skip':
        success = setFullChannelsAllowed()
        if not success:
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if ALIGNMENT_COMMANDS.has_key(action):

        if action == 'start' or action == 'restart' or action == 'startGyro':
            success = initAlignmentColomnsCount()
            if not success:
                response_json = wrap_data({}, error="Error occurred")
                return response_json

        if action == 'startSync':
            payload = req.get_json()
            if 'sectorId' in payload and (len(payload['sectorId']) >= 8 or len(payload['sectorId']) == 0):
                set_ssid_command =  copy.deepcopy(attributeshelper.alignment_set_ssid)
                set_ssid_command['value'] = payload['sectorId']
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(set_ssid_command)
            else:
                response_json = wrap_data({}, error="Wrong data was passed, no sectorId")
                return response_json


        attributes_list = []
        #payload_dict = flatten_payload_to_dict(payload)

        attributes_list = [attributeshelper.alignment_commanding]
            
        attributes_list[0]['value'] = ALIGNMENT_COMMANDS[action]

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)

        # in case of error ubus_attributes_dict will be {}
        success = bool(ubus_attributes_dict)

        if success:
            response_json = wrap_data({}, "Done")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set command")
            return response_json
    else:
        response_json = wrap_data({}, error="Invalid command")
        return response_json

# /api/v1/alignment/speed-test/<action>
def alignment_speed_test(action, req):
    if req.method == 'GET' and action == 'data':
        try:       
            attributes_list = []

            attributes_list = [attributeshelper.HBS_COMPRESSED_MONITOR,
                               attributeshelper.alignment_link_state,
                               attributeshelper.CURRENT_RATE_IDX,
                               attributeshelper.CURRENT_RATE_CBW,
                               attributeshelper.CURRENT_RATE_GI]

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            parsed_data = compresseddatahelper.parse_speed_test(ubus_attributes_dict[attributeshelper.HBS_COMPRESSED_MONITOR['name']])
            modulation_data = compresseddatahelper.parse_hbs_monitor_modulation(ubus_attributes_dict[attributeshelper.HBS_COMPRESSED_MONITOR['name']])
            linkStateNumber = ubus_attributes_dict[attributeshelper.alignment_link_state['name']]

            # Build modulation string for hsu
            if 'CurrentRateIdx' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateIdx'] and \
               'CurrentRateCBW' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateCBW'] and \
               'CurrentRateGI' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateGI']:
                    currentRateIdx = ubus_attributes_dict['CurrentRateIdx']
                    currentRateCBW = ubus_attributes_dict['CurrentRateCBW']
                    currentRateGI = ubus_attributes_dict['CurrentRateGI']
                    CurrentRateIdx = createStringModulation(currentRateIdx, currentRateCBW, currentRateGI)

            response = {}
            response['UpLink'] = parsed_data['ulSpeed']
            response['DownLink'] = parsed_data['dlSpeed']
            response['LinkState'] = linkStatesHash[int(linkStateNumber)]
            response['CurrentRateIdx'] = CurrentRateIdx
            response['hbsModulationRate'] = modulation_data['hbsModulationRate']
            
            response_json = wrap_data(response)
            return response_json
        except:
            radlogger.log('speed_test GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:

            if action == 'start':
                # Start speed test, every 30 seconds (client side)
                command = attributeshelper.START_SPEED_TEST
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
                response_json = wrap_data({}, "Speed Test Initiated")
                return response_json

            elif action == 'stop':
                # Parameter to enable Evaluation process (1-On, 2-Off)
                command = attributeshelper.STOP_SPEED_TEST
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
                response_json = wrap_data({}, "Speed Test Stopped")
                return response_json
            else:
                response_json = wrap_data({}, error="Invalid command")
                return response_json
        except:
            radlogger.log('speed_test POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def startSpeedTest(data):
    try:
        # Start speed test, every 30 seconds (client side)
        command = attributeshelper.START_SPEED_TEST
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
        response_json = wrap_data({}, "Speed Test Initiated")
        return response_json
    except:
        radlogger.log('startSpeedTest method.', sys.exc_info())
        return None

def stopSpeedTest(data):
    try:
        command = attributeshelper.STOP_SPEED_TEST
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
        response_json = wrap_data({}, "Speed Test Stopped")
        return response_json
    except:
        radlogger.log('stopSpeedTest method.', sys.exc_info())
        return None

def setAntenna(data):
    payload = {}
    payload = data
    if (payload == None):
        radlogger.log('setAntenna: No Data is passed.')
        return None

    try:

        payload_dict = flatten_payload_to_dict(payload)
        flatten_data = flatten_json_name(load_mapping_json_file(os.path.join(__location__, 'setantenna.json')))
        integrated = False
        remove_dict1 = {}
        remove_dict2 = {}       
        remove_dict3 = {}
        resyncRequired = False;
        for attr in flatten_data:
            if attr[ubuscontroller.NAME_KEY] in payload_dict:
                attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]
                if attr[ubuscontroller.NAME_KEY].startswith( 'antennaConnectionType' ):
                    
                    attr[ubuscontroller.VALUE_KEY] = converters.ANTENNA_CONNECTION_TYPE[payload_dict[attr[ubuscontroller.NAME_KEY]]]  
                    currentAntennaConnectionType = converters.ANTENNA_CONNECTION_TYPE[payload_dict[attr[ubuscontroller.NAME_KEY]]]
                    remove_dict1 =  {'attr': 1237, 'index': 0, 'name': 'antennaConnectionType', 'object': 36864, 'value': currentAntennaConnectionType}
                    alignment_antennaConnectionType_obj = [attributeshelper.alignment_antennaConnectionType]
                    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(alignment_antennaConnectionType_obj)
                    if not bool(ubus_attributes_dict):
                        radlogger.log('setAntenna method. Empty Previouse Antenna Connection Type', sys.exc_info())
                        return None
                    prevAntennaConnectionType = ubus_attributes_dict[attributeshelper.alignment_antennaConnectionType[ubuscontroller.NAME_KEY]]
                    if (prevAntennaConnectionType != currentAntennaConnectionType):
                        resyncRequired = True
                    if (payload_dict[attr[ubuscontroller.NAME_KEY]] == resource.antenna_con_type_embedded_integrated):
                        integrated = True
                if attr[ubuscontroller.NAME_KEY].startswith( 'antennaGain' ):
                    remove_dict2 =  {'attr': 918, 'index': 0, 'name': 'antennaGain', 'object': 36864, 'value': payload_dict[attr[ubuscontroller.NAME_KEY]]}
                if attr[ubuscontroller.NAME_KEY].startswith( 'cableLoss' ):
                    remove_dict3 =  {'attr': 919, 'index': 0, 'name': 'cableLoss', 'object': 36864, 'value': payload_dict[attr[ubuscontroller.NAME_KEY]]}

        if (integrated):
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(remove_dict1)
        else:
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(remove_dict1)
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(remove_dict2)
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(remove_dict3)

        if resyncRequired:
            resync()

        success = bool(ubus_attributes_dict)

        return success

    except:
        radlogger.log('setAntenna method.', sys.exc_info())
        return None

def setFinalData(data):

    payload = {}
    payload = data
    if (payload == None):
        radlogger.log('setFinalData: No Data is passed.')
        return None

    try:
        HsuInstallationConfirmation = '103'

        if ('installationSrvType' in payload):
            if (payload['installationSrvType'] in converters.SERVICE_TYPE_CONVERTER):
                payload['installationSrvType'] = converters.SERVICE_TYPE_CONVERTER[payload['installationSrvType']]
            else:
                radlogger.log('invalid installationSrvType')
                return None

        if 'confirmInstallation' in payload:
            if payload['confirmInstallation'] == 'true':
                payload['confirmInstallation'] = HsuInstallationConfirmation
            else:
                payload.pop('confirmInstallation');


        payload_dict = flatten_payload_to_dict(payload)

        setFinalData_dict = load_mapping_json_file(os.path.join(__location__, 'setFinalData.json'))

        set_dict = []

        all_payload_keys = payload_dict.keys()
        for key in all_payload_keys:
            if key in setFinalData_dict:
                item = setFinalData_dict[key]
                item['value'] = payload_dict[key]
                set_dict.append(item)

        success = setFullChannelsAllowed()
        if not success:
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        attributes_list = []

        geoLocation = copy.deepcopy(setFinalData_dict['geoLocation'])
        confirmInstallation = copy.deepcopy(setFinalData_dict['confirmInstallation'])

        geoLocation['value'] = payload_dict['latitude'] + ',' + payload_dict['longitude']
        set_dict.append(geoLocation)



        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(set_dict)

        success = bool(ubus_attributes_dict)
        return success
    except:
        radlogger.log('setFinalData method.', sys.exc_info())
        return None

# /api/v1/alignment/evaluation/<action>
def evaluationActionInvoker(action, req):
    if req.method != 'POST':
        response_json = wrap_data({}, error="Invalid command")
        return response_json

    radlogger.log(req.data, None)

    if EVALUATION_COMMANDS.has_key(action):
        set_evaluation_commanding =  copy.deepcopy(attributeshelper.evaluation_commanding)
        REMOTE_EVAL_ENUM = '101'
        orderStr = str(REMOTE_EVAL_ENUM) + ',' + str(EVALUATION_COMMANDS[action]) + ',' + str(ANTENNA_TX_MODES['autoSelection'])
        set_evaluation_commanding['value'] = orderStr

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(set_evaluation_commanding)

        #in case of error ubus_attributes_dict will be {}
        success = bool(ubus_attributes_dict)

        if success:
            response_json = wrap_data({}, "Done")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set value")
            return response_json
    else:
        response_json = wrap_data({}, error="Invalid command")
        return response_json

# /api/v1/alignment/measuring
def alignmentTable(req):
    if req.method == 'GET':

        if GLOBAL_HASH['tableCellCount'] == 0:
            print('alignmentTable - table CellCount is 0')
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        cursorLocation = calculateCursorLocation()
        if not cursorLocation:
            return None

        attributes_list = []
        attributes_list = [attributeshelper.alignment_immediate_results_table]

        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        table = ubus_attributes_dict[attributeshelper.alignment_immediate_results_table['name']]

        tolalSamples = []
        tolalSamples = table.split('|')

        if len(tolalSamples) < 3:
            return None

        numberOfSnaps = len(tolalSamples) / 3


        if ubus_attributes_dict == 0:
            return None

        responceDict = {}
        responceDict['samples'] = []
        responceDict['cursorLocation']  = cursorLocation

        for index in range(0, numberOfSnaps):

            lowSnap  = tolalSamples[index]
            medSnap  = tolalSamples[numberOfSnaps + index]
            highSnap = tolalSamples[numberOfSnaps * 2 + index]

            data = [lowSnap, medSnap, highSnap]

            resultData = {}
            resultData['elevationLow']    = {}
            resultData['elevationMedium'] = {}
            resultData['elevationHigh']   = {}

            resultData['elevationLow']['scanned']                = bool(int(data[0]) & alignmentSamplesState['AllChannelsScanned'])
            resultData['elevationLow']['sectorFound']            = bool(int(data[0]) & alignmentSamplesState['AnySectorsExist'])
            resultData['elevationLow']['sectorWithNetwork']      = bool(int(data[0]) & alignmentSamplesState['SectorWithNetworkIdExists'])
            resultData['elevationLow']['sectorWithSpecSectorId'] = bool(int(data[0]) & alignmentSamplesState['SectorWithSpecificSectorIdExists'])
            resultData['elevationLow']['cirResourcesExist']      = bool(int(data[0]) & alignmentSamplesState['RequiredSectorHasFreeAssuredResources'])
            resultData['elevationLow']['beResourcesExist']       = bool(int(data[0]) & alignmentSamplesState['RequiredSectorHasFreeBEEntries'])

            resultData['elevationMedium']['scanned']                = bool(int(data[1]) & alignmentSamplesState['AllChannelsScanned'])
            resultData['elevationMedium']['sectorFound']            = bool(int(data[1]) & alignmentSamplesState['AnySectorsExist'])
            resultData['elevationMedium']['sectorWithNetwork']      = bool(int(data[1]) & alignmentSamplesState['SectorWithNetworkIdExists'])
            resultData['elevationMedium']['sectorWithSpecSectorId'] = bool(int(data[1]) & alignmentSamplesState['SectorWithSpecificSectorIdExists'])
            resultData['elevationMedium']['cirResourcesExist']      = bool(int(data[1]) & alignmentSamplesState['RequiredSectorHasFreeAssuredResources'])
            resultData['elevationMedium']['beResourcesExist']       = bool(int(data[1]) & alignmentSamplesState['RequiredSectorHasFreeBEEntries'])

            resultData['elevationHigh']['scanned']                = bool(int(data[2]) & alignmentSamplesState['AllChannelsScanned'])
            resultData['elevationHigh']['sectorFound']            = bool(int(data[2]) & alignmentSamplesState['AnySectorsExist'])
            resultData['elevationHigh']['sectorWithNetwork']      = bool(int(data[2]) & alignmentSamplesState['SectorWithNetworkIdExists'])
            resultData['elevationHigh']['sectorWithSpecSectorId'] = bool(int(data[2]) & alignmentSamplesState['SectorWithSpecificSectorIdExists'])
            resultData['elevationHigh']['cirResourcesExist']      = bool(int(data[2]) & alignmentSamplesState['RequiredSectorHasFreeAssuredResources'])
            resultData['elevationHigh']['beResourcesExist']       = bool(int(data[2]) & alignmentSamplesState['RequiredSectorHasFreeBEEntries'])

            responceDict['samples'].append(resultData)

        response_json = wrap_data(responceDict)
        return response_json

# /api/v1/alignment/get-bands
def alignmentGetAllBands(req):
    if req.method == 'GET':
        attributes_list = []
        try:

            file_to_open = 'pregetbands.json'
            pre_combo_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))
                
            file_to_open = 'getbands.json'
            combo_table_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))

        except:
            radlogger.log('Unable to open ' + file_to_open + ' input data file.')
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        try:
            attributes_list = [attributeshelper.COMBO_NUMBER_OF_SUBBANDS, attributeshelper.CURRENT_SUB_BAND_ID]

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            number_of_subBands  = ubus_attributes_dict[attributeshelper.COMBO_NUMBER_OF_SUBBANDS['name']]
            current_sub_band_id = ubus_attributes_dict[attributeshelper.CURRENT_SUB_BAND_ID['name']]

            inflate_table(pre_combo_requests, int(number_of_subBands), 0)   # WRNING!!! Zero Based table

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(pre_combo_requests))

            match_json(pre_combo_requests, ubus_attributes_dict)   

            default_combo_row = copy.deepcopy(combo_table_requests['bandsList'][0])
            combo_table_requests['bandsList'] = []
                       
            for band_index in range(0, int(number_of_subBands)):
                if pre_combo_requests[int(band_index)]['subBandAdminState'] == '1':
                    
                    temp_row = copy.deepcopy(default_combo_row)

                    cbwAvailableString = pre_combo_requests[int(band_index)]['cbwAvailable']
                    cbwAvailableStringArray = cbwAvailableString.split('|')
                    for cbwIndex in range(0, len(alignmentChangeBandCbwArray)):
                        if int(cbwAvailableStringArray[cbwIndex]) < 2:
                            temp_row.pop(alignmentChangeBandCbwArray[cbwIndex], None)
                    
                    for key, val in temp_row.items():
                        val['index'] = band_index   # WRNING!!! Zero Based table
                    combo_table_requests['bandsList'].append(temp_row)
                band_index = band_index + 1

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(combo_table_requests))

            match_json(combo_table_requests, ubus_attributes_dict)

            combo_table_requests['currentCbw'] = int(combo_table_requests['currentCbw']) / 1000

            for bandIndex in range(0, len(combo_table_requests['bandsList'])):
                for cbwIndex in range(0, len(alignmentChangeBandCbwArray)):
                    if alignmentChangeBandCbwArray[cbwIndex] in combo_table_requests['bandsList'][bandIndex]:
                        allowedFreq = combo_table_requests['bandsList'][bandIndex][alignmentChangeBandCbwArray[cbwIndex]]
                        allowedFreqArray = list(allowedFreq)

                        numericAllowedFreqArray = []

                        # ADIR CHANGES  
                        resolution = int(combo_table_requests['bandsList'][bandIndex]['bandResolution'])
                        firstFreq = int(combo_table_requests['bandsList'][bandIndex]['bandMinFreq']) - resolution
                        lastFreq = int(combo_table_requests['bandsList'][bandIndex]['bandMaxFreq'])  + resolution
                        

                        for freqIndex in range(0, len(allowedFreqArray)):
                            freq = firstFreq + freqIndex * resolution
                            if allowedFreqArray[freqIndex] == "1":
                                numericAllowedFreqArray.append(str(freq).rstrip())
                        combo_table_requests['bandsList'][bandIndex][alignmentChangeBandCbwArray[cbwIndex]] = numericAllowedFreqArray

            response_json = wrap_data(combo_table_requests)

            return response_json
    
        except:
            radlogger.log('alignmentGetAllBands method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

# /api/v1/alignment/set-band
def alignmentSetBand(req):

    radlogger.log(req.data, None)

    payload_dict =  {}

    payload = req.get_json()
    payload_dict = payload

    resetTimeOut = 5

    frequenciesList = []

    bandId = ''
    networkId = ''
    channelBw = 0
    frequenciesList = []

    bandId = payload_dict['bandId']
    channelBw = int(payload_dict['channelBw'])
    frequenciesList = payload_dict['frequencies']
    networkId = payload_dict['networkId']

    attributes_list = [attributeshelper.COMBO_NUMBER_OF_SUBBANDS, attributeshelper.CURRENT_SUB_BAND_ID]

    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

    if not bool(ubus_attributes_dict):
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    number_of_subBands  = ubus_attributes_dict[attributeshelper.COMBO_NUMBER_OF_SUBBANDS['name']]
    current_sub_band_id = ubus_attributes_dict[attributeshelper.CURRENT_SUB_BAND_ID['name']]

    if sorted(bandId.split('\/')) != sorted(current_sub_band_id.split('\/')):
        attributes_list = []
        #payload_dict = flatten_payload_to_dict(payload)

        attributes_list = [attributeshelper.alignment_changeBandId]
            
        attributes_list[0]['value'] = bandId

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)
        success = bool(ubus_attributes_dict)

        if success:
            # Reset ODU on another thread and return response to client
            Timer(resetTimeOut, odu_reset, ()).start()
            response_json = wrap_data({}, msg="PendingReset")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set value")
            return response_json
    else:

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

        minFreq    = int(minFreq)
        maxFreq    = int(maxFreq)
        resolution = int(resolution)
        
        numOfFreq = ((maxFreq - minFreq)/resolution) + 1
        
        newAllowableChannelsStr = ''

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
                  

        attributes_list = [attributeshelper.alignment_channelBw,
                           attributeshelper.alignment_available_channels_str]
            
        attributes_list[0]['value'] = channelBw if channelBw > 1000 else (channelBw * 1000)
        attributes_list[1]['value'] = newAllowableChannelsStr

        if networkId == '' or len(networkId) == 4:
            network_id = copy.deepcopy(attributeshelper.alignment_networkId)
            network_id['value'] = networkId
            attributes_list.append(network_id)

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)
        success = bool(ubus_attributes_dict)

        if success:
            response_json = wrap_data({}, msg="Done")
            return response_json
        else: 
            response_json = wrap_data({}, error="Unable to set value")
            return response_json

# /api/v1/alignment/evaluation-results
def getAlignmentEvalResults(req):
    if req.method == 'GET':
        attributes_list = []
        cursorLocation = None

        try:
            attributes_list = [attributeshelper.alignment_link_state,
                               attributeshelper.alignment_evaluation_tput_local,
                               attributeshelper.alignment_cpeRemoteMonitorComp,
                               attributeshelper.CURRENT_RATE_IDX,
                               attributeshelper.CURRENT_RATE_CBW,
                               attributeshelper.CURRENT_RATE_GI]
                   
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            tputLocal      = ubus_attributes_dict[attributeshelper.alignment_evaluation_tput_local['name']]
            compressedData = ubus_attributes_dict[attributeshelper.alignment_cpeRemoteMonitorComp['name']]
            linkStateNumber = ubus_attributes_dict[attributeshelper.alignment_link_state['name']]

            modulation_data = compresseddatahelper.parse_hbs_monitor_modulation(compressedData)
            compressedDict = compresseddatahelper.parse_hbs_remote_monitor(compressedData)
            tputRemote = str(compressedDict['hbsTput'])   # bps
            tputLocal  = tputLocal                        # bps

            # Build modulation string for hsu
            if 'CurrentRateIdx' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateIdx'] and \
               'CurrentRateCBW' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateCBW'] and \
               'CurrentRateGI' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateGI']:
                    currentRateIdx = ubus_attributes_dict['CurrentRateIdx']
                    currentRateCBW = ubus_attributes_dict['CurrentRateCBW']
                    currentRateGI = ubus_attributes_dict['CurrentRateGI']
                    CurrentRateIdx = createStringModulation(currentRateIdx, currentRateCBW, currentRateGI)

            resultData = {}
            resultData['DownLink'] = tputRemote
            resultData['UpLink']   = tputLocal
            resultData['LinkState'] = linkStatesHash[int(linkStateNumber)]
            resultData['CurrentRateIdx'] = CurrentRateIdx
            resultData['hbsModulationRate'] = modulation_data['hbsModulationRate']

            response_json = wrap_data(resultData)
            return response_json
        except:
            print('Unexpected error:', sys.exc_info()[0])
            response_json = wrap_data(None, error="Error occurred")
            return response_json

# /api/v1/alignment/init-values
def getInitialValues_hsu(req):
    if req.method == 'GET':
        try:
            file_to_open = 'initialData.json'
            initial_data_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(initial_data_requests))
            match_json(initial_data_requests, ubus_attributes_dict)
            responceDict = {}

            for index in range (len(initial_data_requests)):
                dataDict = copy.deepcopy(initial_data_requests[index])
                responceDict['apiVersion'] = app.config['API_VERSION']
                responceDict['macAddress'] = dataDict['macAddress']
                responceDict['aggregateCapacity'] = dataDict['aggregateCapacity']
                responceDict['hsuId'] = int(dataDict['hsuId'])
                responceDict['hsuLinkState'] = converters.HSU_LINK_STATE[dataDict['hsuLinkState']]
                responceDict['hsuAirState'] = converters.HSU_AIR_STATE[dataDict['hsuAirState']]
                responceDict['hsuServiceType'] = converters.SERVICE_HSU_TYPE[dataDict['hsuServiceType']]
                responceDict['radiusInstallConfirmationRequired'] = 'true' if dataDict['radiusInstallConfirmationRequired'] == '1' else 'false'
                responceDict['azimutBeamwidth'] = dataDict['azimutBeamwidth']
                responceDict['elevationBeamwidth'] = dataDict['elevationBeamwidth']
                responceDict['attachedAntennaIndication'] = converters.ATTACHED_ANTENNA_INDICATION[dataDict['attachedAntennaIndication']]
                responceDict['numOfElevationZones'] = 0
                responceDict['antennaGain'] = dataDict['antennaGain']
                responceDict['minAntennaGain'] = dataDict['minAntennaGain']
                responceDict['maxAntennaGain'] = dataDict['maxAntennaGain']
                responceDict['cableLoss'] = dataDict['cableLoss']
                responceDict['bandName'] = dataDict['currentBand']
                responceDict['antennaConnectionType'] = converters.ANTENNA_CONNECTION_TYPE[dataDict['antennaConnectionType']]
                responceDict['sectorId'] = dataDict['sectorId']

                # antenna data calculation
                azimutDataArray = responceDict['azimutBeamwidth'].split(',')
                if len(azimutDataArray) == 3:
                   responceDict['azimutBeamwidth'] = int(azimutDataArray[2])

                elevationDataArray = responceDict['elevationBeamwidth'].split(',')
                if len(elevationDataArray) == 3:
                   responceDict['elevationBeamwidth'] = int(elevationDataArray[2])
                   GLOBAL_HASH['elevationBeamwidth'] = responceDict['elevationBeamwidth'] 

                   if int(elevationDataArray[2]) != 0:
                       responceDict['numOfElevationZones'] = (int(elevationDataArray[1]) - int(elevationDataArray[0]))/ int(elevationDataArray[2])

                # Last Value requires calculation. ->Subtract the second value and the first value . [i.e. (30 – (-30)) = 60 (this is the total amount of degrees we cover ) ] and than divide by the third value. And get the amount of steps we use.
                # Full example: [30 – (-30)]/20 = 3

            response_json = wrap_data(responceDict)
            return response_json

        except:
            radlogger.log('ERROR::getInitialValues:', sys.exc_info())
            response_json = wrap_data(None, error="Error occurred")
            return response_json


def getInitialValues_hbs(req):
    if req.method == 'GET':
        try:
            file_to_open = 'initialData_hbs.json'
            initial_data_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(initial_data_requests))
            match_json(initial_data_requests, ubus_attributes_dict)
            responceDict = {}

            for index in range (len(initial_data_requests)):
                dataDict = copy.deepcopy(initial_data_requests[index])
                responceDict['apiVersion'] = app.config['API_VERSION']
                responceDict['macAddress'] = dataDict['macAddress']
                responceDict['aggregateCapacity'] = dataDict['aggregateCapacity']
                responceDict['hsuId'] = int(dataDict['hsuId'])
                responceDict['hbsLinkState'] = converters.HBS_LINK_STATE[dataDict['hbsLinkState']]
                responceDict['hbsAirState'] = converters.HBS_AIR_STATE[dataDict['hbsAirState']]
                #responceDict['hbsServiceCategoryType'] = converters.SERVICE_CATEGORY_HBS_TYPE[dataDict['hbsServiceCategoryType']]
                responceDict['radiusInstallConfirmationRequired'] = 'true' if dataDict['radiusInstallConfirmationRequired'] == '1' else 'false'
                responceDict['azimutBeamwidth'] = dataDict['azimutBeamwidth']
                responceDict['elevationBeamwidth'] = dataDict['elevationBeamwidth']
                responceDict['attachedAntennaIndication'] = converters.ATTACHED_ANTENNA_INDICATION[dataDict['attachedAntennaIndication']]
                responceDict['numOfElevationZones'] = 0
                responceDict['antennaGain'] = dataDict['antennaGain']
                responceDict['minAntennaGain'] = dataDict['minAntennaGain']
                responceDict['maxAntennaGain'] = dataDict['maxAntennaGain']
                responceDict['cableLoss'] = dataDict['cableLoss']
                responceDict['bandName'] = dataDict['currentBand']
                responceDict['antennaConnectionType'] = converters.ANTENNA_CONNECTION_TYPE[dataDict['antennaConnectionType']]
                responceDict['sectorId'] = dataDict['sectorId']

                # antenna data calculation
                azimutDataArray = responceDict['azimutBeamwidth'].split(',')
                if len(azimutDataArray) == 3:
                   responceDict['azimutBeamwidth'] = int(azimutDataArray[2])

                elevationDataArray = responceDict['elevationBeamwidth'].split(',')
                if len(elevationDataArray) == 3:
                   responceDict['elevationBeamwidth'] = int(elevationDataArray[2])
                   GLOBAL_HASH['elevationBeamwidth'] = responceDict['elevationBeamwidth'] 

                   if int(elevationDataArray[2]) != 0:
                       responceDict['numOfElevationZones'] = (int(elevationDataArray[1]) - int(elevationDataArray[0]))/ int(elevationDataArray[2])

                # Last Value requires calculation. ->Subtract the second value and the first value . [i.e. (30 – (-30)) = 60 (this is the total amount of degrees we cover ) ] and than divide by the third value. And get the amount of steps we use.
                # Full example: [30 – (-30)]/20 = 3

            response_json = wrap_data(responceDict)
            return response_json

        except:
            radlogger.log('ERROR::getInitialValues:', sys.exc_info())
            response_json = wrap_data(None, error="Error occurred")
            return response_json
# /api/v1/alignment/link-data
def getLinkData(req):
    attributes_list = []
    try:

        file_to_open = 'getlinkdata.json'
        data = load_mapping_json_file(os.path.join(__location__, file_to_open))
                
    except:
        radlogger.log('Unable to open ' + file_to_open + ' input data file.')
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    try:
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        # Convert values in dict
        if 'hsuLinkState' in ubus_attributes_dict and ubus_attributes_dict['hsuLinkState']:
            ubus_attributes_dict['hsuLinkState'] = converters.HSU_LINK_STATE[ubus_attributes_dict['hsuLinkState']]

        if 'hsuAirState' in ubus_attributes_dict and ubus_attributes_dict['hsuAirState']:
            ubus_attributes_dict['hsuAirState'] = converters.HSU_AIR_STATE[ubus_attributes_dict['hsuAirState']]
        
        if 'currentCbw' in ubus_attributes_dict and ubus_attributes_dict['currentCbw']:
            ubus_attributes_dict['currentCbw'] = int(ubus_attributes_dict['currentCbw']) / 1000

        # Parse compressed data
        parsed_data = compresseddatahelper.parse_HBS_static(ubus_attributes_dict['sectorType'])
        if parsed_data:
            for val in parsed_data:
                if val == 'hbsAgentVersion' :
                    if int(parsed_data[val]) >= 3160 :
                        ubus_attributes_dict['sectorType'] = 'Gen4'
                    else:
                        ubus_attributes_dict['sectorType'] = 'Gen3'

        else:
            ubus_attributes_dict['sectorType'] = ''

        # Wrap data
        response_json = wrap_data(ubus_attributes_dict)
        return response_json
    except:
        radlogger.log('getLinkData GET method.', sys.exc_info())
        response_json = wrap_data(None, error="Error occurred")
        return response_json

# /api/v1/alignment/fine-alignment
def getFineAligmentResults(req):
    if req.method == 'GET':
        attributes_list = []
        cursorLocation = None
        #try:
        #    file_to_open = 'finealignment.json'
        #    data = load_mapping_json_file(os.path.join(__location__, file_to_open))

        #    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))

        try:
            attributes_list = [attributeshelper.alignment_link_state,
                               attributeshelper.alignment_rss_local,
                               attributeshelper.alignment_cpeRemoteMonitorComp,
                               attributeshelper.alignment_SectorId,
                               attributeshelper.alignment_currentCbw,
                               attributeshelper.alignment_frequency,
                               attributeshelper.alignment_hbsCompressedStatic]

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            linkStateNumber    = ubus_attributes_dict[attributeshelper.alignment_link_state['name']]
            rssLocal           = ubus_attributes_dict[attributeshelper.alignment_rss_local['name']]
            compressedData     = ubus_attributes_dict[attributeshelper.alignment_cpeRemoteMonitorComp['name']]
            sectorId           = ubus_attributes_dict[attributeshelper.alignment_SectorId['name']]
            currentCbw         = int ( ubus_attributes_dict[attributeshelper.alignment_currentCbw['name']] ) / 1000
            hbsCompressedData  = ubus_attributes_dict[attributeshelper.alignment_cpeRemoteMonitorComp['name']]
            frequency          = ubus_attributes_dict[attributeshelper.alignment_frequency['name']] 

            compressedDict = compresseddatahelper.parse_hbs_remote_monitor(compressedData)
            rssRemote = compressedDict['hbsRss']

            resultData = {}
            # names = ['hbsLocation', 'hbsIp', 'hbsSubnetMask', 'hbsAntennaType', 'hbsAgentVersion', 'hbsName']
            # Parse compressed data
            parsed_data = compresseddatahelper.parse_HBS_static(ubus_attributes_dict[attributeshelper.alignment_hbsCompressedStatic['name']])
            if parsed_data:
                for val in parsed_data:
                    if val == 'hbsIp':
                        resultData[val] = parsed_data[val]
                    if val == 'hbsName':
                        resultData[val] = parsed_data[val]
                    if val == 'hbsLocation':
                        resultData[val] = parsed_data[val]


            #hbs_parsed_data = compresseddatahelper.parse_HBS_static(ubus_attributes_dict[attributeshelper.alignment_hbsCompressedStatic['name']] )
            #if hbs_parsed_data:
            #    for val in hbs_parsed_data:
            #        if hbs_parsed_data[val].startwith ('hbsIp'):
            #            resultData[val] = hbs_parsed_data[val]
            #        if hbs_parsed_data[val].startwith ('hbsName'):
            #            resultData[val] = hbs_parsed_data[val]
            #        if hbs_parsed_data[val].startwith ('hbsLocation'):
            #            resultData[val] = hbs_parsed_data[val]

            resultData['RSSDL'] = int(rssRemote)
            resultData['RSSUL'] = int(rssLocal)
            resultData['LinkState'] = linkStatesHash[int(linkStateNumber)]
            resultData['SectorId'] = sectorId
            resultData['frequency'] = frequency
            resultData['currentCbw'] = currentCbw 

            response_json = wrap_data(resultData)
            return response_json
        except:
            radlogger.log('getFineAligmentResults GET method.', sys.exc_info())
            response_json = wrap_data(None, error="Error occurred")
            return response_json

# /api/v1/alignment/set-antenna
def setAntennaValues(req):
     # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'setantennadata.json'))
        
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
            radlogger.log('setAntennaValues POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

############## HELPERS ##############

def initAlignmentColomnsCount():
    """
    initAlignmentColomnsCount() -> bool

    Method will ask alignmentScanAzimuthParams and calculate
    horizontalStartAngle
    horizontalEndAngle
    horizontalScanStep and 
    tableCellCount
    """

    attributes_list = []
    attributes_list = [attributeshelper.alignment_scan_azimuth_params]
    ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)
    success = bool(ubus_attributes_dict)
    azimuth = ubus_attributes_dict[attributeshelper.alignment_scan_azimuth_params['name']]
    if azimuth == '':
        print('intAlignmentColomnsCount - azimuth is empty')
        return false

    data = azimuth.split(',')
    if len(data) < 3:
        print('intAlignmentColomnsCount - invalid data')
        return false

    GLOBAL_HASH['horizontalStartAngle'] = int(data[0])
    GLOBAL_HASH['horizontalEndAngle'] = int(data[1])
    GLOBAL_HASH['horizontalScanStep'] = int(data[2])

    if (GLOBAL_HASH['horizontalScanStep'] != 0):
        GLOBAL_HASH['tableCellCount'] = ((GLOBAL_HASH['horizontalStartAngle'] * -1) + GLOBAL_HASH['horizontalEndAngle']) / GLOBAL_HASH['horizontalScanStep']

    return success

def calculateCursorLocation():
    attributes_list = []
    cursorLocation = None

    try:
        attributes_list = [attributeshelper.alignment_horizontal_angle,
                           attributeshelper.alignment_elevation_angle]
                   
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if not bool(ubus_attributes_dict):
            print("Error: Unable to get alignmentHorizontalAngle and alignmentElevationAngle")
            return None

        currentHorizontalAngle = ubus_attributes_dict[attributeshelper.alignment_horizontal_angle['name']]
        currentElevationAngle  = ubus_attributes_dict[attributeshelper.alignment_elevation_angle['name']]

        cursorLocation = getCursorLocation(currentHorizontalAngle, currentElevationAngle)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    return cursorLocation

def setFullChannelsAllowed():

    try:
        attributes_list = []
        attributes_list = [attributeshelper.alignment_min_freq,
                            attributeshelper.alignment_max_freq,
                            attributeshelper.alignment_resolution]

        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json
        attributeshelper.alignment_channelBw;
        minFreq    = ubus_attributes_dict[attributeshelper.alignment_min_freq['name']]
        maxFreq    = ubus_attributes_dict[attributeshelper.alignment_max_freq['name']]
        resolution = ubus_attributes_dict[attributeshelper.alignment_resolution['name']]

        minFreq    = int(minFreq)
        maxFreq    = int(maxFreq)
        resolution = int(resolution)

        numOfFreq = ((maxFreq - minFreq)/resolution) + 1
        
        newAllowableChannelsStr = ''

        currentIterationChannel = minFreq

        for channelIndex in range(0, numOfFreq):
            newAllowableChannelsStr += '1'

        attributes_list = []

        availableStr = copy.deepcopy(attributeshelper.alignment_available_channels_str)

        availableStr['value'] = newAllowableChannelsStr
        attributes_list.append(availableStr)

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)

        success = bool(ubus_attributes_dict)
        return success
    except:
        radlogger.log('setFinalData method.', sys.exc_info())
        return None

def getCursorLocation(currentHorizontalAngle, currentElevationAngle):

    horizontalCellNumber = 0
    verticalCellName = 'middle'

    for horizontalCellCount in range(0, GLOBAL_HASH['tableCellCount']):
        if (GLOBAL_HASH['horizontalStartAngle'] + GLOBAL_HASH['horizontalScanStep'] * horizontalCellCount) >= int(currentHorizontalAngle):
            horizontalCellNumber = horizontalCellCount
            break

    if int(currentElevationAngle) > (GLOBAL_HASH['elevationBeamwidth'] / 2):
        verticalCellName = 'high'

    if int(currentElevationAngle) < -(GLOBAL_HASH['elevationBeamwidth'] / 2):
        verticalCellName = 'low'

    _cursorLocation = {'cellNumber': int(horizontalCellNumber),
                      'elevationCell': verticalCellName,
                      'elevation': int(currentElevationAngle),
                      'horizontal': int(currentHorizontalAngle)}

    return _cursorLocation




#def print_error():
#    exec_info =  sys.exc_info()
#    radlogger.error( "%s: %s" % (exec_info[0], exec_info[1]) )
#    radlogger.error( "%s" % (traceback.print_tb(exec_info[2])) )