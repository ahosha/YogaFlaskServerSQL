"""
Routes for the flask application. DEV!! DEV!! DEV!! DEV!!
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from FlaskServer.Dev import mockedDataRequest
from FlaskServer.Routes.Monitor import monitor_route
from FlaskServer.Routes.System import *
from FlaskServer.Routes.Radio import radio_route_hsu
from FlaskServer.Routes.DeviceMode import devicemode_route
from FlaskServer.Routes.Network import network_route
from FlaskServer.Routes.RecentEvents import recent_events_route
from FlaskServer.Routes.ActiveAlarms import active_alarms_route
from FlaskServer.Routes.TrapsDestinations import trapsdestinations_route
from FlaskServer.Routes.Debug import debug_log_route, debug_attribute_route
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.ChangeBand import *
from FlaskServer.Routes.Operations.spectrum import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Alignment.Training import training_action_invoker
from FlaskServer.Routes.Alignment import *
from FlaskServer.Routes.Wifi import wifi_route
from FlaskServer.Routes.Battery import battery_route
from FlaskServer.Routes.Sensor import sensor_route
from FlaskServer.Routes.Port import port_route
import FlaskServer.consts as consts

from FlaskServer.Routes.Alignment.alignmnetmockup import *
from FlaskServer.Routes.Alignment.Training import *
from FlaskServer.Routes.Operations import *
from FlaskServer.Routes.Operations.licenseactivation import *
from FlaskServer.Routes.Operations.softwareupgrade import *
from FlaskServer.Routes.Debug import *

########################################## Alignment URLS ############################################
#FlaskVersionMode
@app.route(consts.FLASK_VERISON_URL, methods=['GET'])
def flaskversionroute():
    return jsonify(flask_version_route(request))

@app.route(consts.ALIGNMNET_MEASURING_URL, methods=['GET', 'POST'])
#@jwt_required()
def alignmentroute():
	return jsonify(training_measuring(request))

@app.route(consts.ALIGNMNET_BEST_POSITION_URL, methods=['GET', 'POST'])
#@jwt_required()
def bestpositionroute():
	return jsonify(training_best_position(request))

@app.route(consts.ALIGNMNET_FINE_ALIGNMNET_URL, methods=['GET'])
#@jwt_required()
def fineAligmentRoute():
	return jsonify(training_fine_alignment(request))

# LIVE values from UBUS !!!!!!
@app.route(consts.ALIGNMNET_POINTER_LOCATION_URL, methods=['GET'])
#@jwt_required()
def pointerlocationroute():
	return jsonify(pointerLocation(request))

# LIVE values from UBUS !!!!!!
@app.route(consts.ALIGNMNET_ACTION_URL + '/<action>', methods=['POST'])
#@jwt_required()
def actionRoutActRoute(action):
	return jsonify(training_alignmentActionInvoker(action, request))

# LIVE values from UBUS !!!!!!
@app.route(consts.ALIGNMNET_GET_ALL_BANDS_URL, methods=['GET'])
#@jwt_required()
def getAllBandsRoute():
	return jsonify(alignmentGetAllBands(request))

# LIVE values from UBUS !!!!!!
@app.route(consts.ALIGNMNET_SET_BANDS_URL, methods=['POST'])
#@jwt_required()
def setbandsroute():
	return jsonify(alignmentSetBand(request))

# Alignment Simulator Only
@app.route(consts.ALIGNMNET_RESET_TEST_DATA_URL, methods=['POST'])
#@jwt_required()
def resetData_route():
	return jsonify(resetTestDataMockup(request))

@app.route(consts.ALIGNMNET_GENERATE_ID_URL, methods=['POST'])
#@jwt_required()
def generateIdroute():
	return jsonify(generateIdMockup(request))

@app.route(consts.ALIGNMNET_INIT_VALUES, methods=['GET'])
#@jwt_required()
def initValuesRoute():
    return jsonify(training_getInitialValues(request))

@app.route(consts.ALIGNMNET_LINK_DATA, methods=['GET'])
#@jwt_required()
def linkDataRoute():
    return jsonify(getLinkDataMockup(request))

@app.route(consts.ALIGNMNET_SPEED_TEST+ '/<action>', methods=['GET','POST'])
#@jwt_required()
def alignmentspeedtestroute(action):
	return jsonify(mockedDataRequest(request, 'speedtest'))

##################################### Training URLS ######################################

@app.route(consts.TRAINING_URL + '/<action>', methods=['POST'])
#@jwt_required()
def trainingactionroute(action):
	return jsonify(training_action_invoker(request, action))


##################################### Link Evaluation URLS ######################################

# /api/v1/alignment/evaluation/<action>
@app.route(consts.ALIGNMNET_LINK_EVAL_URL + '/<action>', methods=['POST'])
#@jwt_required()
def getEvaluationResultsRoute(action):
	return jsonify(startEvaluationMockup(action, request))
	
@app.route(consts.ALIGNMNET_EVAL_RESULTS_URL, methods=['GET'])
#@jwt_required()
def evaluationResults():
	return jsonify(training_evaluation_results(request))
	
########################################## Data URLS ############################################

#Monitor
@app.route(consts.MONITOR_URL, methods=['GET'])
#@jwt_required()
def monitor_route():
	return jsonify(mockedDataRequest(request, 'monitor'))

#System
@app.route(consts.SYSTEM_URL, methods=['GET', 'POST'])
#@jwt_required()
def system_route():
		return jsonify(mockedDataRequest(request, 'system'))

@app.route(consts.RADIO_URL, methods=['GET', 'POST'])
#@jwt_required()
def radio_route():
	return jsonify(mockedDataRequest(request, 'radio'))

@app.route(consts.NETWORK_URL, methods=['GET', 'POST'])
#@jwt_required()
def network_route():
	return jsonify(mockedDataRequest(request, 'network'))

@app.route(consts.RECENT_EVENTS_URL)
#@jwt_required()
def recentevents_route():
	return jsonify(mockedDataRequest(request, 'recent-events'))

#Traps Destinations
@app.route(consts.TRAPS_DESTINATIONS_URL, methods=['GET', 'POST'])
#@jwt_required()
def trapsroute():
	return jsonify(mockedDataRequest(request, 'traps-destinations'))

@app.route(consts.WIFI_URL, methods=['GET', 'POST'])
#@jwt_required()
def wifiroute():
	return jsonify(mockedDataRequest(request, 'wifi'))

@app.route(consts.ACTIVE_ALARMS_URL, methods=['GET', 'POST'])
#@jwt_required()
def activealarmsroute():
	return jsonify(mockedDataRequest(request, 'active-alarms'))

########################################## Operations URLS ############################################

@app.route(consts.PING_URL, methods=['POST'])
#@jwt_required()
def ping_route():
	return jsonify(ping(request))

@app.route(consts.TRACE_URL, methods=['POST'])
#@jwt_required()
def trace_route():
	return jsonify(trace(request))

@app.route(consts.RESET_URL, methods=['POST'])
#@jwt_required()
def reset_route():
	return jsonify(odu_reset())



@app.route(consts.RESYNC_URL, methods=['POST'])
#@jwt_required()
def resync_route():
	 return jsonify(resync())

@app.route(consts.DEREGISTER_URL, methods=['POST'])
def deregister_local_route():
    return jsonify(deregisterMockup(request))

@app.route(consts.CHANGE_BAND_URL, methods=['GET', 'POST'])
#@jwt_required()
def changeband_route():
	return jsonify(mockedDataRequest(request, 'change-band'))

@app.route(consts.SWU_UPLOAD_URL, methods=['POST'])
#@jwt_required()
def swuuploadroute():
	return jsonify(swu_upload_route(request))

@app.route(consts.SWU_VALIDATE_URL, methods=['GET'])
#@jwt_required()
def swuvalidateroute():
	return jsonify(swu_validate_route(request))

@app.route(consts.SWU_START_URL, methods=['POST'])
#@jwt_required()
def swustartroute():
	return jsonify(swu_start_route(request))

@app.route(consts.SPEED_TEST_URL + '/<action>', methods=['GET', 'POST'])
#@jwt_required()
def speedtestroute(action):
    return jsonify(mockedDataRequest(request, 'speedtest'))

@app.route(consts.SPECTRUM_RANGE_URL, methods=['GET'])
#@jwt_required()
def spectrumrangeroute():
	return jsonify(mockedDataRequest(request, 'spectrum-range'))

@app.route(consts.START_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstartroute():
	return jsonify(mockedDataRequest(request, 'spectrum-start'))

@app.route(consts.STOP_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstoproute():
	return jsonify(mockedDataRequest(request, 'spectrum-stop'))

@app.route(consts.SPECTRUM_TABLE_URL, methods=['GET'])
#@jwt_required()
def spectrumtableroute():
	return jsonify(mockedDataRequest(request, 'spectrum-table'))

@app.route(consts.LICENSE_ACTIVATION_URL, methods=['GET', 'POST'])
#@jwt_required()
def activatelicenseroute():
	return jsonify(license_activation(request))

@app.route(consts.DIAGNOSTICS_URL, methods=['GET'])
#@jwt_required()
def diagnostics():
	return get_diagnostics(request)

########################################## Debug URLS ############################################

@app.route(consts.DEBUG_LOG_URL, methods=['GET'])
def debuglogroute():
	return debug_log_route()

@app.route(consts.DEBUG_ATTRIBUTE_URL, methods=['GET', 'POST'])
def debugattributeurl():
	return jsonify(debug_attribute_route(request))


#DeviceMode
@app.route(consts.DEVICE_MODE_URL, methods=['GET'])
#@jwt_required()
def devicemoderoute():
    return jsonify(devicemode_route())