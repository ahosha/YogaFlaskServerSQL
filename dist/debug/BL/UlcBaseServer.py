import os
import logging
import logging.handlers
import datetime
from FlaskServer.utils import get_base_dir
from FlaskServer.setting import *
from FlaskServer.BL.BaseServer import *
from FlaskServer.BL.config import *
from FlaskServer.Routes.DeviceMode import *
from flask_cors import CORS


class UlcBaseServer(BaseServer): 
    
    def __init__(self):
        self.deviceType = 'UlcBaseServer' 

    def configure_app(self, app):
        app.config.from_object(BaseConfig)
        CORS(app, supports_credentials=True)
        # Configure logging
        file_handler = logging.handlers.RotatingFileHandler(app.config['LOG_FILENAME'], maxBytes=10000, backupCount=1)
        file_handler.setLevel(app.config['LOG_LEVEL'])
        f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(message)s|', '%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(f)
        app.logger.addHandler(file_handler)
        
    def getDeviceType(self):
        return self.deviceType

    def getDeviceMode(self):
        devicemode = devicemode_route()
        data = devicemode['data']
        res =  devicemode['data']['sysObjectId']
        return res

