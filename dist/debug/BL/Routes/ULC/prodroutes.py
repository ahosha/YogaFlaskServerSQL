"""
Routes for the flask application.
"""
from FlaskServer import app
from flask import jsonify, request
from flask_restful import Resource , Api

from flask_jwt import JWT, jwt_required, current_identity
from FlaskServer.Routes.Monitor import monitor_route , monitor_route_hbs, Monitor
from FlaskServer.Routes.System import *
from FlaskServer.Routes.Radio import radio_route_hsu , radio_route_hbs, Radio
from FlaskServer.Routes.Network import network_route , Network
from FlaskServer.Routes.RecentEvents import recent_events_route , RecentEvents
from FlaskServer.Routes.ActiveAlarms import active_alarms_route , ActiveAlarms
from FlaskServer.Routes.TrapsDestinations import trapsdestinations_route  , TrapsDestinations
from FlaskServer.Routes.Debug import debug_log_route, debug_attribute_route
#from FlaskServer.BL.Routes.DeviceDebug import debug_device_route
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.ChangeBand import *
from FlaskServer.Routes.Operations.spectrum import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Alignment.Training import training_action_invoker
from FlaskServer.Routes.Alignment import *
from FlaskServer.Routes.Wifi import wifi_route , Wifi
from FlaskServer.Routes.Hss import hss_route, Hss
from FlaskServer.Routes.Battery import battery_route
#from FlaskServer.Routes.InternalVoltages import internalVoltages_route
from FlaskServer.Routes.Sensor import sensor_route
from FlaskServer.Routes.Port import port_route
import FlaskServer.consts as consts 
from FlaskServer.Routes.DeviceMode import devicemode_route, DeviceMode 
from FlaskServer.serverstate import ServerState
########################################## Data URLS ############################################

api = Api(app)


api.add_resource(DeviceMode , consts.DEVICE_MODE_URL)
api.add_resource(Hss , consts.HSS_URL)
api.add_resource(Monitor , consts.MONITOR_URL)
api.add_resource(System , consts.SYSTEM_URL) 
api.add_resource(Radio , consts.RADIO_URL)
api.add_resource(Network , consts.NETWORK_URL)
api.add_resource(RecentEvents , consts.RECENT_EVENTS_URL)
api.add_resource(ActiveAlarms , consts.ACTIVE_ALARMS_URL)
api.add_resource(TrapsDestinations , consts.TRAPS_DESTINATIONS_URL)
api.add_resource(Wifi , consts.WIFI_URL)
api.add_resource(Operation , consts.OPERATION_URL + '/<op_name>' , consts.OPERATION_URL + '/<op_name>/<action>')
api.add_resource(Spectrum , consts.SPECTRUM_URL + '/<op_name>')
api.add_resource(SoftwareUpgrade , consts.SWU_URL + '/<op_name>')
api.add_resource(Alignment , consts.ALIGNMNET_URL + '/<op_name>' , consts.ALIGNMNET_URL + '/<op_name>/<action>')


#FlaskVersionMode
@app.route(consts.FLASK_VERISON_URL, methods=['GET'])
def flaskversionroute():
    return jsonify(flask_version_route(request))


#Monitor
#@app.route(consts.MONITOR_URL, methods=['GET'])
#@jwt_required()
#def monitorroute():
#    mode = ServerState.getDeviceMode(ServerState())
#    if mode == 'HBS':
#       return jsonify(monitor_route_hbs(request))
#    else: 
#        return jsonify(monitor_route(request))


#System
#@app.route(consts.SYSTEM_URL, methods=['GET', 'POST'])
#@jwt_required()
#def systemroute():
#    return jsonify(system_route(request))

#Radio
#@app.route(consts.RADIO_URL, methods=['GET', 'POST'])
@jwt_required()
#def radioroute():
#    mode = ServerState.getDeviceMode(ServerState())
#    if mode == 'HBS':
#      return jsonify(radio_route_hbs(request))
#    else:
#      return jsonify(radio_route_hsu(request))


##Network
#@app.route(consts.NETWORK_URL, methods=['GET', 'POST'])
#@jwt_required()
#def networkroute():
#    return jsonify(network_route(request))

#Recent Events
#@app.route(consts.RECENT_EVENTS_URL, methods=['GET'])
#@jwt_required()
#def recenteventsroute():
#    return jsonify(recent_events_route(request))

# Active Alarms
#@app.route(consts.ACTIVE_ALARMS_URL, methods=['GET'])
#@jwt_required()
#def activealarmstoute():
#    return jsonify(active_alarms_route(request))

#Traps Destinations
#@app.route(consts.TRAPS_DESTINATIONS_URL, methods=['GET', 'POST'])
#@jwt_required()
#def trapsroute():
#    return jsonify(trapsdestinations_route(request))


#Wifi
#@app.route(consts.WIFI_URL, methods=['GET', 'POST'])
#@jwt_required()
#def wifiroute():
#    return jsonify(wifi_route(request))

#@app.route(consts.HSS_URL, methods=['GET', 'POST'])
#@jwt_required()
#def hssroute():
#    return jsonify(hss_route(request))

########################################## Operations URLS ############################################

#@app.route(consts.PING_URL, methods=['POST'])
#@jwt_required()
#def pingroute():
#    return jsonify(ping(request))

#@app.route(consts.TRACE_URL, methods=['POST'])
#@jwt_required()
#def traceroute():
#    return jsonify(trace(request))

#@app.route(consts.RESET_URL, methods=['POST'])
#@jwt_required()
#def trace_route():
#    return jsonify(odu_reset())

#@app.route(consts.RESYNC_URL, methods=['POST'])
#@jwt_required()
#def resync_route():
#    return jsonify(resync())

#@app.route(consts.DEREGISTER_URL, methods=['POST'])
#@jwt_required()
#def deregisterlocalroute():
#    return jsonify(deregister_local_route(request))


#@app.route(consts.CHANGE_BAND_URL, methods=['GET', 'POST'])
#@jwt_required()
#def dump_routing_func():
#    return jsonify(changeBand(request))

#@app.route(consts.SWU_UPLOAD_URL, methods=['POST'])
#@jwt_required()
#def swuuploadroute():
#    return jsonify(swu_upload_route(request))

#@app.route(consts.SWU_VALIDATE_URL, methods=['GET'])
#@jwt_required()
#def swuvalidateroute():
#    return jsonify(swu_validate_route(request))

#@app.route(consts.SWU_START_URL, methods=['POST'])
#@jwt_required()
#def swustartroute():
#    return jsonify(swu_start_route(request))

#@app.route(consts.SWU_BACKUP_URL, methods=['GET'])
#@jwt_required()
#def swubackuproute():
#    return swu_start_backup(request)

#@app.route(consts.SWU_FILE_EXISTENCE_URL, methods=['GET'])
#@jwt_required()
#def swuFileExistenceRoute():
#    return jsonify(swu_check_file_existence(request))

#@app.route(consts.SPEED_TEST_URL + '/<action>', methods=['GET', 'POST'])
##@jwt_required
#def speedtestroute(action):
#    mode = ServerState.getDeviceMode(ServerState())
#    if mode == 'HBS':
#       return jsonify(speed_test_hbs(action, request))
#    else:
#       return jsonify(speed_test(action, request))

#@app.route(consts.SPECTRUM_RANGE_URL, methods=['GET'])
#@jwt_required()
#def spectrumrangeroute():
#    return jsonify(spectrum_range(request))

#@app.route(consts.START_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
#def spectrumstartroute():
#    return jsonify(start_spectrum(request))

#@app.route(consts.STOP_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
#def spectrumstoproute():
#    return jsonify(stop_spectrum(request))

#@app.route(consts.SPECTRUM_TABLE_URL, methods=['GET'])
#@jwt_required()
#def spectrumtableroute():
#    return jsonify(spectrum_table(request))

#@app.route(consts.DIAGNOSTICS_URL, methods=['GET'])
#@jwt_required()
#def diagnostics():
#    return get_diagnostics(request)

#@app.route(consts.LICENSE_ACTIVATION_URL, methods=['GET', 'POST'])
#@jwt_required()
#def activatelicenseroute():
#    return jsonify(license_activation(request))

#@app.route(consts.CHANGE_LINK_PASSWORD, methods=['POST'])
#@jwt_required()
#def changelinkpasswordroute():
#    return jsonify(change_link_password(request))

#@app.route(consts.RESTORE_TO_DEFAULTS_URL, methods=['POST'])
#@jwt_required()
#def restoretodefaultsroute():
#    return jsonify(restore_to_defaults(request))

#@app.route(consts.INSTALLATION_CONFIRMATION_URL, methods=['POST'])
#@jwt_required()
#def installationconfirmationroute():
#    return jsonify(installation_confirmation(request))
########################################## Debug URLS ############################################

@app.route(consts.DEBUG_LOG_URL, methods=['GET'])
def debuglogroute():
    return debug_log_route()

@app.route(consts.DEBUG_ATTRIBUTE_URL, methods=['GET', 'POST'])
def debugattributeurl():
    return jsonify(debug_attribute_route(request))

########################################## Alignment URLS ############################################


#@app.route(consts.ALIGNMNET_MEASURING_URL, methods=['GET'])
#@jwt_required()
#def alignmentRoute():
#    return jsonify(alignmentTable(request))

#@app.route(consts.ALIGNMNET_BEST_POSITION_URL, methods=['GET'])
#@jwt_required()
#def bestPositionRoute():
#    return jsonify(getBestPosition(request))
    
#@app.route(consts.ALIGNMNET_POINTER_LOCATION_URL, methods=['GET'])
#@jwt_required()
#def pointerLocationRoute():
#    return jsonify(pointerLocation(request))

#@app.route(consts.ALIGNMNET_ACTION_URL + '/<action>', methods=['POST'])
#@jwt_required()
#def actionRoutActRoute(action):
#    return jsonify(alignmentActionInvoker(action, request))

#@app.route(consts.ALIGNMNET_LINK_EVAL_URL + '/<action>', methods=['POST'])
#@jwt_required()
#def getEvaluationResultsRoute(action):
#    return jsonify(evaluationActionInvoker(action, request))

#@app.route(consts.ALIGNMNET_GET_ALL_BANDS_URL, methods=['GET'])
#@jwt_required()
#def getAllBandsRoute():
#    return jsonify(alignmentGetAllBands(request))

#@app.route(consts.ALIGNMNET_SET_BANDS_URL, methods=['POST'])
#@jwt_required()
#def setbandsroute():
#    return jsonify(alignmentSetBand(request))

#@app.route(consts.ALIGNMNET_FINE_ALIGNMNET_URL, methods=['GET'])
#@jwt_required()
#def fineAligmentRoute():
#    return jsonify(getFineAligmentResults(request))

#@app.route(consts.ALIGNMNET_EVAL_RESULTS_URL, methods=['GET'])
#@jwt_required()
#def evaluationResults():
#    return jsonify(getAlignmentEvalResults(request))

#@app.route(consts.ALIGNMNET_INIT_VALUES, methods=['GET'])
#@jwt_required()
#def initValuesRoute():
#    return jsonify(getInitialValues(request))

#@app.route(consts.ALIGNMNET_LINK_DATA, methods=['GET'])
#@jwt_required()
#def linkDataRoute():
#    return jsonify(getLinkData(request))

#@app.route(consts.ALIGNMNET_SPEED_TEST+ '/<action>', methods=['GET','POST'])
#@jwt_required()
#def alignmentspeedtestroute(action):
#    return jsonify(alignment_speed_test(action, request))


##################################### Training URLS ######################################

@app.route(consts.TRAINING_URL + '/<action>', methods=['POST'])
def trainingactionroute(action):
    return jsonify(training_action_invoker(request, action))


##################################### Smart Node URLS ######################################
#Battery
@app.route(consts.BATTERY_URL, methods=['GET', 'POST'])
@jwt_required()
def batteryroute():
    return jsonify(battery_route(request))

@app.route(consts.INTERNAL_VOLTAGE_URL, methods=['GET'])
@jwt_required()
def internalvoltagesroute():
    return jsonify(internalVoltages_route(request))
	
#Sensor
@app.route(consts.SENSOR_URL, methods=['GET', 'POST'])
@jwt_required()
def sensorroute():
    return jsonify(sensor_route(request))


#Port
@app.route(consts.PORT_URL, methods=['GET', 'POST'])
@jwt_required()
def portroute():
    return jsonify(port_route(request))

##################################### P2P ULC URLS ######################################
#DeviceMode
#@app.route(consts.DEVICE_MODE_URL, methods=['GET'])
#@jwt_required()
#def devicemoderoute():
#    return jsonify(devicemode_route())

##Port
#@app.route(consts.DEVICE_DEBUG_URL, methods=['POST'])
#@jwt_required()
#def devicedebugroute():
#    return jsonify(debug_device_route(request))







