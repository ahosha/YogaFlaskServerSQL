from rx import Observable, Observer 
from rx.subjects import BehaviorSubject
from FlaskServer.singleton import Singleton
import FlaskServer.consts as consts                                 
#class Singleton(type):
#    _instances = {}
#    def __call__(cls, *args, **kwargs):
#        if cls not in cls._instances:
#            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#        return cls._instances[cls]

class ServerState():    

    """description of class"""
    __metaclass__ = Singleton
    DEVICE_MODE = 'HBS'
    MAC_ADDRESS_HSU = ''
    LINK_STATE = ''
    NUM_OF_LINKS = 0

    monitor_data = None
    SwCapabilities =None

    def setSwCapabilities(self ,s):
        self.SwCapabilities = s
    def getSwCapabilities(self):
        self.SwCapabilities


    def setMonitor(self, d):
        self.monitor_data = d
    def getMonitor(self):
        return self.monitor_data

    #this stream will hold all hsu devices on the sector of the HBS
    hsuDevicesSub     = BehaviorSubject(None)
    registeredHsusSub = BehaviorSubject({})
    #this stream will hold the local monitor of the device
    monitorSub      = BehaviorSubject(None)

    #this stream will hold the local recentEventSub of the device
    recentEventSub  = BehaviorSubject(None)

    #api data stream
    systemSub       = BehaviorSubject(None)
    deviceModeSub   = BehaviorSubject(None)
    radioSub        = BehaviorSubject(None)
    networkSub      = BehaviorSubject(None)
    portsSub        = BehaviorSubject(None)
    wifiSub         = BehaviorSubject(None)

    #events streams
    onFlushingLogsSub = BehaviorSubject(None)

    #dispath method will use to update data on the observer
    def dispath(self , observer_name , payload):
        if observer_name == consts.MONITOR_SUB:
            self.monitorSub.on_next(payload)
            return payload
        elif observer_name == consts.SYSTEM_SUB:
            self.systemSub.on_next(payload)
            return payload
        #elif observer_name == consts.DEVICE_MODE_SUB:
        #    self.deviceModeSub.on_next(payload)
        #    return payload
        elif observer_name == consts.RADIO_SUB:
            self.radioSub.on_next(payload)
            return payload
        elif observer_name == consts.PORT_SUB:
            self.portsSub.on_next(payload)
            return payload
        elif observer_name == consts.WIFI_SUB:
            self.wifiSub.on_next(payload)
            return payload
        elif observer_name == consts.HSU_DEVICES_SUB:
            self.hsuDevicesSub.on_next(payload)
            return payload
        elif observer_name == consts.REGISTERED_HSU_SUB:
           self.registeredHsusSub.on_next(payload)
           return payload
        elif observer_name == consts.FLUSH_LOG_SUB:
           self.onFlushingLogsSub.on_next(payload)
           return payload
        else:
            print observer_name + ' is not recognize observable.'
            return None
    #select method will use to get observerable
    def select(self ,observer_name):
        if observer_name == consts.MONITOR_SUB:
           return self.monitorSub
        elif observer_name == 'network':
           return self.networkSub
        elif observer_name == consts.SYSTEM_SUB:
           return self.systemSub
        #elif observer_name == consts.DEVICE_MODE_SUB:
        #   return self.deviceModeSub
        elif observer_name == consts.RADIO_SUB:
           return self.radioSub
        elif observer_name == consts.PORT_SUB:
           return self.portsSub
        elif observer_name == consts.WIFI_SUB:
           return self.wifiSub
        elif observer_name == consts.NETWORK_SUB:
           return self.wifiSub
        elif observer_name == consts.HSU_DEVICES_SUB:
           return self.hsuDevicesSub
        elif observer_name == consts.REGISTERED_HSU_SUB:
           return self.registeredHsusSub
        elif observer_name == consts.FLUSH_LOG_SUB:
           return self.onFlushingLogsSub
        else:
            print observer_name + ' is not recognize observable.'
            return None

    def getDeviceMode(self):
        return self.DEVICE_MODE

    def setDeviceMode(self,mode):
        self.DEVICE_MODE = mode

    def getMacAdressHsu(self):
        return self.MAC_ADDRESS_HSU

    def setMacAdressHsu(self,address):
        self.MAC_ADDRESS_HSU = address

    @classmethod
    def setNumOfLinks(self , number):
        self.NUM_OF_LINKS = number

    @classmethod
    def getNumOfLinks(self):
        return self.NUM_OF_LINKS


