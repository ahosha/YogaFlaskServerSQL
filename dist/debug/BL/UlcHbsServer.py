from FlaskServer.BL.BaseServer import BaseServer
from FlaskServer.setting import *

class UlcHbsServer(BaseServer):

   
    def __init__(self):
        self.deviceType = 'ULC' 

    def configure_instance(self):
        if WORKING_MODE == 'TestingConfig':
            from FlaskServer.utils import clean
            clean()
            import FlaskServer.BL.Routes.ULC.testroutes
        elif WORKING_MODE == 'TrainingConfig':
            import FlaskServer.BL.Routes.ULC.trainingroutes
        else:
            import FlaskServer.BL.Routes.ULC.prodroutes