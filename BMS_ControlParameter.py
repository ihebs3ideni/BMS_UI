''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''
import numpy as np

Connected = False

voltageIDs = np.arange(1281,1316,1)
temperatureIDs = np.arange(1329,1350,1)
generalsID = 257
ENERGYMETER_STROM_ID = 0x111
USER_COMMAND_CAN_MESSAGE = 0x3FF
DIS_CAN_MESSAGE = 0x41

getVoltagesCommand = [3]
getTemperaturesCommand = [4]
startBalancingCommand = [5]
stopBalancingCommand = [6]
hvSimulationCommand = np.array([0, 0, 64, 0])
fanControlCommand = 7
numberOfCells = 140
numberOfTempSensors = 80
defaultValues = {'cellVoltages': 0, 'cellTemperatures': 999, 'akkuVoltage': 000, 'stateOfCharge':  999, 'maxVoltage': 0,
                 'minVoltage': 0, 'maxTemperature': 999, 'minTemperature': 999}

states = {'0': 'IDLE', '1': 'Precharge', '2':'Drive', '4': 'Precharge Fail', '5': 'Data Error', '6':'Relais Stuck'}
Bus_Status_Ok = True

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
