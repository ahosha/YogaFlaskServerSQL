from FlaskServer.BL.BaseServer import BaseServer
from FlaskServer.setting import *

class SmartNodeServer(BaseServer):

   
    def __init__(self):
        self.deviceType = 'SmartNode' 
    

    def configure_instance(self):
        if WORKING_MODE == 'TestingConfig':
            from FlaskServer.utils import clean
            clean()
            import FlaskServer.BL.Routes.SmartNode.testroutes
        elif WORKING_MODE == 'TrainingConfig':
            import FlaskServer.BL.Routes.SmartNode.trainingroutes
        else:
            import FlaskServer.BL.Routes.SmartNode.prodroutes