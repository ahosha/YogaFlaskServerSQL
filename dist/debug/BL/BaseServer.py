import os
import logging
import logging.handlers
import datetime
from FlaskServer.utils import get_base_dir
from FlaskServer.setting import *
from FlaskServer.BL.config import *
from flask_cors import CORS

class BaseServer: 
    
    def __init__(self):
        self.deviceType = 'undefined' 

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

    def configure_instance(self):
        #import route for testing/prod
        if WORKING_MODE == 'TestingConfig':
            from FlaskServer.utils import clean
            clean()
            import FlaskServer.BL.Routes.ULC.testroutes
        elif WORKING_MODE == 'TrainingConfig':
            import FlaskServer.BL.Routes.ULC.trainingroutes
        else:
            import FlaskServer.BL.Routes.ULC.prodroutes




    

