
import unittest
from FlaskServer.Routes.System.system_tester import SystemTester
from FlaskServer.Routes.Wifi.wifi_tester import WifiTester
from FlaskServer.Routes.TrapsDestinations.trap_tester import TrapTester
from FlaskServer.Routes.Sensor.sensor_tester import SensorTester
from FlaskServer.Routes.Security.security_tester import SecurityTester
from FlaskServer.Routes.RecentEvents.recentEvent_tester import RecentEventsTester
from FlaskServer.Routes.Radio.radio_tester import RadioTester
from FlaskServer.Routes.Port.port_tester import PortTester
from FlaskServer.Routes.Operations.operation_tester import OperationsTester
from FlaskServer.Routes.Network.network_tester import NetworkTester
from FlaskServer.Routes.Monitor.monitor_tester import MonitorTester
from FlaskServer.Routes.DeviceMode.deviceMode_tester import DeviceModeTester
from FlaskServer.Routes.Battery.battery_tester import BatteryTester

testers = [SystemTester , WifiTester , TrapTester , SensorTester , SecurityTester , 
           RecentEventsTester , RadioTester , PortTester , OperationsTester , NetworkTester , MonitorTester , DeviceModeTester , BatteryTester]

for testname in testers:
    suite = unittest.TestLoader().loadTestsFromTestCase(testname)
    unittest.TextTestRunner(verbosity=2).run(suite)






