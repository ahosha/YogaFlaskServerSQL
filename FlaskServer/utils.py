import datetime, time
import glob
import os
import consts as consts
#from FlaskServer.jsonutils import *
import sys, traceback

from flask_restful import reqparse

TRUE = 1
FALSE = 0

def create_arg(name , type , required , help):
    return {"name":name , "type": type , "required": required ,"help":help}

def check_args_func(args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg['name'], type=arg['type'], required=arg['required'] , help=arg['help'])
    return parser.parse_args()

def log_err(route_name, methodType = 'unknow type' , err = 'Error occurred'):
    exec_info =  sys.exc_info()
    err_msg = exec_info[1].message
    err_file_name_as_list = str(exec_info[2].tb_frame.f_code.co_filename).split('\\')
    err_file_name = get_flie_name_err(err_file_name_as_list , 6)
    #err_line =  str(exec_info[2].tb_next.tb_lineno)
    err_line =  get_line_err(exec_info)
    radlogger.log(route_name + ' ' + methodType + ' method.', sys.exc_info())
    radlogger.log('****-' + err_msg + '-****')
    radlogger.log('****- In File  :' + err_file_name + '-****')
    radlogger.log('****- In Line  :' + err_line + '-****')
    response_json = wrap_data({}, err , err_msg )
    return response_json

def get_line_err(exec_info):
     err = exec_info[2]
     try:
        return str(err.tb_next.tb_lineno)
     except:
        return str(err.tb_lineno)

def get_flie_name_err(err_file_name_as_list , path_levels):
    name = '';
    for index, level in reversed(list(enumerate(err_file_name_as_list))):
        if index >= path_levels:
            name = level + '/' + name
    return name

#def build_modulation_string(ubus_attributes_dict):
#    from FlaskServer.Routes.Monitor.modulation import createStringModulation
#    if 'CurrentRateIdx' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateIdx'] and \
#    'CurrentRateCBW' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateCBW'] and \
#    'CurrentRateGI' in ubus_attributes_dict and ubus_attributes_dict['CurrentRateGI']:
#        currentRateIdx = ubus_attributes_dict['CurrentRateIdx']
#        currentRateCBW = ubus_attributes_dict['CurrentRateCBW']
#        currentRateGI = ubus_attributes_dict['CurrentRateGI']
#        ubus_attributes_dict['CurrentRateIdx'] = createStringModulation(currentRateIdx, currentRateCBW, currentRateGI)
#    return ubus_attributes_dict;

#def getReadyForSetInUbus(payload , flatten_data):
#    import FlaskServer.ubuscontroller as ubuscontroller
#    payload_dict = flatten_payload_to_dict(payload)
#    for attr in flatten_data:
#        if attr[ubuscontroller.NAME_KEY] in payload_dict:
#            attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

#    flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]
#    return flatten_data

def pop_data(data , names):
    for name in names:
        if name in data:
            data.pop(name)
    return data
# Delete all cache and .pyc files
def clean():
    filelist = glob.glob("*.cache")
    for f in filelist:
        # delete all cache files
        os.remove(f)
# Wrap response data in 'data' key. 
def wrap_data(data, msg=None, error=None):
    response_object = {}
    response_object['data'] = data
    if msg:
        response_object['data']['message'] = msg
    if error:
        response_object['error'] = {}
        response_object['error']['message'] = error
    return response_object

def get_date_string(date_time, reboot_time):

    date = datetime.now() + timedelta(seconds=date_time)

    newDate = reboot_time + timedelta(milliseconds=date_time)

    return newDate

def cast_to_int(dict, *keys):
    for key in keys: 
        if key in dict and dict[key]:
            dict[key] = int(dict[key])

def cast_to_int_divide_by_factor(dict, factor, *keys):
    for key in keys: 
        if key in dict and dict[key] and factor:
            dict[key] = float(dict[key]) / factor

def cast_to_int_multiply_by_factor(dict, factor, *keys):
    for key in keys: 
        if key in dict and dict[key] and factor:
            dict[key] = float(dict[key]) * factor

def getInterfaceName(number):
    if number.isdigit() and number == '1':
        return 'Management Port on ODU'
    elif number.isdigit() and number == '101':
        return 'Radio Interface'
    else:
        return ''

def formatFrequency(freq):
    try:

        floatFreq = float(freq)
        result = "{0:0000.00} [MHz]".format(floatFreq / 1000) if floatFreq > 1000000 else '{:.3f} [GHz]'.format(floatFreq / 1000)
        return result
    except:
        return None

def getConvertedTimeFromTimeT(number_of_ticks, rebootTime):

    number_of_seconds = int(number_of_ticks)
    init1970 = datetime.datetime(1970, 1, 1)
    initial2005Date = datetime.datetime(2005, 9, 1)

    date = init1970 + datetime.timedelta(seconds = number_of_seconds)

    rebootTimeWithOneDay = rebootTime - datetime.timedelta(days=1)
    
    if date < rebootTimeWithOneDay:
        #New date = Event time - "9/1/2005 12:00:00" + reboot time
        newDate = rebootTime + (date - initial2005Date)
        #If future time or time before reboot, do not return new date
        if (newDate > datetime.datetime.now() or newDate < (datetime.datetime.now() - datetime.timedelta(days = 1))):
            # DEBUG
            return newDate.strftime(consts.DATE_TIME_FORMAT)
            #return ''
        return newDate.strftime(consts.DATE_TIME_FORMAT)
    return date.strftime(consts.DATE_TIME_FORMAT)

def getSysUpTime(number_of_ticks):
    number_of_seconds = int(number_of_ticks)/100
    return_time = datetime.datetime.now() - datetime.timedelta(seconds = number_of_seconds)
    return return_time

def getFetureSupportByCapability(capabilityBitmask, index):
    capabilities = list(capabilityBitmask)
    if (len(capabilities) < (index - 1)):
        return false

    intIndex = int(index)
    return capabilities[index] != '0'

def get_base_dir():
    return os.path.abspath(os.path.dirname(__file__))

