


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