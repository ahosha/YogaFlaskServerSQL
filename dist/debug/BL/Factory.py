import os
import logging
import logging.handlers
import datetime
from FlaskServer.utils import get_base_dir
from FlaskServer.BL.config import *
from FlaskServer.setting import *
from FlaskServer.BL.BaseServer import BaseServer
from FlaskServer.BL.SmartNodeServer import SmartNodeServer
from FlaskServer.BL.UlcBaseServer import UlcBaseServer
from FlaskServer.BL.UlcHbsServer import UlcHbsServer
from FlaskServer.BL.UlcHsuServer import UlcHSuServer

class Factory:
     
    def create_app_instance(self, app):
        app.config.from_object(BaseConfig)
        if DEVICE_TYPE == 'ULC':
            baseServer = UlcBaseServer()
            devicetype = baseServer.getDeviceType()
            deviceMode = baseServer.getDeviceMode()
            print('deviceMode' , deviceMode);
            
            if deviceMode == 'HBS':
               baseServer = UlcHbsServer()
            else :
               baseServer = UlcHSuServer()
            #ProductionConfig || TestingConfig  || TrainingConfig
            baseServer.configure_app(app)
        elif  DEVICE_TYPE == 'SmartNode':
            baseServer = SmartNodeServer()
            #ProductionConfig || TestingConfig  || TrainingConfig
            baseServer.configure_app(app)
            devicetype = baseServer.getDeviceType()
        elif  DEVICE_TYPE == 'HBS':
            baseServer = UlcHbsServer()
            #ProductionConfig || TestingConfig  || TrainingConfig
            baseServer.configure_app(app)
            devicetype = baseServer.getDeviceType()
        baseServer.configure_instance()
        #import runtester



