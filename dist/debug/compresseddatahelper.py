import ipaddress, random, sys, datetime
from FlaskServer import radlogger
from FlaskServer import converters
from FlaskServer.utils import *
#from FlaskServer.Routes.Monitor.modulation import *
import string

BITS_NUM_IN_BITS = 1000000.0
BITS_NUM_IN_KBITS = 1000.0

def hexToDecimal(hex , base = 10): 
    return int(hex , base)

def parse_HBS_static(raw_value):
    names = ['hbsLocation', 'hbsIp', 'hbsSubnetMask', 'hbsAntennaType', 'hbsAgentVersion', 'hbsName']

    if not raw_value:
        return None

    result = {}
    splitted = str(raw_value).split(',')
    if not splitted or len(splitted) != 6:
        return result

    # Example data: London,0A674D64,FFFFFF00,4,3155,SuperName
    for idx, name in enumerate(names):
        result[name] = splitted[idx]

    try:
        # Convert hex -> decimal -> ip
        result[names[1]] = str(ipaddress.IPv4Address(int(result[names[1]], 16)))
    except:
        radlogger.log('parse_HBS_static method.', sys.exc_info())
        return None

    try:
        # Convert hex -> decimal -> subnet mask
        result[names[2]] = str(ipaddress.IPv4Address(int(result[names[2]], 16)))
    except:
        radlogger.log('parse_HBS_static method.', sys.exc_info())
        return None

    return result


def parse_HSU_static(raw_value):
    if not raw_value:
        return None
    if raw_value == 'No Link':
        return 'No Link'

    result = {}
    splitted = str(raw_value).split(',')
    result['SessionID'] =  splitted[0]
    result['hsuIpAddress'] = convert_ip_adress(splitted[1])
    result['hsuName'] = splitted[2]
    result['hsuLocation'] = splitted[3]
    result['hsuSerialNumber'] = splitted[4]
    result['hsuMACAddress'] = splitted[5]    
    result['AirLinkRange'] = hexToDecimal(splitted[6])
    result['MaxThroughputDown'] = hexToDecimal(splitted[7] , 16)
    result['MaxThroughputUp'] = hexToDecimal(splitted[8] , 16)
    result['CpacityLimit'] = hexToDecimal(splitted[9] , 16)
    result['hsuAntennaType'] = hexToDecimal(splitted[10])
    result['AggregateCapacity'] = hexToDecimal(splitted[11] , 16)

    return result


def convert_sw_capabilities(raw_value): 
    if not raw_value:
        return None
    splitted = list(raw_value)
    SwFeature = {}
    SwFeatureNames = ['AutoReAlignment', 'RemoteTrapMode' , 'DynamicChannelBandwidth' , 'Ttl' , 'DhcpRelay', 'IpV6', 'SnmpV3' ,
                      'Security' , 'TurboGain' , 'Wifi' ,'Lan1PortConfig', 'Lan2PortConfig' , 'Gps' , 'Tc1588' , 'SyncE' , 'Hss' ,
                      'Atpc' , 'Buzzer' , 'Dfs', 'Aes256' , 'HsuPoe' , 'Mobility' , 'SingleHsuMode' , 'SSH' ,'SFP' ,'LinuxSwu' ]

    for index , val in enumerate(splitted):
        if index >= len(SwFeatureNames) :
           return SwFeature

        SwFeature[SwFeatureNames[index]] = val

    return SwFeature



def parse_HBS_air_monitor(raw_value):
    if not raw_value:
        return None

    result = {}
    splitted = str(raw_value).split('|')

    result['InBytes'] = hexToDecimal(splitted[0] + splitted[1] + splitted[2] + splitted[3] , 16)
    result['OutBytes'] = hexToDecimal(splitted[4] + splitted[5] + splitted[6] + splitted[7] , 16)
    result['InFrames'] = hexToDecimal(splitted[8] + splitted[9] + splitted[10] + splitted[11] , 16)
    result['OutFrames'] = hexToDecimal(splitted[12] + splitted[13] + splitted[14] + splitted[15] , 16)
    result['HBSState'] = hexToDecimal(splitted[16])
    result['HBSFreq'] = hexToDecimal(splitted[17] + splitted[18] + splitted[19] + splitted[20] , 16)
    result['NumberOfLinks'] = hexToDecimal(splitted[21] + splitted[22] ,16)
    result['ECChangeCounter'] = hexToDecimal(splitted[23] + splitted[24] + splitted[25] + splitted[26] , 16)
    result['CurrentRatio'] = hexToDecimal(splitted[27] + splitted[28] , 16)
    result['TotalAirFrames'] = hexToDecimal(splitted[29] + splitted[30] + splitted[31] + splitted[32] , 16)
    result['HBSRxRateInKbps'] = hexToDecimal(splitted[33] + splitted[34] + splitted[35] + splitted[36] , 16)
    result['HBSTxRateInKbps'] = hexToDecimal(splitted[37] + splitted[38] + splitted[39] + splitted[40] , 16)
    result['HBSRxRateInFps'] = hexToDecimal(splitted[41] + splitted[42] + splitted[43] + splitted[44] , 16)
    result['HBSTxRateInFps'] = hexToDecimal(splitted[45] + splitted[46] + splitted[47] + splitted[48] , 16)
    result['HBSSetMode'] = hexToDecimal(splitted[49])
    result['hbsLan1RxMbps'] = convert_kbps_to_mbps([ int(splitted[50]) , int(splitted[51]) , int(splitted[52]) , int(splitted[53]) ])
    result['hbsLan1TxMbps'] = convert_kbps_to_mbps([ int(splitted[54]) , int(splitted[55]) , int(splitted[56]) , int(splitted[57]) ])
    result['hbsLan1RxFps'] = hexToDecimal(splitted[58] + splitted[59] + splitted[60] + splitted[61] , 16)
    result['hbsLan1TxFps'] = hexToDecimal(splitted[58] + splitted[59] + splitted[60] + splitted[61] , 16)
    result['hbsLan2RxMbps'] = convert_kbps_to_mbps([ int(splitted[62]) , int(splitted[63]) , int(splitted[64]) , int(splitted[65]) ])
    result['hbsLan2TxMbps'] = convert_kbps_to_mbps([ int(splitted[66]) , int(splitted[67]) , int(splitted[68]) , int(splitted[69]) ])
    result['hbsLan2RxFps'] = hexToDecimal(splitted[70] + splitted[71] + splitted[72] + splitted[73] , 16)
    result['hbsLan2TxFps'] = hexToDecimal(splitted[74] + splitted[75] + splitted[76] + splitted[77] , 16)
    result['SyncEPerformance'] = hexToDecimal(splitted[78])
    result['MaxAvailableBEHSUs'] = hexToDecimal(splitted[79])

    data = {}
    necessary_data = ['hbsLan1RxMbps' , 'hbsLan1TxMbps', 'hbsLan2RxMbps' , 'hbsLan2TxMbps']
    
    for val in necessary_data:
        data[val] = result[val]

    return data




def parse_HBS_monitor(raw_value):

    if not raw_value:
        return None

    result = {}

    splitted = str(raw_value).split('|')
    result['hsuLinkState'] =  hexToDecimal(splitted[0])
    result['LinkWorkingMode'] = hexToDecimal(splitted[1])
    result['Session Id'] = hexToDecimal(splitted[2] + splitted[3] + splitted[4] + splitted[5] , 16)



    result['hbsTput'] = convert_hex_to_bps([int(splitted[6]) ,int(splitted[7]) , int(splitted[8]) ,int(splitted[9])])
    #result['hbsTput'] = hexToDecimal(splitted[6] + splitted[7] + splitted[8] + splitted[9] , 16)

    result['hsuTput'] = convert_hex_to_bps([int(splitted[10]) ,int(splitted[11]) , int(splitted[12]) , int(splitted[16])])
    #result['hsuTput'] = hexToDecimal(splitted[10] + splitted[11] + splitted[12] + splitted[13] , 16)


    result['hbsRss'] = (hexToDecimal(splitted[14])) - 255
    result['hbsRssBalance '] = hexToDecimal(splitted[15])  
    result['hsuRss'] = (hexToDecimal(splitted[16])) - 255
    result['hsuRssBalance'] = hexToDecimal(splitted[17])
    result['TxOperationMode'] = hexToDecimal(splitted[18])
    result['hsuInBytes'] = hexToDecimal(splitted[19] + splitted[20] + splitted[21] + splitted[22] , 16)
    result['hsuOutBytes'] = hexToDecimal(splitted[23] + splitted[24] + splitted[25] + splitted[26] , 16)
    result['hsuInFrames'] = hexToDecimal(splitted[27] + splitted[28] + splitted[29] + splitted[30] , 16)
    result['hsuOutFrames'] = hexToDecimal(splitted[31] + splitted[32] + splitted[33] + splitted[34] , 16)
    result['hsuID'] = hexToDecimal(splitted[35])
    result['hsuRxRateInKbps'] = hexToDecimal(splitted[36] + splitted[37] + splitted[38] + splitted[39] , 16)
    result['hsuTxRateInKbps'] = hexToDecimal(splitted[40] + splitted[41] + splitted[42] + splitted[43] , 16)
    result['hsuRxRateInFps'] = hexToDecimal(splitted[44] + splitted[45] + splitted[46] + splitted[47] , 16)
    result['hsuTxRateInFps'] = hexToDecimal(splitted[48] + splitted[49] + splitted[50] + splitted[51] , 16)
    result['DLdirection'] = hexToDecimal(splitted[52] + splitted[53] + splitted[54] + splitted[55] , 16)
    result['ULdirection'] = hexToDecimal(splitted[56] + splitted[57] + splitted[58] + splitted[59] , 16)
    result['NumberOfLocalChangesAtHSU'] = hexToDecimal(splitted[60])
    result['AlignmentStatus'] = hexToDecimal(splitted[61])
    result['hbsChain1Rss'] = hexToDecimal(splitted[62])
    result['hbsChain2Rss'] = hexToDecimal(splitted[63])
    result['hbsChain3Rss'] = hexToDecimal(splitted[64])
    result['hsuChain1Rss'] = hexToDecimal(splitted[65])
    result['hsuChain2Rss'] = hexToDecimal(splitted[66])
    result['hsuChain3Rss'] = hexToDecimal(splitted[67])
    result['hsuCurrentRateIndex'] = hexToDecimal(splitted[68] + splitted[69])
    result['hsuCurrentRateCBW'] = hexToDecimal(splitted[70])
    result['hsuCurrentRateGI'] = hexToDecimal(splitted[71])
    result['hbsCurrentRateIndex'] = hexToDecimal(splitted[72] + splitted[73])
    result['hbsCurrentRateCBW'] = hexToDecimal(splitted[74])
    result['hbsCurrentRateGI'] = hexToDecimal(splitted[75])
    result['BsaAzimuth'] = hexToDecimal(splitted[76] + splitted[77] , 16)
     
    result['hsuLan1RxMbps'] =  convert_kbps_to_mbps( [ int(splitted[78]) , int(splitted[79]) , int(splitted[80]) , int(splitted[81]) ])
    result['hsuLan1TxMbps'] = convert_kbps_to_mbps([ int(splitted[82]) , int(splitted[83]) , int(splitted[84]) , int(splitted[85]) ])
    result['hsuLan1RxFps'] = hexToDecimal(splitted[86] + splitted[87] + splitted[88] + splitted[89] , 16)
    result['hsuLan1TxFps'] = hexToDecimal(splitted[90] + splitted[91] + splitted[92] + splitted[93] , 16)

    result['hsuLan2RxMbps'] = convert_kbps_to_mbps([ int(splitted[94]) , int(splitted[95]) , int(splitted[96]) , int(splitted[97]) ])
    result['hsuLan2TxMbps'] = convert_kbps_to_mbps([ int(splitted[98]) , int(splitted[99]) , int(splitted[100]) , int(splitted[101]) ])
    result['hsuLan2RxFps'] = hexToDecimal(splitted[102] + splitted[103] + splitted[104] + splitted[105] , 16)
    result['hsuLan2TxFps'] = hexToDecimal(splitted[106] + splitted[107] + splitted[108] + splitted[109] , 16)


    result['1588TCPerformance'] = hexToDecimal(splitted[110])
    result['SyncEPerformance'] = hexToDecimal(splitted[111])
    result['ATPCstatus'] = hexToDecimal(splitted[112])
    result['hbsSpeed'] = hexToDecimal(splitted[113] + splitted[114] + splitted[115] + splitted[116] , 16)
    result['hsuSpeed'] = hexToDecimal(splitted[117] + splitted[118] + splitted[119] + splitted[120] , 16)
    #result['Reserved'] = hexToDecimal(splitted[121] + splitted[122] + splitted[123] + splitted[124] + splitted[125] + splitted[126] + splitted[127] + splitted[128])

    data = {}
    necessary_data = ['hsuLan2RxMbps' , 'hsuLan2TxMbps', 'hsuLan1RxMbps' , 
                      'hsuLan1TxMbps' , 'hbsRss' ,'hsuRss' ,'DLdirection', 'hsuTput' , 'hbsTput' ,
                      'ULdirection' , 'hsuCurrentRateIndex','hsuCurrentRateCBW', 'hbsSpeed', 'hsuSpeed',
                      'hsuCurrentRateCBW','hsuCurrentRateGI', 'hbsCurrentRateIndex',  'hbsCurrentRateCBW',  'hbsCurrentRateGI'
                       ]
    
    for val in necessary_data:
        data[val] = result[val]

    return data

def parse_hsu_monitor(raw_value):
    if not raw_value:
        return None

    try:
    
        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.strip('|').split('|')
        else:
            splitted = raw_value.split()

        byte_array = [int(i) for i in splitted if i != '']
    
        lan1_rx_bytes = [byte_array[16], byte_array[17], byte_array[18], byte_array[19]]
        lan1_tx_bytes = [byte_array[20], byte_array[21], byte_array[22], byte_array[23]]
        lan1_rx_frames = [byte_array[24], byte_array[25], byte_array[26], byte_array[27]]
        lan1_tx_frames = [byte_array[28], byte_array[29], byte_array[30], byte_array[31]]

        atpcStateDict = parceAtpcData(byte_array[50])
        installConfirmReq = 'True' if byte_array[51] == '1' else "False"

        parsed_list = [convert_kbps_to_mbps(lan1_rx_bytes), 
                convert_kbps_to_mbps(lan1_tx_bytes),
                convert_to_frames(lan1_rx_frames),
                convert_to_frames(lan1_tx_frames)]

        result = {}
        result['hsuLan1RxMbps'] = parsed_list[0]
        result['hsuLan1TxMbps'] = parsed_list[1]
        result['hsuLan1RxFps'] = parsed_list[2]
        result['hsuLan1TxFps'] = parsed_list[3]

        result['installConfirmRequired'] = installConfirmReq
        if (atpcStateDict):
            allKeys = atpcStateDict.keys()
            for key in allKeys:
                result[key] = atpcStateDict[key]

        return result
    except:
        radlogger.log('parse_hsu_monitor method.', sys.exc_info())
        return None

def parse_hbs_remote_monitor(raw_value):
    try:
        if not raw_value:
            return None

        names = ["hbsRss", "hbsTput", "hbsLan1RxMbps", "hbsLan1TxMbps" , "txRatio"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        byteArray = [int(i) for i in splitted if i != '']

        hbs_rss =  byteArray[0] - 255                
        hbs_tput = [byteArray[2], byteArray[3], byteArray[4], byteArray[5]]
        hbs_lan1_rx_bytes = [byteArray[63], byteArray[64], byteArray[65], byteArray[66]]
        hbs_lan1_tx_bytes = [byteArray[67], byteArray[68], byteArray[69], byteArray[70]]

        hex1 = ''.join('{:02x}'.format(byteArray[54]))
        hex2 = ''.join('{:02x}'.format(byteArray[55]))
        hex3 = hex1 + hex2;

        hbs_tx_ratio  = hexToDecimal(hex3 , 16) 

  
        #hbs_tx_ratio      = (int((str(byteArray[54] , 2)) + (str(byteArray[55] ,2)) , 2)) / 10
        parsed_list = [hbs_rss,
                       convert_hex_to_bps(hbs_tput),
                       convert_kbps_to_mbps(hbs_lan1_rx_bytes),
                       convert_kbps_to_mbps(hbs_lan1_tx_bytes),
                       hbs_tx_ratio]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        radlogger.log('parse_hbs_remote_monitor method.', sys.exc_info())
        return None   


def parse_hbs_monitor_modulation(raw_value):
    try:
        if not raw_value:
            return None

        names = ["hbsModulationRate"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        byteArray = [int(i) for i in splitted if i != '']

        hbs_rate_index_bytes = str(byteArray[59] + byteArray[60])
        hbs_rate_cbw_bytes = str(byteArray[61])
        hbs_rate_gi_bytes = str(byteArray[62])

         # Build modulation string for hbs
        hbsModulationRate = createStringModulation(hbs_rate_index_bytes, hbs_rate_cbw_bytes, hbs_rate_gi_bytes)

        parsed_list = [hbsModulationRate]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        radlogger.log('parse_hbs_monitor method.', sys.exc_info())
        return None   

def parceAtpcData(number):

    atpcDict = {}
    atpcDict['atpcSupported'] = ''
    atpcDict['atpcStstus'] = converters.ATPC_STATUSES['0']
    atpcDict['atpcRequiredRateAchieved'] = ''
    atpcDict['atpcNumberOfLoweredDbs'] = ''

    try:
        stringInBits = bin(number)
        bitmask = stringInBits[2:]

        atpcDict['atpcSupported'] = 'True' if bitmask[0:1] == '1' else 'False'
        if atpcDict['atpcSupported'] == 'True':
            status = int(bitmask[1:2], 2)
            requiredRateAchieved = bitmask[3:4]
            numberOfLoweredDbs = int(bitmask[4:], 2)

            atpcDict['atpcStstus'] = converters.ATPC_STATUSES[str(status)]
            atpcDict['atpcRequiredRateAchieved'] = 'True' if requiredRateAchieved == '1' else 'False'
            atpcDict['atpcNumberOfLoweredDbs'] = numberOfLoweredDbs
            return atpcDict
    except:
        radlogger.log('parceAtpcData method.', sys.exc_info())
        return atpcDict

def parse_spectrum_compressed(raw_value):
    names = ["frequency", "scanned", "timestamp", 
             "lastNFAntennaA", "lastNFAntennaB", 
             "avgNFAntennaA", "avgNFAntennaB",
             "maxNFAntennaA", "maxNFAntennaB",
             "cacPerformed", "lastCACTimestamp",
             "radarDetected", "radarDetectedTimestamp",
             "channelAvailable", "maxBeaconRSS"]

    if not raw_value:
        return None
    
    # Split string to list of integers
    if '|' in raw_value:
        splitted = raw_value.strip('|').split('|')
    else:
        splitted = raw_value.split()

def convert_kbps_to_mbps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    to_mbps = round(to_int / BITS_NUM_IN_KBITS, 1)

    return to_mbps

def convert_bps_to_mbps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    to_mbps = round(to_int / BITS_NUM_IN_BITS, 1)

    return to_mbps


def convert_ip_adress(ipAddr):
    hex1 = int(ipAddr[0:2], 16);
    hex2 = int(ipAddr[2:4], 16);
    hex3 = int(ipAddr[4:6], 16);
    hex4 = int(ipAddr[6:8], 16);
    ip = ''.join('{0}.{1}.{2}.{3}'.format(hex1, hex2, hex3, hex4))
    return ip

def convert_hex_to_bps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def convert_to_frames(byte_array):
    
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def convert_hex_to_int(byte_array):
    
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def calc_current_eth_tput(raw_value):
    
    value = int(raw_value)
    return value
    #if value == -1:
    #    return -1
    #if value >= 0:
    #    return round(value / BITS_NUM_IN_BITS, 1 if value > BITS_NUM_IN_BITS else 2)

def parse_speed_test(raw_value):
    try:
        if not raw_value:
            return None

        names = ["dlSpeed", "ulSpeed"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        byteArray = [int(i) for i in splitted if i != '']

        download_speed = [byteArray[96], byteArray[97], byteArray[98], byteArray[99]] 
        upload_speed = [byteArray[100], byteArray[101], byteArray[102], byteArray[103]] 
        
        parsed_list = [convert_bps_to_mbps(download_speed),
                       convert_bps_to_mbps(upload_speed)]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return 0






def parse_speed_test_hbs(raw_value):
    try:
        if not raw_value:
            return None


        names = ["dlSpeed", "ulSpeed"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        #result['hbsSpeed'] = hexToDecimal(splitted[113] + splitted[114] + splitted[115] + splitted[116] , 16)
        #result['hsuSpeed'] = hexToDecimal(splitted[117] + splitted[118] + splitted[119] + splitted[120] , 16)

        byteArray = [int(i) for i in splitted if i != '']

        download_speed = [byteArray[113], byteArray[114], byteArray[115], byteArray[116]] 
        upload_speed = [byteArray[117], byteArray[118], byteArray[119], byteArray[120]] 
        
        parsed_list = [convert_bps_to_mbps(download_speed),
                       convert_bps_to_mbps(upload_speed)]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return 0

def convert_oct_to_date(raw_value):
    try:
        if not raw_value:
            return None

        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()
        
        byteArray = [int(i) for i in splitted if i != '']

        hex1 = ''.join('{:02x}'.format(byteArray[0]))
        hex2 = ''.join('{:02x}'.format(byteArray[1]))
        year = int(hex1 + hex2, 16)
        month = byteArray[2]
        day = byteArray[3]
        hour = byteArray[4]
        min = byteArray[5]
        sec = byteArray[6]

        date = datetime.datetime(year,month, day, hour, min, sec)
        return date.isoformat()
    except:
        radlogger.log('convert_oct_to_date.', sys.exc_info())
        return 0




def createStringModulation (currentRateIdx , currentRateCBW , currentRateGI):

        withGi = False
        if len(currentRateIdx) < 3:
            return ''
        rateInd = int(currentRateIdx)
        cbw = int(currentRateCBW)
        gi = False

        if rateInd < 100 | rateInd > 309:
            return ''
        if cbw >= 0: #new rates (3.6)
            withGi = True
            if '1' == currentRateGI:
                gi = True
            else:
                gi = False
        else:
            return ''
        rateTable = getRateMappingTable()
        mcsTable = getMcsIndexTable()

        if withGi: #get cbw value from index
                cbw = getCbwIndexMapping(cbw + 1)  #in ODU the first index = 0
            #protect not valid rates
        if not rateTable[cbw].has_key(rateInd):
                return ''
        rate = rateTable[cbw][rateInd];

        #old rate presentation
        if not withGi:
            return rate + "Mbps (" + mcsTable[rateInd] + ")"

        #new rate presentation
        if gi:
            rate = round((rate * 10) / (float)(9.0), 1)

        rateTemp = str(rate)[0:(len(str(rate))-2)]

        if rateTemp!='':
            if int(rateTemp) == rate:
                rate = int(rateTemp)

        return str(rate) + "Mbps (" + str(mcsTable[rateInd]) + ") " + str(cbw) + "MHz"


def getRateMappingTable():
    rateMappingTable5M = {
				            100: 1.625, 
				            101: 3.25,  
				            102: 4.875, 
				            103: 6.5,   
				            104: 9.75,  
				            105: 13,    
				            106: 14.625,
				            107: 16.25, 
				            108: 19.5,  
				            # 9 n/a
				            200: 3.25,  
				            201: 6.5,   
				            202: 9.75,  
				            203: 13,    
				            204: 19.5,  
				            205: 26,    
				            206: 29.25, 
				            207: 32.5,  
				            208: 39,  
				            # 9 n/a              
				            300: 4.875,    # 0
				            301: 9.75,     # 1
				            302: 14.625,   # 2
				            303: 19.5,     # 3
				            304: 29.25,    # 4
				            305: 39,       # 5
				            306: 43.875,   # 6
				            307: 48.75,    # 7
				            308: 58.5,     # 8
				            309: 65       # 9
				         }

    rateMappingTable10M = {
				             100: 3.25,
				             101: 6.5,
				             102: 9.75,
				             103: 13,
				             104: 19.5,
				             105: 26,
				             106: 29.25,
				             107: 32.5,
				             108: 39,
				             # 9 n/a
				             200: 6.5,
				             201: 13,
				             202: 19.5,
				             203: 26,
				             204: 39,
				             205: 52,
				             206: 58.5,
				             207: 65,
				             208: 78,
				             # 9 n/a
				             300: 9.75,     # 0
				             301: 19.5,     # 1
				             302: 29.25,    # 2
				             303: 39,       # 3
				             304: 58.5,     # 4
				             305: 78,       # 5
				             306: 87.75,    # 6
				             307: 97.5,     # 7
				             308: 117,      # 8
				             309: 130       # 9
				          }

    rateMappingTable20M = {
				            100: 6.5,
				            101: 13,
				            102: 19.5,
				            103: 26,
				            104: 39,
				            105: 52,
				            106: 58.5,
				            107: 65,
				            108: 78,
				            # 9 n/a
				            200: 13,
				            201: 26,
				            202: 39,
				            203: 52,
				            204: 78,
				            205: 104,
				            206: 117,
				            207: 130,
				            208: 156,
				            # 9 n/a
				            300: 19.5,   # 0
				            301: 39,     # 1
				            302: 58.5,   # 2
				            303: 78,     # 3
				            304: 117,    # 4
				            305: 156,    # 5
				            306: 175.5,  # 6
				            307: 195,    # 7
				            308: 234,    # 8
				            309: 260    # 9
				          }

    rateMappingTable40M = {
				             100: 13.5,
				             101: 27,
				             102: 40.5,
				             103: 54,
				             104: 81,
				             105: 108,
				             106: 121.5,
				             107: 135,
				             108: 162,
				             109: 180,
				             200: 27,
				             201: 54,
				             202: 81,
				             203: 108,
				             204: 162,
				             205: 216,
				             206: 243,
				             207: 270,
				             208: 324,
				             209: 360,
				             300: 40.5,
				             301: 81,
				             302: 121.5,
				             303: 162,
				             304: 243,
				             305: 324,
				             306: 364.5,
				             307: 405,
				             308: 486,
				             309: 540,
				          }
              
    rateMappingTable80M = {
				             100: 29.3,
				             101: 58.5,
				             102: 87.8,
				             103: 117,
				             104: 175.5,
				             105: 234,
				             106: 263.3,
				             107: 292.5,
				             108: 351,
				             109: 390,
				             200: 58.5,
				             201: 117,
				             202: 175.5,
				             203: 234,
				             204: 351,
				             205: 468,
				             206: 526.5,
				             207: 585,
				             208: 702,
				             209: 780,
				             300: 87.8,
				             301: 175.5,
				             302: 263.3,
				             303: 351,
				             304: 526.5,
				             305: 702,
				             # 6 n/a
				             307: 877.5,
				             308: 1053,
				             309: 1170,
				          }
                  
    rateMappingTable7M = {
				             100: 2.5,
				             101: 5,
				             102: 7.5,
				             103: 10,
				             104: 15.1,
				             105: 20.1,
				             106: 22.6,
				             107: 25.1,
				             108: 30.1,
				             # 9 n/a
				             200: 5,
				             201: 10,
				             202: 15.1,
				             203: 20.1,
				             204: 30.1,
				             205: 40.2,
				             206: 45.2,
				             207: 50.2,
				             208: 60.3,
				             # 9 n/a
				             300: 15.1,    
				             301: 30.1,    
				             302: 45.2,   
				             303: 60.3,    
				             304: 90.4,   
				             305: 120.5,   
				             306: 135.6,   
				             307: 150.7,   
				             308: 180.8,   
				             309: 200.9,   
				         }
                    
    rateMappingTable14M = {
				                100: 5,
				                101: 10,
				                102: 15.1,
				                103: 20.1,
				                104: 30.1,
				                105: 40.2,
				                106: 45.2,
				                107: 50.2,
				                108: 60.3,
				                # 9 n/a
				                200: 10,
				                201: 20.1,
				                202: 30.1,
				                203: 40.2,
				                204: 60.3,
				                205: 80.4,
				                206: 90.4,
				                207: 100.5,
				                208: 120.5,
				                # 9 n/a
				                300: 30.1,     
				                301: 60.3,     
				                302: 90.4,    
				                303: 120.5,       
				                304: 180.8,     
				                305: 241.1,       
				                306: 271.2,    
				                307: 301.4,     
				                308: 361.6,      
				                309: 401.8,      
				             }

    rateMappingTable = {                                                                                                                    
                            5 : rateMappingTable5M ,
                            10: rateMappingTable10M,
                            20: rateMappingTable20M,
                            40: rateMappingTable40M,
                            80: rateMappingTable80M,
                            7 : rateMappingTable7M ,
                            14: rateMappingTable14M
                         }

    return rateMappingTable
   
    
def getMcsIndexTable():
            #create table
            mcsIndexTable = {
                100: "1xBPSK 1/2",
                101: "1xQPSK 1/2",
                102: "1xQPSK 3/4",
                103: "1x16-QAM 1/2",
                104: "1x16-QAM 3/4",
                105: "1x64-QAM 2/3",
                106: "1x64-QAM 3/4",
                107: "1x64-QAM 5/6",
                108: "1x256-QAM 3/4",
                109: "1x256-QAM 5/6",
                200: "2xBPSK 1/2",
                201: "2xQPSK 1/2",
                202: "2xQPSK 3/4",
                203: "2x16-QAM 1/2",
                204: "2x16-QAM 3/4",
                205: "2x64-QAM 2/3",
                206: "2x64-QAM 3/4",
                207: "2x64-QAM 5/6",
                208: "2x256-QAM 3/4",
                209: "2x256-QAM 5/6",
                300: "3xBPSK 1/2",
                301: "3xQPSK 1/2",
                302: "3xQPSK 3/4",
                303: "3x16-QAM 1/2",
                304: "3x16-QAM 3/4",
                305: "3x64-QAM 2/3",
                306: "3x64-QAM 3/4",
                307: "3x64-QAM 5/6",
                308: "3x256-QAM 3/4",
                309: "3x256-QAM 5/6"
            }
            return mcsIndexTable    
        
def getCbwIndexMapping (index):
           cbwIndexMapping = {
                                1: 5,
                                2: 10,
                                3: 20,
                                4: 40,
                                5: 80,
                                6: 7,
                                7: 14
                            }   
           return  cbwIndexMapping.get(index)   

