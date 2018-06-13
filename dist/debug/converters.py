from FlaskServer.Resources import en as resource

WI_SUPPORT_HTTPS = {
    "1": "mandatoryDisabled",
    "2": "mandatoryEnabled",
    "3": "disabled",
    "4": "enabled",
    "5": "securedOnlyEnabled",
    "6": "securedDisabled",
    "7": "securedAllModesEnabled",
    "8": "securedAllModesDisabled"
}

TRAP_SNMP_MODE = { 
    "1": resource.snmpv1, 
    "3": resource.snmpv3,
    # Convert back
    resource.snmpv1: "1", 
    resource.snmpv3: "3"
}

SERVICE_TYPE_CONVERTER = {
    '1' : 'cir',
    '2' : 'be',
    'cir' : '1',
    'be' : '2'
}

ACTUAL_CONNECT_MODE = {
    '1': 'none',
    '2': 'ptp',
    '3': 'ptmp'
}

SYSTEM_OBJECT_ID = {
"5": "HBS",
"6": "HSU",
"3": "SN"
}

HSU_LINK_STATE = {
    "0": "N/A",
    "1": resource.linkOff,
    "2": resource.violated,
    "3": resource.unregistered,
    "4": resource.registered,
    "5": resource.authenticationError,
    "6": resource.swUpgradeRequired,
    "7": resource.registeredPassive
}
HSU_AIR_STATE = { 
    "0": "N/A",
    "2": resource.air_state_bit_failed,
    "3": resource.air_state_alignment_required,
    "4": resource.air_state_spectrum_measurment,
    "5": resource.air_state_scanning,
    "6": resource.air_state_cac,
    "7": resource.air_state_transceiving,
    "8": resource.air_state_stand_by,
    "9": resource.air_state_raw_alignment,
    "10": resource.air_state_unreachable
    }

HBS_AIR_STATE = { 
    "0": 'N/A',
    "1": 'init',
    "2": resource.air_state_bit_failed,
    "3": resource.air_state_inactive,
    "4": resource.air_state_spectrum_measurment,
    "5": resource.air_state_scanning,
    "6": resource.air_state_cac,
    "7": resource.air_state_transceiving,
    "8": resource.air_state_stand_by,
    "9": resource.air_state_raw_alignment,
    "10": resource.air_state_unreachable
    }


HBS_LINK_STATE = { 
    "0": "N/A",
    "1": 'noSync',
    "2": 'violated',
    "3": 'syncUnregistered',
    "4": 'syncRegistered',
    "5": 'authenticationError',
    "6": 'swUpgradeRequired',
    "7": 'syncRegisteredPassive',
    "8": 'syncRegisteredALP'
    }


ANTENNA_TYPE = { 
    "-1": resource.antenna_none,
    "1": resource.antenna_single,
    "2": resource.antenna_dual,
    "3": resource.antenna_undefined,
    "4": resource.antenna_triple,
    # Convert back
    resource.antenna_none:      "-1",
    resource.antenna_single:    "1",
    resource.antenna_dual:      "2",
    resource.antenna_undefined: "3",
    resource.antenna_triple:    "4",
 }
ANTENNA_CONNECTION_TYPE = { 
    "-1": resource.antenna_con_type_none,
    "1": resource.antenna_con_type_external,
    "2": resource.antenna_con_type_integrated,
    "3": resource.antenna_con_type_embedded_external,
    "4": resource.antenna_con_type_embedded_integrated,
    "5": resource.antenna_con_type_integrated_bsa,
    # Convert back
    resource.antenna_con_type_none:                  "-1",
    resource.antenna_con_type_external:              "1",
    resource.antenna_con_type_integrated:            "2",
    resource.antenna_con_type_embedded_external:     "3",
    resource.antenna_con_type_embedded_integrated:   "4",
    resource.antenna_con_type_integrated_bsa:        "5"
    }
ATTACHED_ANTENNA_INDICATION = { 
    "1": resource.antenna_indication_undefined,
    "2": resource.antenna_indication_integrated,
    "3": resource.antenna_indication_turbo,
    "4": resource.antenna_indication_external,
    # Convert back
    resource.antenna_indication_undefined:    "1",
    resource.antenna_indication_integrated:   "2",
    resource.antenna_indication_turbo:        "3",
    resource.antenna_indication_external:     "4",
    }
EVENTS_SEVERITY = { 
    "1": resource.events_info,
    "2": resource.events_normal,
    "4": resource.events_warning,
    "8": resource.events_minor,
    "16": resource.events_major,
    "32": resource.events_critical
    }
LAN_CURRENT_STATUS = {
    "1": resource.lan_current_status_not_connected,
    "10": resource.lan_current_status_hd_10m,
    "11": resource.lan_current_status_fd_10m,
    "15": resource.lan_current_status_hd_100m,
    "16": resource.lan_current_status_fd_100m,
    "20": resource.lan_current_status_hd_1g,
    "21": resource.lan_current_status_fd_1g,
    "65535": resource.lan_current_status_unknown
    }
LAN_DESIRED_STATUS = {
    "1": resource.lan_desired_status_auto,
    "5": resource.lan_desired_status_auto_100m,
    "10": resource.lan_desired_status_hd_10m,
    "11": resource.lan_desired_status_fd_10m,
    "15": resource.lan_desired_status_hd_100m,
    "16": resource.lan_desired_status_fd_100m,
    "21": resource.lan_desired_status_fd_1g,
    "254": resource.lan_desired_status_disable_poe,
    "255": resource.lan_desired_status_disable,
    # Convert back
    resource.lan_desired_status_auto        : "1",
    resource.lan_desired_status_auto_100m   : "5",
    resource.lan_desired_status_hd_10m      : "10",
    resource.lan_desired_status_fd_10m      : "11",
    resource.lan_desired_status_hd_100m     : "15",
    resource.lan_desired_status_fd_100m     : "16",
    resource.lan_desired_status_fd_1g       : "21",
    resource.lan_desired_status_disable_poe : "254",
    resource.lan_desired_status_disable     : "255",
    }
WIFI_POWER_MODES = {
    "1": resource.wifi_undefined,
    "2": resource.wifi_auto,
    "3": resource.wifi_power_off,
    "4": resource.wifi_always_on,
    "5": resource.wifi_power_on,
    # Convert back
    resource.wifi_undefined  : "1",
    resource.wifi_auto   : "2",
    resource.wifi_power_off  : "3",
    resource.wifi_always_on  : "4",
    resource.wifi_power_on       : "5"
    }
WIFI_SECURITY_TYPE = {
    "1": resource.wifi_security_open,
    "2": resource.wifi_security_wep,
    "3": resource.wifi_security_wpa2,
    # Convert back
    resource.wifi_security_open  : "1",
    resource.wifi_security_wep   : "2",
    resource.wifi_security_wpa2  : "3",
    }
WIFI_AP_STATUS = {
    "1": resource.wifi_staus_off,
    "2": resource.wifi_staus_on,
    "3": resource.wifi_staus_connected,
    # Convert back
    resource.wifi_staus_off  : "1",
    resource.wifi_staus_on   : "2",
    resource.wifi_staus_connected  : "3",
    }
SPECTRUM_CHANNEL_SCANNED = {
    "1": resource.channel_not_scanned,
    "2": resource.channel_scanned,
    # Convert back
    resource.channel_not_scanned  : "1",
    resource.channel_scanned      : "2",
    }

SERVICE_HSU_TYPE = {
    '1': resource.hsu_type_fixed,
    '2': resource.hsu_type_stationary,
    '3': resource.hsu_type_mobile,
    '4': resource.hsu_type_transport,
    '5': resource.hsu_type_mobile_channel,
    '6': resource.hsu_type_residential,
    '7': resource.hsu_type_new_fixed,
    '8': resource.hsu_type_new_residential,
     # Convert back
     resource.hsu_type_fixed           : '1',
     resource.hsu_type_stationary      : '2',
     resource.hsu_type_mobile          : '3',
     resource.hsu_type_transport       : '4',
     resource.hsu_type_mobile_channel  : '5',
     resource.hsu_type_residential     : '6',
     resource.hsu_type_new_fixed       : '7',
     resource.hsu_type_new_residential : '8',
    }

SERVICE_CATEGORY_HBS_TYPE = {
    '1': 'assuredAllocation',
    '2': 'bestEffort',
    '3': 'undefined',
    }

ATPC_STATUSES = {
    '0': 'Off',
    '1': 'Max',
    '2': 'Min',
    '3': 'Dynamic',
    'Off':     '0',
    'Max':     '1',
    'Min':     '2',
    'Dynamic': '3',
}

SWU_STATUS = { 
    "1": "None",
    "2": "In Progress",
    "3": "Pending Reset",
    "4": "Error",
    # Convert back
    "None":             "1",
    "In Progress":      "2",
    "Pending Reset":    "3",
    "Error":            "4",
}

SWU_TYPE = { 
    "1": "SWU",
    "2": "RESTORE",
    # Convert back
    "SWU":           "1",
    "RESTORE":       "2",
}

SNMP_SUPPORT = {
    "1" :"enabled",
    "2" :"snmpv1Only",
    "3" :"snmpv3Only",
 }


TELNET_SUPPORT = {
    "1" :"enable",
    "2" :"disable",
    "3" :"mandatoryDisabled",
    "4" :"mandatoryEnabled",
 }

HSS_CURRENT_OP_STATE = {
"1" :"notSupported",
"2" :"independentUnit",
"3" :"hubSyncMaster",
"4" :"hubSyncClientContinueTx",
"5" :"hubSyncClientDisableTx",
"6" :"gpsSync",
"7" :"independentSyncUnit-ISU"
}

HSS_PULSE_TYPE = {
"1" :"notApplicable",
"2" :"typeA",
"3" :"typeB",
"4" :"typeC",
"5" :"typeD",
"6" :"typeE",
"7" :"typeF"
}

HSS_PULSE_STATUS = {
"1" :"notDetected",
"2" :"generating",
"3" :"generatingAndDetected",
"4" :"generatingAndImproperDetected",
"5" :"detected",
"6" :"improperDetected",
"7" :"multipleSourcesDetected"
}

HSS_DESIRED_OP_STATE = {
"1" :"notSupported",
"2" :"independentUnit",
"3" :"hubSyncMaster",
"4" :"hubSyncClientContinueTx",
"5" :"hubSyncClientDisableTx",
"6" :"gpsSync",
"7" :"independentSyncUnit-ISU"
}

HSS_SYNCP_STATUS = {
"1" :"notApplicable",
"2" :"notSynchronized",
"3" :"synchronized"
}