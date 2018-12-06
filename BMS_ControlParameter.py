''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''
import datetime

import numpy as np

Connected = False
Bus_Status_Ok = True
logDataControl = False


voltageIDs = np.arange(1281,1316,1)
temperatureIDs = np.arange(1329,1350,1)
generalsID = 257
ENERGYMETER_STROM_ID = 0x111
USER_COMMAND_CAN_MESSAGE = 0x3FF
DIS_CAN_MESSAGE = 0x41

dummyBite = [1]
getVoltagesCommand = [3]
getTemperaturesCommand = [4]
startBalancingCommand = [5]
stopBalancingCommand = [6]
fanControlCommand = 7
setUserCommand = [8]
resetUserCommand = [9]
hvSimulationCommand = [0, 0, 64, 0]
numberOfCells = 140
numberOfTempSensors = 80
defaultValues = {'cellVoltages': 0, 'cellTemperatures': 999, 'akkuVoltage': 000, 'stateOfCharge':  999, 'maxVoltage': 0,
                 'minVoltage': 0, 'maxTemperature': 999, 'minTemperature': 999}

states = {'0': 'IDLE', '1': 'Precharge', '2':'Drive', '4': 'Precharge Fail', '5': 'Data Error', '6':'Relais Stuck'}


#file = open("logData.txt", "a+")


def createLogDataFile():
    now = datetime.datetime.now()
    name = "Logdata/logData_"+now.strftime("%Y-%m-%d-%H%M")


    try:
        file = open(str(name+'.txt'), "r+")
    except Exception as e:
        file = open(str(name+'.txt'), "a+")
    file.write('logData BMS_Nanni %s' %str(now.date()))
    return file


def setConnectionState(state):
    global Connected
    Connected = state
    print("Connected=",state)


def getConnectionState():
    global Connected
    print("Connected=", Connected)
    return Connected


def setBusStatus(state):
    global Bus_Status_Ok
    Bus_Status_Ok = state


def getBusStatus():
    global Bus_Status_Ok
    return Bus_Status_Ok


def setLogDataControl(state):
    global logDataControl
    logDataControl = state

def getLogDataControl():
    global logDataControl
    return logDataControl




'''class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()


  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
    print('Timer stopped')'''