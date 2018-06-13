


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ServerState():
    """description of class"""
    __metaclass__ = Singleton
    DEVICE_MODE = ''
    MAC_ADDRESS_HSU = ''
    LINK_STATE = ''

    def getDeviceMode(self):
        return self.DEVICE_MODE

    def setDeviceMode(self,mode):
        self.DEVICE_MODE = mode

    def getMacAdressHsu(self):
        return self.MAC_ADDRESS_HSU

    def setMacAdressHsu(self,address):
        self.MAC_ADDRESS_HSU = address


