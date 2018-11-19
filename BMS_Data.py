''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''

import logging
import traceback

import numpy as np

import BMS_ControlParameter as p

########################################## Data ################################################################

""" variable declaration begins"""
rawGenerals = []
rawVoltages = []
rawTemperatures = []
rawStrom = [[88, 88, 88, 88]]

transmissionError = 'None'
HV_Button = 'Off'


errors = {'currentError': True , 'VoltageErrors': np.array([True] * p.numberOfCells),
          'TemperatureErrors': np.array([True] * (p.numberOfCells-60)) }



""" variable declaration ends"""

""" mathods declaration begins"""


def getdata(cell, type):  # methode that enables user to get the data from this class
    data = {'soc': getSOC(), 'cs': getState(),'bc': getCurrent(), 'bv': getAkkuVoltage(),
            'bt': getAkkuTemperature(),'te': getTransmissionError(), 'mxV': getMaxVoltage(),
            'mnV': getMinVoltage(), 'mxT': getMaxTemperature(),"hvb": getHV(),'mnT': getMinTemperature(), 'sc': getSC(),
            'v': get_cell_voltage(cell), 't': get_cell_temperature(cell)}

    return data[type]


def get_position(cell): #returns the position of the cell data inside the 4 value msg
    if cell in range(1, p.numberOfCells+1, 1):

        a = cell % 4
        return a - 1
    else:
        print('item not in the list')
        return 1


def get_ID(cell, first_id): #returns the ID of the msg having the data for a given cell
    #if cell in range(1, 141, 1):
    id = first_id + ((cell - 1) // 4)
    return hex(id)



def get_cell_voltage(cell): #extracts the voltages of a specific cell from rawVoltages
    idleVoltage = p.defaultValues['cellVoltages'] #ERRORS
    global transmissionError
    try:
        if len(rawVoltages) != 0:
            transmissionError = "None"
            for i in range(len(rawVoltages) - 1, 0, -1):

                if rawVoltages[i]['ID'] == get_ID(cell, p.voltageIDs[0]):
                    idleVoltage = (rawVoltages[i]['data'][get_position(cell) * 2] << 8) + \
                                  rawVoltages[i]['data'][get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break

        return idleVoltage
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def get_cell_temperature(cell):
    idleTemperature = p.defaultValues['cellTemperatures'] #ERROR
    global transmissionError
    try:
        if len(rawTemperatures) != 0 :
            transmissionError = "None"
            for i in range(len(rawTemperatures) - 1, 0, -1):
                if rawTemperatures[i]['ID'] == get_ID(cell, p.temperatureIDs[0]):
                    idleTemperature = (rawTemperatures[i]['data'][get_position(cell) * 2] << 8) \
                        + rawTemperatures[i]['data'][get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break


        return idleTemperature
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getCurrent():
    i = len(rawStrom)-1
    a = rawStrom[i]
    global transmissionError

    current = a[0]* 2**24  + a[1] * 2**16 + a[2]* 2**8+ a[3]
    if current != 0:
        transmissionError = "None"
        if current > (2**31):
            return ((2**32)-current) * (-1)
        else:
            return current

    else:

        transmissionError = 'Transmition Error'
        return 8888888


def getState():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            transmissionError = "None"
            a = (rawGenerals[i-1][0] & 0b11100000) >> 5
            return p.states[str(a)]
        else:
            return "no state"

    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getSC():
    global transmissionError
    try:
        i =  len(rawGenerals)
        if i != 0:
            transmissionError = "None"
            a = (rawGenerals[i-1][0] & 0b10000) >> 4
            dic = {'0': 'off' , '1': 'on'}
            return dic[str(a)]
        else:
            return "no data"
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getAkkuVoltage():
    global transmissionError
    try:
        i= len(rawGenerals)
        if i != 0:
            akkuVoltage = (((rawGenerals[i-1][0] & 0b1111) << 8 ) + rawGenerals[i-1][1])/5
            transmissionError = "None"
            return akkuVoltage
        else:
            return p.defaultValues['akkuVoltage']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getAkkuTemperature():
    return ''


def getSOC():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            soc = (rawGenerals[i-1][2])/2.55
            transmissionError = "None"
            return format(soc, '.1f')

        else:
            return p.defaultValues['stateOfCharge']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getMaxVoltage():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            MxVoltage = ((rawGenerals[i-1][3] << 4) + ((rawGenerals[i-1][4]& 0b11110000)>>4)+1000)/1000
            transmissionError = 'None'
            return MxVoltage

        else:
            return p.defaultValues['maxVoltage']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getMinVoltage():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            transmissionError = "None"
            MinVoltage = ((((rawGenerals[i-1][4] & 0b1111) << 8) + rawGenerals[i-1][5])+1000)/1000

            return MinVoltage
        else:
            return p.defaultValues['minVoltage']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getMaxTemperature():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            transmissionError = "None"
            MxTemp = rawGenerals[i-1][6]*0.5
            return MxTemp
        else:
            return p.defaultValues['maxTemperature']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())

def getMinTemperature():
    global transmissionError
    try:
        i = len(rawGenerals)
        if i != 0:
            transmissionError = "None"
            MinTemp = rawGenerals[i - 1][7]*0.5
            return MinTemp
        else:
            return p.defaultValues['minTemperature']
    except Exception as e:

        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getTransmissionError():
    global transmissionError
    return transmissionError


def setErrors(num,type): #methode that checks the existence of errors and fills the error dictionnary accordingly
    try:
        if type == 'v':
            for i in range(num):
                #print('cellVoltages= ', self.cellVoltages)
                if get_cell_voltage(i)>4000 or get_cell_voltage(i)<2000:
                    errors['VoltageErrors'][i] = False

                else:
                    errors['VoltageErrors'][i] = True

        elif type == 't':
            for i in range(num):

                if get_cell_temperature(i) > 600 or get_cell_temperature(i) < 250:

                    errors['TemperatureErrors'][i] = False
                else:
                    errors['TemperatureErrors'][i] = True

    except Exception as e:
        global transmissionError
        transmissionError = 'Transmission Error'
        logging.error(traceback.format_exc())


def getErrors(cell, type): #methode that returns the errors
    errors_dic = {'v': errors['VoltageErrors'], 't': errors['TemperatureErrors']}
    return errors_dic[type][cell]

def getHV():
    global HV_Button
    return HV_Button

def setHv(state):
    global HV_Button
    hv_dic = {0: 'off', 1: 'on'}
    HV_Button = hv_dic[state]


""" mathods declaration ends"""