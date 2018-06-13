﻿"""
Routes for the flask application.
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from FlaskServer.Routes.Monitor import monitor_route
from FlaskServer.Routes.System import *
from FlaskServer.Routes.Radio import radio_route_hsu
from FlaskServer.Routes.Network import network_route
from FlaskServer.Routes.RecentEvents import recent_events_route
from FlaskServer.Routes.ActiveAlarms import active_alarms_route
from FlaskServer.Routes.TrapsDestinations import trapsdestinations_route
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
from FlaskServer.Routes.Wifi import wifi_route
from FlaskServer.Routes.Battery import battery_route
#from FlaskServer.Routes.InternalVoltages import internalVoltages_route
from FlaskServer.Routes.Sensor import sensor_route
from FlaskServer.Routes.Port import port_route
from FlaskServer.Routes.Monitor import monitor_route_SN
import FlaskServer.consts as consts 
from FlaskServer.Routes.Security import *
########################################## Data URLS ############################################

#FlaskVersionMode
@app.route(consts.FLASK_VERISON_URL, methods=['GET'])
def flaskversionroute():
    return jsonify(flask_version_route(request))


#Monitor
@app.route(consts.MONITOR_URL, methods=['GET'])
@jwt_required()
def monitorroute():
    return jsonify(monitor_route_SN(request))

#System
@app.route(consts.SYSTEM_URL, methods=['GET', 'POST'])
@jwt_required()
def systemroute():
    return jsonify(system_route(request))

#Radio
@app.route(consts.RADIO_URL, methods=['GET', 'POST'])
@jwt_required()
def radioroute():
    return jsonify(radio_route_hsu(request))

#Network
@app.route(consts.NETWORK_URL, methods=['GET', 'POST'])
@jwt_required()
def networkroute():
    return jsonify(network_route(request))

#Recent Events
@app.route(consts.RECENT_EVENTS_URL, methods=['GET'])
@jwt_required()
def recenteventsroute():
    return jsonify(recent_events_route(request))

# Active Alarms
@app.route(consts.ACTIVE_ALARMS_URL, methods=['GET'])
@jwt_required()
def activealarmstoute():
    return jsonify(active_alarms_route(request))

#Traps Destinations
@app.route(consts.TRAPS_DESTINATIONS_URL, methods=['GET', 'POST'])
@jwt_required()
def trapsroute():
    return jsonify(trapsdestinations_route(request))

#@app.route(consts.WIFI_URL, methods=['GET', 'POST'])
#@jwt_required()
#def wifiroute():
#    return jsonify(wifi_route(request))

########################################## Operations URLS ############################################

@app.route(consts.PING_URL, methods=['POST'])
@jwt_required()
def pingroute():
    return jsonify(ping(request))

@app.route(consts.TRACE_URL, methods=['POST'])
@jwt_required()
def traceroute():
    return jsonify(trace(request))

@app.route(consts.RESET_URL, methods=['POST'])
@jwt_required()
def trace_route():
    return jsonify(odu_reset())

@app.route(consts.RESYNC_URL, methods=['POST'])
@jwt_required()
def resync_route():
    return jsonify(resync())

@app.route(consts.DEREGISTER_URL, methods=['POST'])
@jwt_required()
def deregisterlocalroute():
    return jsonify(deregister_local_route(request))



@app.route(consts.SWU_UPLOAD_URL, methods=['POST'])
@jwt_required()
def swuuploadroute():
    return jsonify(swu_upload_route(request))

@app.route(consts.SWU_VALIDATE_URL, methods=['GET'])
@jwt_required()
def swuvalidateroute():
    return jsonify(swu_validate_route(request))

@app.route(consts.SWU_START_URL, methods=['POST'])
@jwt_required()
def swustartroute():
    return jsonify(swu_start_route(request))

@app.route(consts.SWU_BACKUP_URL, methods=['GET'])
@jwt_required()
def swubackuproute():
    return swu_start_backup(request)

@app.route(consts.SWU_FILE_EXISTENCE_URL, methods=['GET'])
@jwt_required()
def swuFileExistenceRoute():
    return jsonify(swu_check_file_existence(request))

@app.route(consts.SPEED_TEST_URL + '/<action>', methods=['GET', 'POST'])
@jwt_required()
def speedtestroute(action):
    return jsonify(speed_test(action, request))


@app.route(consts.DIAGNOSTICS_URL, methods=['GET'])
@jwt_required()
def diagnostics():
    return get_diagnostics(request)

@app.route(consts.LICENSE_ACTIVATION_URL, methods=['GET', 'POST'])
@jwt_required()
def activatelicenseroute():
    return jsonify(license_activation(request))

@app.route(consts.CHANGE_LINK_PASSWORD, methods=['POST'])
@jwt_required()
def changelinkpasswordroute():
    return jsonify(change_link_password(request))

@app.route(consts.RESTORE_TO_DEFAULTS_URL, methods=['POST'])
@jwt_required()
def restoretodefaultsroute():
    return jsonify(restore_to_defaults(request))

@app.route(consts.INSTALLATION_CONFIRMATION_URL, methods=['POST'])
@jwt_required()
def installationconfirmationroute():
    return jsonify(installation_confirmation(request))
########################################## Debug URLS ############################################

@app.route(consts.DEBUG_LOG_URL, methods=['GET'])
def debuglogroute():
    return debug_log_route()

@app.route(consts.DEBUG_ATTRIBUTE_URL, methods=['GET', 'POST'])
def debugattributeurl():
    return jsonify(debug_attribute_route(request))



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

#Security
@app.route(consts.SECURITY_URL, methods=['POST'])
@jwt_required()
def securityroute():
    return jsonify(security_route(request))







