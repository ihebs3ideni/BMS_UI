''' Author: Saidani Iheb
    Season: 2017-2018
    Project: Nanni's Little Helper
    '''

import sys
import os
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from PyQt5.QtCore import QTimer, Qt
import threading
import csv
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QFileDialog, QRadioButton, QHBoxLayout, QVBoxLayout,
                             QPushButton, QWidget, QTableWidget, QTabWidget, QCheckBox, QSlider, QTableWidgetItem,
                             QGridLayout,QAbstractItemView, QLabel, QLineEdit,QLCDNumber )
from random import randint
import traceback
import logging
from can.interfaces.pcan import PcanBus
from can.bus import BusABC
import can
import atexit
import numpy as np

#######################################################################################################################

#global variable to control whether the GUI is connected
Connected = False



########################################### communication #############################################################

class BMS_Communications(BusABC):
    def __init__(self):
        super().__init__()
        self.cont=0
        self.cont1 = 0
        self.startCommunication = False
        self.Voltages = []
        self.Temperatures = []
        self.temp_max = 0
        self.temp_min = 0
        self.voltage_max = 0
        self.voltage_min = 0
        self.currentState = ''
        self.voltageErrors = []
        self.temperatureErrors = []
        self.soc = 0
        self.rawStrom = [[88,88,88,88]]
        self.stromID = 273
        self.batteryVoltage = 0
        self.batteryTemperature = 0
        self.generals = []
        self.generalsID = 257
        self.v_id = np.arange(1281,1316,1)
        self.t_id = np.arange(1329,1350,1)
        self.check = False
        self.msg = can.Message(arbitration_id=0x41, data=[0, 0, 0, 0], extended_id=False)
        #print(self.Voltages)
        #self.bus = PcanBus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
    def comm(self,bus):

        print('starting communications')
        for msg in bus:
            if self.check:

                '''thread0 =threading.Thread(target= bus.send(self.msg))
                thread0.setDaemon(True)
                thread0.start()'''
                threading.Thread(target= self.sending(bus,[0,0,0,0], 0x41)).start()
                threading.Thread(target= self.sending(bus,[3],id=0x3ff)).start()
                #print(msg)
                if msg.arbitration_id in self.v_id:
                    dic = {'ID': 0, 'data': []}
                    dic['ID'] = hex(msg.arbitration_id)
                    for i in range(len(msg.data)):
                        dic['data'].append(msg.data[i])
                    self.Voltages.append(dic)
                    if len(self.Voltages) > 500:
                        del (self.Voltages[0:300])
                if msg.arbitration_id in self.t_id:
                    dic1 = {'ID': 0, 'data': []}
                    dic1['ID'] = hex(msg.arbitration_id)
                    for j in range(len(msg.data)):
                        dic1['data'].append(msg.data[j])
                    self.Temperatures.append(dic1)
                    if len(self.Temperatures) > 500:
                        del (self.Temperatures[0:300])
                if msg.arbitration_id == self.generalsID:

                    list1 = []
                    for i in range(len(msg.data)):
                        list1.append(msg.data[i])
                    self.generals.append(list1)

                    if len(self.generals) > 300:
                        del(self.generals[:200])
                if msg.arbitration_id == 0x111:
                    list1 = [88,88,88,88]
                    for i in range(4):
                       list1[i]= msg.data[i+2]
                    self.rawStrom.append(list1)
                    #print(list1)

            else:

                break

    def sending(self,bus, d, id):
        msg = can.Message(arbitration_id=id, data=d, extended_id=False)
        bus.send(msg)

    def terminate(self):

        self.check = False
        self.cont = 0
        self.cont1 +=1
        if self.cont1 == 2:
            print(self.Voltages)
        elif self.cont1 == 3:
            print(self.Temperatures)

    def close(self,bus):
        bus.shutdown()

    def starting(self,bus):
        try:
            self.cont = self.cont + 1

            if self.cont == 1:

                self.cont1 = 0

                self.check = True
                t = threading.Thread(target=lambda: self.comm(bus))
                t.setDaemon(True)
                t.start()
            else:
                pass
        except can.CanError:
            print('error Can')
            bus.reset()


    def initialize_bus(self):

        bus = PcanBus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
        print(bus.status())
        return bus

    def balancing(self,bus):

        self.sending(bus,[5],id=0x3ff)
        print('balancing')

    def stop_balancing(self,bus):
        self.sending(bus, [6],id=0x3ff)
        print('balancing stopped')

    def HV_simulate(self,bus):
        self.sending(bus, d=[0,0,64,0],id=0x41)

        print('HV Clicked')

    '''def reku_simulate(self,bus):
        self.sending(bus, d=[0,0,32],id=0x41)

        print('Reku Clicked')

    def start_simulate(self,bus):
        self.sending(bus, d=[0,0,128],id=0x41)

        print('Start Clicked')

    def lr1_simulate(self, bus):
        self.sending(bus, d=[0, 0, 16], id=0x41)

        print('LR1 Clicked')

    def lr2_simulate(self, bus):
        self.sending(bus, d=[0, 0, 8], id=0x41)

        print('LR2 Clicked')

    def lr3_simulate(self, bus):
        self.sending(bus, d=[0, 0, 4], id=0x41)

        print('LR3 Clicked')

    def lr4_simulate(self, bus):
        self.sending(bus, d=[0, 0, 2], id=0x41)

        print('LR4 Clicked')

    def lr5_simulate(self, bus):
        self.sending(bus, d=[0, 0, 1], id=0x41)

        print('LR5 Clicked')

    def lr6_simulate(self, bus):
        self.sending(bus, d=[0, 0, 0,128], id=0x41)

        print('LR6 Clicked')'''

    def getCurrent(self):
        i = len(self.rawStrom)-1
        a = self.rawStrom[i]

        current = a[0]* 2**24  + a[1] * 2**16 + a[2]* 2**8+ a[3]
        if current > (2**31):
            return ((2**32)-current) * (-1)
        else:
            return current



    def get_position(self,cell):
        if cell in range(1, 141, 1):

            a = cell% 4
            return a-1
        else:
            print('item not in the list')
            return 1

    def get_id(self, cell, first_id):
        #if cell in range(1, 141, 1):
        id = first_id + ((cell - 1) // 4)
        return hex(id)

    def get_cell_voltage(self,cell):
        a = 3808 #ERRORS
        try:
            for i in range(len(self.Voltages) - 1, 0, -1):

                if self.Voltages[i]['ID'] == self.get_id(cell, self.v_id[0]):
                    a = (self.Voltages[i]['data'][self.get_position(cell) * 2] << 8) + self.Voltages[i]['data'][self.get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break

            return a
        except Exception as e:
            logging.error(traceback.format_exc())

    def get_cell_temperature(self,cell):
        a = 400 #ERROR
        try:
            for i in range(len(self.Temperatures) - 1, 0, -1):
                if self.Temperatures[i]['ID'] == self.get_id(cell, self.t_id[0]):
                    a = (self.Temperatures[i]['data'][self.get_position(cell) * 2] << 8) \
                        + self.Temperatures[i]['data'][self.get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break

            return a
        except Exception as e:
            logging.error(traceback.format_exc())



    def raw_data(self, type):
        list = np.array([])
        if type =='v':
            for i in range (len(self.Voltages)):
                np.append(list,self.Voltages[len(self.Voltages)-1]['data'][i])
            return list
        elif type == 't':
            for i in range (len(self.Temperatures)):
                np.append(list,self.Temperatures[len(self.Temperatures)-1]['data'][i])
            return list
        elif type == 'g':
            for i in range (len(self.generals)):
                np.append(list,self.generals[len(self.generals)-1][i])
            return list



    def getState(self):
        try:
            i = len(self.generals)
            if i != 0:
                a = (self.generals[i-1][0] & 0b11100000) >> 5
                dic = {'0': 'IDLE', '1': 'Precharge', '2':'Drive', '4': 'Precharge Fail', '5': 'Data Error', '6':'Relais Stuck'}

                return dic[str(a)]
        except Exception as e:
            logging.error(traceback.format_exc())

    def getSC(self):
        try:
            i =  len(self.generals)
            if i != 0:
                a = (self.generals[i-1][0] & 0b10000) >> 4
                dic = {'0': 'off' , '1': 'on'}
                return dic[str(a)]
        except Exception as e:
            logging.error(traceback.format_exc())

    def getAkkuVoltage(self):
        try:
            i= len(self.generals)
            if i != 0:
                akkuVoltage = (((self.generals[i-1][0] & 0b1111) << 8 ) + self.generals[i-1][1])/5
                return akkuVoltage
        except Exception as e:
            logging.error(traceback.format_exc())

    def getAkkuTemperature(self):
        return 0

    def getSOC(self):
        try:
            i = len(self.generals)
            if i != 0:
                soc = (self.generals[i-1][2])/2.55
                return format(soc, '.1f')
        except Exception as e:
            logging.error(traceback.format_exc())

    def getMaxVoltage(self):
        try:
            i = len(self.generals)
            if i != 0:
                MxVoltage = ((self.generals[i-1][3] << 4) + ((self.generals[i-1][4]& 0b11110000)>>4)+1000)/1000
                return MxVoltage
        except Exception as e:
            logging.error(traceback.format_exc())

    def getMinVoltage(self):
        try:
            i = len(self.generals)
            if i != 0:
                MinVoltage = ((((self.generals[i-1][4] & 0b1111) << 8) + self.generals[i-1][5])+1000)/1000

                return MinVoltage
        except Exception as e:
            logging.error(traceback.format_exc())
    def getMaxTemperature(self):
        try:
            i = len(self.generals)
            if i != 0:
                MxTemp = self.generals[i-1][6]*0.5
                return MxTemp
        except Exception as e:
            logging.error(traceback.format_exc())

    def getMinTemperature(self):
        try:
            i = len(self.generals)
            if i != 0:
                MinTemp = self.generals[i - 1][7]*0.5
                return MinTemp
        except Exception as e:
            logging.error(traceback.format_exc())

    def control_fan(self,bus,d,ID):
        self.sending(bus,d,ID)

    ################################################################################################################



    ########################################## Data ################################################################



class Data():
    def __init__(self, numberOfCells,bus,com):
        #data for the celltable tab
        self.bus= bus
        self.com = com
        self.cellVoltages = np.array([0]*140)
        self.cellTemperatures = np.array([0]*80)
        '''if use == 'table':
            #self.com = BMS_Communications()

            self.fillData(numberOfCells,'v')
            self.fillData(numberOfCells, 't')'''

    #data for the general tabs

        self.stateOfCharge = 0
        self.currentState = ''
        self.batteryCurrent = 0
        self.batterVoltage = 0
        self.batteryTemperature = 0
        self.HVButton = 'off'
        #self.shutDownCircuitVoltage = 0
        #self.preChargeStartTime = 0
        #self.failTime = 0
        #self.upTime = 0
        self.shutdownCircuit = ''
        self.transmitionError = 'None'
        #self.airLSAux = ''
        #self.airHSAux = ''
        #self.HVButton = ''
        #self.startLoad = ''

        self.maxTemperature = 0
        self.minTemperature = 0
        self.maxVoltage = 0
        self.minVoltage = 0
        '''if use =='generals':
            #self.com = BMS_Communications()

            self.fillData(numberOfCells, 'soc')
            self.fillData(numberOfCells, 'cs')
            self.fillData(numberOfCells, 'bc')
            self.fillData(numberOfCells, 'bv')
            self.fillData(numberOfCells, 'bt')
            self.fillData(numberOfCells, 'dcv')
            self.fillData(numberOfCells, 'te')
            self.fillData(numberOfCells, 'mxV')
            self.fillData(numberOfCells, 'mnV')
            self.fillData(numberOfCells, 'mxT')
            self.fillData(numberOfCells, 'mnT')
            self.fillData(numberOfCells, 'scv')
            self.fillData(numberOfCells, 'pst')
            self.fillData(numberOfCells, 'ft')
            self.fillData(numberOfCells, 'ut')

            self.fillData(numberOfCells, 'airLsAux')
            self.fillData(numberOfCells, 'airHsAux')
            self.fillData(numberOfCells, 'hvb')
            self.fillData(numberOfCells, 'sl')'''

    # data for error tab

        self.errors = {'currentError': True , 'VoltageErrors': np.array([True] * numberOfCells) , 'TemperatureErrors': np.array([True] * (numberOfCells-60)) }

        '''if use == 'errors':
            #self.com = BMS_Communications()
            self.checkErrors(140,'c')
            self.checkErrors(numberOfCells,'v')
            self.checkErrors(numberOfCells-60,'t')
            #print(self.errors['VoltageErrors'][5])'''
    #data for Fan Control

        self.fanInstructions = {}
        for i in range(101):
            self.fanInstructions.update({i : hex(randint(1,100))})



    def checkErrors(self,num,type,object): #methode that checks the existence of errors and fills the error dictionnary accordingly
        try:

            if type =='c':
                a = randint(0, 20)

                if a%2 == 0:

                    self.errors['currentError'] = False

                else: pass
            elif type == 'v':
                for i in range(num):
                    #print('cellVoltages= ', self.cellVoltages)
                    if object.cellVoltages[i]>4000 or object.cellVoltages[i]<2000:
                        self.errors['VoltageErrors'][i] = False

                    else:
                        self.errors['VoltageErrors'][i] = True



            elif type == 't':
                for i in range(len(self.cellTemperatures)):

                    if object.cellTemperatures[i]>600 or object.cellTemperatures[i]<250:

                        self.errors['TemperatureErrors'][i] = False
                    else: self.errors['TemperatureErrors'][i] = True



        except Exception as e:
            logging.error(traceback.format_exc())

    #a = BMS_Communications()

    def getErrors(self,cell, type): #methode that returns the errors
        errors = { 'v' :self.errors['VoltageErrors'], 't': self.errors['TemperatureErrors'] }
        if type == 'c':
            return self.errors['currentError']
        else:
            return errors[type][cell]









    def fillData(self, num, type): #methode that interprets the raw data and devide it into categories
        try:
            if type=='v' or type == 'V':

                for i in range(140):
                    a = self.com.get_cell_voltage(i+1)

                    #print('a1= ', a)
                    self.cellVoltages[i]=int(a)

            elif type =='t' or type == 'T':
                if self.com.get_cell_voltage(1) is not None:
                    for i in range(80):
                        a= self.com.get_cell_temperature(i+1)
                        self.cellTemperatures[i]=int(a)
                        self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
            elif type == 'soc':
                if self.com.getSOC() is not None:
                    self.stateOfCharge = self.com.getSOC()
                    self.transmitionError = 'None'
                else:
                    self.stateOfCharge = 9999
                    self.transmitionError = 'Error'
            elif type == 'cs':
                if self.com.getState() is not None:
                    self.currentState = self.com.getState()
                    self.transmitionError = 'None'
                else:
                    self.currentState = 'Transmition Error'
                    self.transmitionError = 'Error'
            elif type == 'bc':
                if self.com.getCurrent() is not None:
                    self.batteryCurrent = self.com.getCurrent()
                    self.transmitionError = 'None'
                else:
                    self.batteryCurrent = 8888888
                    self.transmitionError = 'Transmition Error'
            elif type == 'bv':
                if self.com.getAkkuVoltage() is not None:
                    self.batterVoltage = self.com.getAkkuVoltage()
                    self.transmitionError = 'None'
                else:
                    self.batterVoltage = -9999
                    self.transmitionError = 'Error'
            elif type == 'bt':
                if self.com.getAkkuTemperature() is not None:
                    self.batteryTemperature = self.com.getAkkuTemperature()
                    self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
                    self.batteryTemperature = 99999


            elif type == 'hvb':

                self.HVButton = 'off'

            elif type =='mxT':
                if self.com.getMaxTemperature() is not None:
                    self.maxTemperature = self.com.getMaxTemperature()
                    self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
                    self.maxTemperature = 9999999
            elif type == 'mnT':
                if self.com.getMinTemperature() is not None:
                    self.minTemperature = self.com.getMinTemperature()
                    self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
                    self.minTemperature = -999999
            elif type == 'mxV':
                if self.com.getMaxVoltage() is not None:
                    self.maxVoltage = self.com.getMaxVoltage()
                    self.transmitionError = 'None'

                else:
                    self.transmitionError = 'Error'
                    self.maxVoltage = 888888

            elif type == 'mnV':
                if self.com.getMinVoltage() is not None:
                    self.minVoltage =  self.com.getMinVoltage()
                    self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
                    self.minVoltage = -8888888
            elif type == 'sc':
                if self.com.getSC() is not None:
                    self.shutdownCircuit = self.com.getSC()
                    self.transmitionError = 'None'
                else:
                    self.transmitionError = 'Error'
                    self.shutdownCircuit = 'No Data'
            '''elif type == 'scv':
                self.shutDownCircuitVoltage = randint(0,100)
            elif type == 'pst':
                self.preChargeStartTime = randint(0,1000)
            elif type == 'ft':
                self.failTime = randint(0,500)
            elif type == 'ut':
                self.upTime = randint(0,200)

            elif type == 'airLsAux':
                self.airLSAux = 'off'
            elif type == 'airHsAux':
                self.airHSAux = 'off'
            elif type == 'hvb':
                self.HVButton = 'off'
            elif type == 'sl':
                self.startLoad = 'off'
            elif type == 'te':
                self.transmitionError = 'None' '''

        except Exception as e:
            logging.error(traceback.format_exc())

    def getdata(self, cell, type): #methode that enables user to get the data from this class
        data = {'soc':self.stateOfCharge, 'cs': self.currentState,
                 'bc': self.batteryCurrent, 'bv': self.batterVoltage, 'bt': self.batteryTemperature, 'hvb': self.HVButton,
               'te': self.transmitionError, 'mxV': self.maxVoltage, 'mnV': self.minVoltage, 'mxT': self.maxTemperature,
                 'mnT': self.minTemperature, 'sc':self.shutdownCircuit}


        if type =='v' or type == 'V':

            return self.cellVoltages[cell]
        elif type == 't' or type =='T':
            return self.cellTemperatures[cell]
        else:
            return data[type]




        '''elif type == 'scv':
            return self.shutDownCircuitVoltage
        elif type == 'pst':
            return self.preChargeStartTime
        elif type == 'ft':
            return self.failTime
        elif type == 'ut':
            return self.upTime
        elif type == 'airLsAux':
            return self.airLSAux
        elif type == 'airHsAux':
            return self.airHSAux
        elif type == 'hvb':
            return self.HVButton
        elif type == 'sl':
            return self.startLoad'''


    def getFanRotationSpeed(self,x):
        print(self.fanInstructions)
        return self.fanInstructions[x]



####################################################################################################################






  ##################################### Graphical Design #####################################################


'''class DriverInformations(QWidget):
    def __init__(self,bus, data,bms_com):
        super().__init__()
        self.com= bms_com
        self.bus = bus
        self.data = data
        self.HVButton = QPushButton('HV Button')
        self.respond1 = QLabel()
        self.i1 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')

        self.startButton = QPushButton('Start Button')
        self.respond2 = QLabel()
        self.i2 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.rekuButton = QPushButton('Reku Button')
        self.respond3 = QLabel()
        self.i3 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr1 = QPushButton('LR1 Button')
        self.respond4 = QLabel()
        self.i4 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr2 = QPushButton('LR2 Button')
        self.respond5 = QLabel()
        self.i5 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr3 = QPushButton('LR3 Button')
        self.respond6 = QLabel()
        self.i6 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr4 = QPushButton('LR4 Button')
        self.respond7 = QLabel()
        self.i7 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr5 = QPushButton('LR5 Button')
        self.respond8 = QLabel()
        self.i8 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')
        self.lr6 = QPushButton('LR6 Button')
        self.respond9 = QLabel()
        self.i9 = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')




        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.HVButton)
        h_box.addWidget(self.respond1)
        h_box.addStretch()
        h_box.addWidget(self.startButton)
        h_box.addWidget(self.respond2)
        h_box.addStretch()
        h_box.addWidget(self.rekuButton)
        h_box.addWidget(self.respond3)
        h_box.addStretch()

        h_box1 = QHBoxLayout()
        h_box1.addStretch()
        h_box1.addWidget(self.lr1)
        h_box1.addWidget(self.respond4)
        h_box1.addStretch()
        h_box1.addWidget(self.lr2)
        h_box1.addWidget(self.respond5)
        h_box1.addStretch()
        h_box1.addWidget(self.lr3)
        h_box1.addWidget(self.respond6)
        h_box1.addStretch()

        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.lr4)
        h_box2.addWidget(self.respond7)
        h_box2.addStretch()
        h_box2.addWidget(self.lr5)
        h_box2.addWidget(self.respond8)
        h_box2.addStretch()
        h_box2.addWidget(self.lr6)
        h_box2.addWidget(self.respond9)
        h_box2.addStretch()



        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(h_box)
        v_box.addStretch()
        v_box.addLayout(h_box1)
        v_box.addStretch()
        v_box.addLayout(h_box2)
        v_box.addStretch()



        self.setLayout(v_box)


    def HV_clicked(self):

        self.com.HV_simulate(self.bus)
        self.respond1.setPixmap(self.i1.scaled(50, 50))

    def start_clicked(self):

        self.com.start_simulate(self.bus)
        self.respond2.setPixmap(self.i2.scaled(50, 50))

    def Reku_clicked(self):

        self.com.reku_simulate(self.bus)
        self.respond3.setPixmap(self.i3.scaled(50, 50))

    def lr1_clicked(self):
        self.com.lr1_simulate(self.bus)
        self.respond4.setPixmap(self.i4.scaled(50, 50))

    def lr2_clicked(self):
        self.com.lr2_simulate(self.bus)
        self.respond5.setPixmap(self.i5.scaled(50, 50))

    def lr3_clicked(self):
        self.com.lr3_simulate(self.bus)
        self.respond6.setPixmap(self.i6.scaled(50, 50))

    def lr4_clicked(self):
        self.com.lr4_simulate(self.bus)
        self.respond7.setPixmap(self.i7.scaled(50, 50))

    def lr5_clicked(self):
        self.com.lr5_simulate(self.bus)
        self.respond8.setPixmap(self.i8.scaled(50, 50))

    def lr6_clicked(self):
        self.com.lr6_simulate(self.bus)
        self.respond9.setPixmap(self.i9.scaled(50, 50))'''





####################################################################################################################




####################################################################################################################


class GeneralsTab(QWidget):
    def __init__(self,bus, data,bms_com):
        super().__init__()
        self.com1 = bms_com
        self.bus = bus
        self.data = data

        self.warning_label = QLabel()
        warning_layout = QHBoxLayout()
        warning_layout.addStretch()
        warning_layout.addWidget(self.warning_label)
        warning_layout.addStretch()



        #set state of charge layout
        self.stateofcharge = QLabel('State of Charge:')
        self.percentage= QLabel('%')
        self.line = QLineEdit()
        #self.fillBlanks('soc', self.line)
        self.line.setFixedWidth(40)
        self.line.setReadOnly(True)


        self.logo = QLabel('')
        self.i = QPixmap('C:/Users/iheb/BMS_UI/icons/State of charge.ico')
        self.logo.setPixmap(self.i.scaled(30,30))

        h_box0 = QHBoxLayout()
        h_box0.addSpacing(30)
        h_box0.addWidget(self.logo)
        h_box0.addWidget(self.stateofcharge)
        h_box0.addWidget(self.line)
        h_box0.addWidget(self.percentage)
        h_box0.addStretch()



        # set GeneralVolatge Layout

        self.voltage = QLabel("Battery Voltage")
        self.line2 = QLineEdit()

        self.line2.setFixedWidth(50)
        self.line2.setReadOnly(True)
        self.v = QLabel('V')

        self.logo1 = QLabel('')
        self.i1 = QPixmap('C:/Users/iheb/BMS_UI/icons/voltage.ico')
        self.logo1.setPixmap(self.i1.scaled(30, 30))

        h_box2 = QHBoxLayout()
        h_box2.addSpacing(30)
        h_box2.addWidget(self.logo1)
        h_box2.addWidget(self.voltage)
        h_box2.addWidget(self.line2)
        h_box2.addWidget(self.v)
        h_box2.addStretch()

        # set SC Layout

        self.sc = QLabel("Shutdown Circuit")
        self.line3 = QLineEdit()
        self.line3.setFixedWidth(50)
        self.line3.setReadOnly(True)


        self.logo2 = QLabel('')
        self.i2 = QPixmap('C:/Users/iheb/BMS_UI/icons/sc.png')
        self.logo2.setPixmap(self.i2.scaled(30, 30))

        h_box3 = QHBoxLayout()
        h_box3.addSpacing(30)
        h_box3.addWidget(self.logo2)
        h_box3.addWidget(self.sc)
        h_box3.addWidget(self.line3)

        h_box3.addStretch()

        #set Current (strom) layout
        self.current = QLabel("Battery Current (Strom)")
        self.line4 = QLineEdit()
        self.line4.setFixedWidth(50)
        self.line4.setReadOnly(True)
        self.c = QLabel('mA')

        self.logo3 = QLabel('')
        self.i3 = QPixmap('C:/Users/iheb/BMS_UI/icons/Strom.ico')
        self.logo3.setPixmap(self.i3.scaled(30, 30))

        h_box4 = QHBoxLayout()
        h_box4.addSpacing(30)
        h_box4.addWidget(self.logo3)
        h_box4.addWidget(self.current)
        h_box4.addWidget(self.line4)
        h_box4.addWidget(self.c)
        h_box4.addStretch()


        # first vertical layout that contains 5 horizental ones
        v_box1 = QVBoxLayout()
        v_box1.addSpacing(30)
        v_box1.addLayout(h_box0)

        v_box1.addStretch()

        v_box1.addLayout(h_box4)
        v_box1.addStretch()
        v_box1.addLayout(h_box2)

        v_box1.addStretch()
        v_box1.addLayout(h_box3)

        # max voltage layout



        self.vm = QLabel('Voltage Max:')
        self.line5 = QLineEdit()
        self.line5.setFixedWidth(50)
        self.line5.setReadOnly(True)
        self.logo8 = QLabel('')
        self.i8 = QPixmap('C:/Users/iheb/BMS_UI/icons/maxVoltage.png')
        self.logo8.setPixmap(self.i8.scaled(30,30))
        self.v1 = QLabel('V')

        h_box5 = QHBoxLayout()
        h_box5.addSpacing(30)
        h_box5.addWidget(self.logo8)
        h_box5.addWidget(self.vm)
        h_box5.addWidget(self.line5)
        h_box5.addWidget(self.v1)
        h_box5.addStretch()






        # min Voltage Layout

        self.prStartTime = QLabel('Voltage Min:')
        self.line6 = QLineEdit()

        self.line6.setFixedWidth(50)
        self.line6.setReadOnly(True)
        self.logo4 = QLabel('')
        self.i4 = QPixmap('C:/Users/iheb/BMS_UI/icons/minVoltage.png')
        self.logo4.setPixmap(self.i4.scaled(30, 30))
        self.s = QLabel('mV')
        h_box6 = QHBoxLayout()
        h_box6.addSpacing(30)
        h_box6.addWidget(self.logo4)
        h_box6.addWidget(self.prStartTime)
        h_box6.addWidget(self.line6)
        h_box6.addWidget(self.s)
        h_box6.addStretch()

        # max temperature Layout

        self.failTime = QLabel('Temperature Max:')
        self.line7 = QLineEdit()
        self.line7.setFixedWidth(50)
        self.line7.setReadOnly(True)
        self.logo5 = QLabel('')
        self.i5 = QPixmap('C:/Users/iheb/BMS_UI/icons/maxTemperature.png')
        self.logo5.setPixmap(self.i5.scaled(30, 30))
        self.s1 = QLabel('C°')
        h_box7 = QHBoxLayout()
        h_box7.addSpacing(30)
        h_box7.addWidget(self.logo5)
        h_box7.addWidget(self.failTime)
        h_box7.addWidget(self.line7)
        h_box7.addWidget(self.s1)
        h_box7.addStretch()

        # min Temperature Layout

        self.upTime = QLabel('Temperature Min:')
        self.line8 = QLineEdit()
        self.line8.setFixedWidth(50)
        self.line8.setReadOnly(True)
        self.logo6 = QLabel('')
        self.i6 = QPixmap('C:/Users/iheb/BMS_UI/icons/minTemperature.png')
        self.logo6.setPixmap(self.i6.scaled(30, 30))
        self.s2 = QLabel('C°')
        h_box8 = QHBoxLayout()
        h_box8.addSpacing(30)
        h_box8.addWidget(self.logo6)
        h_box8.addWidget(self.upTime)
        h_box8.addWidget(self.line8)
        h_box8.addWidget(self.s2)
        h_box8.addStretch()



        # second vertical layout that contains 5 horizental ones
        v_box2 = QVBoxLayout()
        v_box2.addSpacing(30)
        v_box2.addLayout(h_box5)
        v_box2.addStretch()
        v_box2.addLayout(h_box6)
        v_box2.addStretch()
        v_box2.addLayout(h_box7)
        v_box2.addStretch()
        v_box2.addLayout(h_box8)


        #Transmition error Layout

        self.txError = QLabel ('Transmition Error: ')
        self.line10 = QLineEdit()
        self.line10.setFixedWidth(50)
        self.line10.setReadOnly(True)

        h_box10 = QHBoxLayout()
        h_box10.addSpacing(30)
        h_box10.addWidget(self.txError)
        h_box10.addWidget(self.line10)
        h_box10.addStretch()

        # set current State layout

        self.state = QLabel("Current State: ")
        self.line1 = QLineEdit()
        self.line1.setFixedWidth(120)
        self.line1.setReadOnly(True)
        h_box1 = QHBoxLayout()
        h_box1.addSpacing(30)
        h_box1.addWidget(self.state)
        h_box1.addWidget(self.line1)
        h_box1.addStretch()

        # dcLink Voltage Layout

        self.HV_state = QLabel('HV Button:')
        self.line9 = QLineEdit('off')

        self.line9.setFixedWidth(30)
        self.line9.setReadOnly(True)
        self.v2 = QLabel('V')
        h_box9 = QHBoxLayout()
        h_box9.addSpacing(30)
        h_box9.addWidget(self.HV_state)
        h_box9.addWidget(self.line9)
        #h_box9.addWidget(self.v2)
        h_box9.addStretch()


        #start balancing command
        self.startBalancing = QPushButton('Start Balancing')
        self.logo7 = QLabel('')
        self.i7 = QPixmap('C:/Users/iheb/BMS_UI/icons/balancing.png')
        self.logo7.setPixmap(self.i7.scaled(30,30))
        self.respond= QLabel('   ')


        #HV_BUtton_simuate
        self.HVButton = QPushButton('HV Button')
        self.logo9 = QLabel('')
        self.i9 = QPixmap('C:/Users/iheb/BMS_UI/icons/HV.png')
        self.logo9.setPixmap(self.i9.scaled(30, 30))
        self.respond1 = QLabel()
        self.i_hv = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')

        h_box15 = QHBoxLayout()
        h_box15.addSpacing(30)
        h_box15.addWidget(self.logo7)
        h_box15.addSpacing(10)
        h_box15.addWidget(self.startBalancing)
        h_box15.addStretch()
        h_box15.addWidget(self.respond)
        h_box15.addStretch()

        h_box16 = QHBoxLayout()
        h_box16.addSpacing(30)
        h_box16.addWidget(self.logo9)
        h_box16.addSpacing(10)
        h_box16.addWidget(self.HVButton)
        h_box16.addStretch()
        h_box16.addWidget(self.respond1)
        h_box16.addStretch()

        v_box4 = QVBoxLayout()
        v_box4.addLayout(h_box15)
        v_box4.addStretch()
        v_box4.addLayout(h_box16)
        v_box4.addStretch()

        # AirLsAux  Layout

        '''self.airls = QLabel('AirLSAux: ')
        self.line11 = QLineEdit()
        self.line11.setFixedWidth(30)
        self.line11.setReadOnly(True)

        h_box11 = QHBoxLayout()
        h_box11.addSpacing(30)
        h_box11.addWidget(self.airls)
        h_box11.addWidget(self.line11)
        h_box11.addStretch()

        # AirHsAux  Layout

        self.airhs = QLabel('AirHSAux: ')
        self.line12 = QLineEdit()
        self.line12.setFixedWidth(30)
        self.line12.setReadOnly(True)

        h_box12 = QHBoxLayout()
        h_box12.addSpacing(30)
        h_box12.addWidget(self.airhs)
        h_box12.addWidget(self.line12)
        h_box12.addStretch()

        # HV Button  Layout

        self.hvButton = QLabel('HV Button: ')
        self.line13 = QLineEdit()
        self.line13.setFixedWidth(30)
        self.line13.setReadOnly(True)


        h_box13 = QHBoxLayout()
        h_box13.addSpacing(30)
        h_box13.addWidget(self.hvButton)
        h_box13.addWidget(self.line13)
        h_box13.addStretch()

        # Start Load Layout

        self.startLoad = QLabel('StartLoad: ')
        self.line14 = QLineEdit()
        self.line14.setFixedWidth(30)
        self.line14.setReadOnly(True)

        h_box14 = QHBoxLayout()
        h_box14.addSpacing(30)
        h_box14.addWidget(self.startLoad)
        h_box14.addWidget(self.line14)
        h_box14.addStretch()'''




        #third vertical layout that contains 5 horizental ones
        v_box3 = QVBoxLayout()
        v_box3.addSpacing(30)
        v_box3.addLayout(h_box10)
        v_box3.addStretch()
        v_box3.addLayout(h_box1)
        v_box3.addStretch()
        v_box3.addLayout(h_box9)
        v_box3.addStretch()
        v_box3.addLayout(v_box4)

        #horizental layout containing the fan controlling slider

        self.fan = QLabel('Fan Controller: ')
        self.lcd = QLCDNumber(self)
        self.sld = QSlider(Qt.Horizontal,self)
        self.sld.setMinimum(0)
        self.sld.setMaximum(100)
        palette = self.lcd.palette()
        palette.setColor(palette.Light, QColor(255, 0, 0))
        self.lcd.setPalette(palette)
        self.lcd.setFixedSize(55, 30)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.fan)
        hbox.addWidget(self.sld)
        hbox.addSpacing(30)
        hbox.addWidget(self.lcd)
        hbox.addStretch()








        # set general layout
        v_box0 = QVBoxLayout()

        h_box = QHBoxLayout()
        h_box.addLayout(v_box1)
        h_box.addStretch()
        h_box.addLayout(v_box2)
        h_box.addStretch()
        h_box.addLayout(v_box3)
        h_box.addSpacing(30)
        v_box0.addLayout(warning_layout)
        v_box0.addLayout(h_box)
        v_box0.addSpacing(30)

        v_box = QVBoxLayout()
        v_box.addLayout(v_box0)
        v_box.addLayout(hbox)

        self.setLayout(v_box)
        self.t = QTimer() #timer for the Balancing response
        self.t1 = QTimer() #timer for the HV Button response
        self.ie = QPixmap('C:/Users/iheb/BMS_UI/icons/error.png')
        self.i = QPixmap('C:/Users/iheb/BMS_UI/icons/respond.png')

    def fillBlanks(self): #methode that times the filling of the labels from the general tab
        self.timer1 = QTimer()
        self.timer1.timeout.connect(lambda: self.setData())
        self.timer1.start(2000)

    def setData(self): #methode that enables the data to be set
        self.d = self.data
        threading.Thread(target= self.d.fillData(140, 'soc')).start()
        threading.Thread(target=self.d.fillData(140, 'cs')).start()
        threading.Thread(target=self.d.fillData(140, 'bc')).start()
        threading.Thread(target=self.d.fillData(140, 'bv')).start()
        threading.Thread(target=self.d.fillData(140, 'sc')).start()
        threading.Thread(target=self.d.fillData(140, 'hvb')).start()
        threading.Thread(target=self.d.fillData(140, 'te')).start()
        threading.Thread(target=self.d.fillData(140, 'mxV')).start()
        threading.Thread(target=self.d.fillData(140, 'mnV')).start()
        threading.Thread(target=self.d.fillData(140, 'mxT')).start()
        threading.Thread(target=self.d.fillData(140, 'mnT')).start()
        threading.Thread(target=self.line.setText(str(self.d.getdata(cell=1, type='soc')))).start()
        threading.Thread(target=self.line1.setText(str(self.d.getdata(cell=1, type='cs')))).start()
        threading.Thread(target=self.line2.setText(str(self.d.getdata(cell=1, type='bv')))).start()
        threading.Thread(target=self.line3.setText(str(self.d.getdata(cell=1, type='sc')))).start()
        threading.Thread(target=self.line4.setText(str(self.d.getdata(cell=1, type='bc')))).start()
        threading.Thread(target=self.line5.setText(str(self.d.getdata(cell=1, type='mxV')))).start()
        threading.Thread(target=self.line6.setText(str(self.d.getdata(cell=1, type='mnV')))).start()
        threading.Thread(target=self.line7.setText(str(self.d.getdata(cell=1, type='mxT')))).start()
        threading.Thread(target=self.line8.setText(str(self.d.getdata(cell=1, type='mnT')))).start()
        threading.Thread(target=self.line9.setText(str(self.d.getdata(cell=1, type='hvb')))).start()
        threading.Thread(target=self.line10.setText(str(self.d.getdata(cell=1, type='te')))).start()
        #self.line11.setText(str(self.d.getdata(cell=1, type='airLsAux')))
        #self.line12.setText(str(self.d.getdata(cell=1, type='airHsAux')))
        #self.line13.setText(str(self.d.getdata(cell=1, type='hvb')))
        #self.line14.setText(str(self.d.getdata(cell=1, type='sl')))



    def start_Balancing(self):

        self.respond.setMinimumSize(30, 30)
        global Connected
        if Connected:
            try:



                if self.sender().text()== 'Start Balancing':
                    self.startBalancing.setText('Stop Balancing')
                    self.com1.balancing(self.bus)
                    print('balancing on')
                    self.respond.setPixmap(self.i.scaled(30, 30))
                    self.t.timeout.connect(lambda: threading.Thread(target=self.response(self.t, self.respond)).start())
                    self.t.start(2000)




                else:
                    self.startBalancing.setText('Start Balancing')
                    self.com1.stop_balancing(self.bus)
                    print('balancing off')
                    self.respond.setPixmap(self.i.scaled(30, 30))
                    self.t.timeout.connect(lambda: threading.Thread(target=self.response(self.t,self.respond)).start())
                    self.t.start(2000)
            except Exception as e:


                self.respond.setPixmap(self.ie.scaled(30, 30))
                logging.error(traceback.format_exc())
        else:
            print("you need to be connected")

    def response(self,timer,label):
        label.clear()
        timer.stop()



    def HV_clicked(self):
        self.respond1.setMinimumSize(30, 30)
        global Connected
        if Connected:
            try:
                self.com1.HV_simulate(self.bus)

                self.respond1.setPixmap(self.i_hv.scaled(30, 30))

                #self.t1.timeout.connect(lambda: threading.Thread(target=self.response(self.t1,self.respond1)).start())
                #self.t1.start(2000)
                self.line9.setText("on")
            except Exception as e:
                self.respond1.setPixmap(self.ie.scaled(30, 30))
                self.line9.setText("on")
                logging.error(traceback.format_exc())
        else:
            print("you need to be connected")

    def no_pcan(self):
        self.warning_label.setText('NO PCAN ADAPTER IS DETECTED, PLEASE PLUG ADAPTER AND RESTART THE PROGRAM')

    def controlFan(self,x):
        global Connected
        if Connected:
            try:
                print(x)
                #self.com1.control_fan(self.bus,self.data.getFanRotationSpeed(x),0x23)
                self.data.getFanRotationSpeed(x)
            except Exception as e:
                #self.enable.setChecked(False)
                logging.error(traceback.format_exc())
        else:
            print("you need to be connected")




####################################################################################################################






####################################################################################################################

class ErrorTab(QWidget):
    def __init__(self,bus,data,bms_com):
        super().__init__()
       # self.error_dar("Voltage Error:",self.checkVerror(), self.checkTerror())
        self.bus = bus
        self.data = data
        self.com = bms_com

        self.v_box = QVBoxLayout()
        self.setLayout(self.v_box)
        # set layout with the label and its icon
        h_box1 = QHBoxLayout()
        self.l = QLabel("Voltage Error:")
        self.p = QLabel('')
        self.i = QPixmap('C:/Users/iheb/BMS_UI/icons/voltage.ico')
        self.p.setPixmap(self.i.scaled(25, 25))

        h_box1.addWidget(self.p)
        h_box1.addWidget(self.l)
        h_box1.addStretch()
        # set layout with the label and its icon
        h_box2 = QHBoxLayout()
        self.l1 = QLabel("Temperature Error:")
        self.p1 = QLabel('')
        self.i1 = QPixmap('C:/Users/iheb/BMS_UI/icons/temperature.ico')
        self.p1.setPixmap(self.i1.scaled(25, 25))

        h_box2.addWidget(self.p1)
        h_box2.addWidget(self.l1)
        h_box2.addStretch()

        h_box3 = QHBoxLayout()
        self.l2 = QLabel('Current Error:')
        self.p2 = QLabel('')
        self.i2 = QPixmap('C:/Users/iheb/BMS_UI/icons/voltage.ico')
        self.p2.setPixmap(self.i2.scaled(25, 25))

        h_box3.addWidget(self.p2)
        h_box3.addWidget(self.l2)
        h_box3.addStretch()
        # set the final label
        '''self.v_box.addLayout(h_box3)
        self.v_box.addStretch()

        self.v_box.addSpacing(10)

        .c = self.error_dar('c')
        self.c_l = QHBoxLayout()
        self.c_l.addLayout(self.c)
        self.refresh(self.c_l,'c')
        self.v_box.addLayout(self.c_l)
        #self.update_c()
        self.v_box.addSpacing(10)
        self.v_box.addStretch()'''

        self.v_box.addLayout(h_box1)
        self.v_box.addStretch()

        self.v = self.error_dar('v')
        self.v_l = QHBoxLayout()
        self.v_l.addLayout(self.v)
        self.refresh(self.v_l, 'v')

        self.v_box.addLayout(self.v_l)
        self.v_box.addStretch()

        self.v_box.addLayout(h_box2)
        self.v_box.addStretch()

        self.t = self.error_dar('t')
        self.t_l = QHBoxLayout()
        self.t_l.addLayout(self.t)
        self.refresh(self.t_l, 't')

        self.v_box.addLayout(self.t_l)
        self.v_box.addStretch()





    def unfill(self, box): #methode that deletes the layout and its content
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())

        deleteItems(box)










    def error_dar(self,types): #methode that represent the cells errors in a radio button widget and returns Layouts
        self.grid = QGridLayout()
        threading.Thread(target=self.data.fillData(150,'v')).start()
        threading.Thread(target=self.data.fillData(80, 't')).start()
        threading.Thread(target=self.data.fillData(150, 'c')).start()


        values = np.array([7, 8, 21, 22, 35, 36, 49, 50,  63, 64, 77, 78, 91, 92, 105, 106,119, 120, 133, 134,
                  6, 9, 20, 23, 34, 37, 48, 51,  62, 65, 76, 79, 90, 93, 104, 107,118, 121, 132, 135,
                  5, 10, 19, 24, 33, 38, 47, 52, 61, 66, 75, 80, 89, 94, 103, 108,117, 122, 131, 136,
                  4, 11, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81, 88, 95, 102, 109,116, 123, 130, 137,
                  3, 12, 17, 26, 31, 40, 45, 54, 59, 68, 73, 82, 87, 96, 101, 110,115, 124, 129, 138,
                  2, 13, 16, 27, 30, 41, 44, 55, 58, 69, 72, 83, 86, 97, 100, 111,114, 125, 128, 139,
                  1, 14, 15, 28, 29, 42, 43, 56, 57, 70, 71, 84, 85, 98, 99,  112,113, 126, 127, 140,
                  ])
        positions = np.array([(i,j) for i in range(7) for j in range(20)])

        values1 = np.array([4,5,12,13,20,21,28,29,36,37,44,45,52,53,60,61,68,69,76,77,
                   3,6,11,14,19,22,27,30,35,38,43,46,51,54,59,62,67,70,75,78,
                   2,7,10,15,18,23,26,31,34,39,42,47,50,55,58,63,66,71,74,79,
                   1,8, 9,16,17,24,25,32,33,40,41,48,49,56,57,64,65,72,73,80])

        positions1 = np.array([(i, j) for i in range(4) for j in range(20)])


        if types == 'v':

            #self.data.checkErrors(140, 'v')
            h_box1 = QHBoxLayout()

            for position, value in zip(positions, values):
                #print('position = ' + str(position))
                #print('value = ' + str(values))
                if value == '':
                    continue
                self.b= QRadioButton(str(value))
                self.b.setEnabled(False)
                if not(self.getErrors(value,'v',self.data)): #check errors for every cell while creating the radiobutton
                    self.b.setChecked(True)
                else:
                    self.b.setChecked(False)
                self.grid.addWidget(self. b, *position)
            h_box1.addLayout(self.grid)
            return h_box1







        elif types == 't':
            #self.data.checkErrors(80, 't')
            h_box2 = QHBoxLayout()
            for position, value in zip(positions1, values1):

                if value == '':
                    continue
                self.b = QRadioButton(str(value))
                self.b.setEnabled(False)
                if not(self.getErrors(value,'t',self.data)):
                    self.b.setChecked(True)

                else:
                    self.b.setChecked(False)

                if value %4 ==1:
                    self.b.setChecked(True)

                self.grid.addWidget(self.b, *position)

            h_box2.addLayout(self.grid)
            return h_box2



        elif types == 'c':
            #self.data.checkErrors(140, 'c')
            self.b1 = QRadioButton('No Error')
            self.b2 = QRadioButton('Error')
            h_box = QHBoxLayout()
            h_box.addWidget(self.b1)
            h_box.addStretch()
            h_box.addWidget(self.b2)
            h_box.addStretch()
            self.b1.setEnabled(False)
            self.b2.setEnabled(False)
            if not(self.getErrors(1,'c',self.data)):
                self.b1.setChecked(True)
            else:
                self.b2.setChecked(True)

            return h_box



    def update_error(self,layout, type ): #methode that updates the errors representation
        try:



            if type == 'v':
                self.unfill(layout)



                layout.addLayout(self.error_dar('v'))
            elif type == 't':
                self.unfill(layout)



                layout.addLayout(self.error_dar('t'))
            elif type =='c':

                self.unfill(layout)

                layout.addLayout(self.error_dar('c'))
        except TypeError:
            print('error with Error-update')



    def refresh(self, layout, type): #methode that times the updates of the errors representation
        try:

            if type == 'v':
                self.timer1 = QTimer()
                self.timer1.timeout.connect(lambda: self.update_error(layout,'v'))

                self.timer1.start(3000)
            elif type == 't':
                self.timer2 = QTimer()
                self.timer2.timeout.connect(lambda: self.update_error(layout, 't'))

                self.timer2.start(3000)
            elif type == 'c':
                self.timer3 = QTimer()
                self.timer3.timeout.connect(lambda: self.update_error(layout, 'c'))

                self.timer3.start(3000)



        except TypeError:
            print('problem with Error-refresh')
            self.bus.shutdown()








    def getErrors(self, cell , type,object): #methode that returns the errors from the Data class
        errorCheck = Data(140,self.bus,self.com)

        threading.Thread(target= errorCheck.checkErrors(140, 'c',object)).start()
        threading.Thread(target=errorCheck.checkErrors(140, 'v',object)).start()
        threading.Thread(target=errorCheck.checkErrors(140, 't',object)).start()


        if (type == 'v'):
            return errorCheck.getErrors(cell-1,'v')
        elif (type == 't'):
            return errorCheck.getErrors(cell-1,'t')
        elif (type == 'c'):
            return errorCheck.getErrors(cell-1,'c')












####################################################################################################################


#####################################################################################################################


class CellTab(QWidget):

    def __init__(self, r , c,bus,data,bms_com):
        super().__init__()
        self.bus = bus
        self.data = data
        self.com = bms_com
        self.tableWidget = QTableWidget(r, c)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  #makes table read only

        for i in range(c):
            self.tableWidget.setColumnWidth(i,90)
        #adjuct cells to the size of the contents
        #self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #self.tableWidget.resizeColumnsToContents()
        col_headers = []
        for i in range(c):
            a = 'cell:' + str(i + 1)
            col_headers += [a]
        self.tableWidget.setHorizontalHeaderLabels(col_headers)



        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1000)
        self.slider.setMaximum(15000)
        self.slider.setTickInterval(1000)

        self.slider.setTickPosition(QSlider.TicksBelow)

        self.le = QLineEdit('1000ms')
        self.le.setFixedWidth(60)

        self.b = QPushButton("Clear")
        self.b1 = QPushButton("Start Refresh")
        self.b2 = QPushButton("Save")

        self.v = QCheckBox("Voltage")
        self.t = QCheckBox("Temperature")
        self.v.setChecked(True)
        self.t.setChecked(True)







        self.tableWidget.cellDoubleClicked.connect(self.cell_was_clicked)



        self.averageVoltage = QLabel('cells Average Voltage: ')
        self.lineAV = QLineEdit()
        self.lineAV.setFixedWidth(80)
        self.lineAV.setReadOnly(True)
        self.logoAV = QLabel('')
        self.iAV = QPixmap("C:/Users/iheb/BMS_UI/icons/average voltage.png")
        self.logoAV.setPixmap(self.iAV.scaled(40, 40))

        self.averageTemperature = QLabel('cells Average Temperature: ')
        self.lineAT = QLineEdit()
        self.lineAT.setFixedWidth(80)
        self.lineAT.setReadOnly(True)
        self.logoAT= QLabel('')
        self.iAT = QPixmap("C:/Users/iheb/BMS_UI/icons/average temp.png")
        self.logoAT.setPixmap(self.iAT.scaled(40, 40))
        self.v3 = QLabel('V')
        self.t1 = QLabel('C°')

        h_box1 = QHBoxLayout()

        h_box1.addWidget(self.logoAV)
        h_box1.addWidget(self.averageVoltage)
        h_box1.addWidget(self.lineAV)
        h_box1.addWidget(self.v3)

        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.logoAT)
        h_box2.addWidget(self.averageTemperature)
        h_box2.addWidget(self.lineAT)
        h_box2.addWidget(self.t1)

        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box1)
        v_box1.addLayout(h_box2)

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.le)
        h_box.addWidget(self.slider)
        h_box.addWidget(self.b1)
        h_box.addWidget(self.b2)
        h_box.addWidget(self.b)

        h_box.addStretch()

        h_box.addWidget(self.v)
        h_box.addWidget(self.t)
        h_box.addLayout(v_box1)

        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addWidget(self.tableWidget)
        v_box.addLayout(h_box)



        self.setLayout(v_box)

    def cell_was_clicked(self):
        try:
            print(str(self.tableWidget.selectedItems()))

        except TypeError:
            logging.error(traceback.format_exc())
            print('Error when selecting a cell')
            self.bus.shutdown()



    def clear(self,b,r,c): #methode that clears the table cells

        b.clearContents()
        b.setColumnCount(c)
        b.setRowCount(r)


    def refresh(self, button, v_check, t_check, table, c): #methode that times the updating of the table
        sender = self.sender()
        #timer
        self.timer = QTimer()
        #connectTimer
        if sender.text() == 'Start Refresh':
            button.setText('Stop Refresh')

            threading.Thread(target= self.timer.timeout.connect(lambda: self.thread_refill1(v_check, t_check, table, c, self.timer))).start()

            #t1.setDaemon(False)

        elif sender.text() == 'Stop Refresh':
            button.setText('Start Refresh')

            threading.Thread(target=self.timer.timeout.connect(lambda: self.thread_refill2(v_check, t_check, table, c, self.timer))).start()


            #t2.setDaemon(False)

            print('not refreshing')
        #startTimer
        refresh_time = self.getRefreshTime()
        self.timer.start(refresh_time)

    def thread_refill1(self,v_check, t_check, table, c, timer):
        t1 = threading.Thread(target=self.tab_refill(v_check, t_check, table, c, True, timer))
        t1.setDaemon(True)
        t1.start()

    def thread_refill2(self,v_check, t_check, table, c,timer):
        t2 = threading.Thread(target=self.tab_refill(v_check, t_check, table, c, False, timer))
        t2.setDaemon(True)
        t2.start()

    def tab_refill (self,v_checkBox,t_checkBox, table, c,ok, timer): #methode that refill the cell table
        try:
            if ok:
                threading.Thread(target=self.data.fillData(140, 'v')).start()
                threading.Thread(target=self.data.fillData(80, 't')).start()
                self.av =0
                if v_checkBox.isChecked():
                    table.insertRow(0)
                    for i in range(c):
                        v=self.getCells(i,'v')
                        t1= threading.Thread(target= table.setItem(0, i, QTableWidgetItem('V:'+str(v))))
                        table.item(0,i).setBackground(QColor(250,250,0))
                        t1.setDaemon(True)
                        t1.start()

                        self.av +=v
                        if self.getErrors(i-1, 'v'):
                            table.item(0,i).setBackground(QColor(250,0,0))
                    #print('voltage is checked')
                    #print(self.av/table.columnCount())
                    self.lineAV.setText(str(format(self.av/table.columnCount(), '.2f')))
                    #self.lineAV.setText(str(self.data.getCellVoltage(12)))
                self.at = 0
                if t_checkBox.isChecked():
                    table.insertRow(0)

                    for i in range(c-60):
                        t=self.getCells(i,'t')
                        t3 = threading.Thread(target= table.setItem(0, i, QTableWidgetItem('T:'+str(t))))
                        table.item(0, i).setBackground(QColor(0, 200, 200))
                        t3.setDaemon(True)
                        t3.start()

                        self.at+=t
                        if self.getErrors(i-1, 't'):
                            table.item(0, i).setBackground(QColor(250, 0, 0))
                        if (i+1)%4 == 1:
                            t4 = threading.Thread(target=table.setItem(0, i, QTableWidgetItem('unplausibel')))
                            table.item(0, i).setBackground(QColor(250, 0, 0))
                            t4.setDaemon(True)
                            t4.start()
                    #print('temperature is checked')
                    #print(self.at / table.columnCount())
                    self.lineAT.setText(str(format(self.at / table.columnCount(), '.2f')))
                if not (t_checkBox.isChecked()) and not(v_checkBox.isChecked()):

                    print('pick one')
            else:

                timer.stop()
        except TypeError:
            logging.error(traceback.format_exc())
            print('Error while refreshing the cell Table')
            self.bus.shutdown()

    def getCells(self,cell,type): #methode that get's the cell data from the Data class

        #self.data.fillVData(num = 140, type='v')

        if type =='v':


            return self.data.getdata(cell,'v')/1000

        elif type == 't':

            return self.data.getdata(cell,'t')/10

    def getErrors(self, cell, type): #methode that get's the errors from the Data class
        self.dataError = Data(140,bus=self.bus,com=self.com)
        threading.Thread(target= self.dataError.checkErrors(140, 'c',self.data)).start()
        threading.Thread(target=self.dataError.checkErrors(140, 'v',self.data)).start()
        threading.Thread(target=self.dataError.checkErrors(80, 't',self.data)).start()




        return not(self.dataError.getErrors(cell, type))



    def updateData(self):
        #self.data = Data(140, bus=self.bus)

        return self.data





    def v_change(self): #methode that tracks the value changes of the Slider therefore for the time of refresh
        my_value = str(self.slider.value())
        self.le.setText(my_value+'ms')

    def lbl(self): #methoe that overwrites the value of the slider when manually written in the label
        if int(self.le.text()) >= 1000 and  int(self.le.text())<=15000:
            self.slider.setValue(int(self.le.text()))

        elif self.le.text() is '':
            pass

        else:
            pass

    def getRefreshTime(self): #methode that returns the refresh time set  either by the slider or the label next to it


        return self.slider.value()



    def save_file(self): #methode that saves the cell table as a csv file
        path = QFileDialog.getSaveFileName(self.tableWidget, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        try:
            if path[0] != '':
                with open(path[0], 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file, dialect='excel', delimiter=';')
                    for row in range(self.tableWidget.rowCount()):
                        row_data = []

                        for column in range(self.tableWidget.columnCount()):
                            item = self.tableWidget.item(row, column)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append('')
                        writer.writerow(row_data)
        except Exception as e:
            logging.error(traceback.format_exc())
            print('error while saving')

    def get_voltages_from_table(self,j):
        v = []

        j=0
        while(True):
            if self.tableWidget.item(j, 0).text()[:1] == 'V':

                for i in range(self.tableWidget.columnCount()):
                    a = self.tableWidget.item(j, i).text()
                    v.append(int(a[2:]))
                break

            else:
                j+=1
        return v

            ####################################################################################################################

class MyTabsWidget(QWidget):
    def __init__(self,bus,data,bms_com):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.bus= bus



        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        #self.tab4 = QWidget()
        #self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Generals")
        self.tabs.addTab(self.tab2, "Cells")
        self.tabs.addTab(self.tab3, "Errors")
        #self.tabs.addTab(self.tab4, "Driver Informations")


        #create first tab
        thread1 = threading.Thread(target=self.create_tab1(bus,data,bms_com))
        thread1.setDaemon(True)
        thread1.start()



        # Create second tab

        thread2 = threading.Thread(target=self.create_tab2(bus, data,bms_com))
        thread2.setDaemon(True)
        thread2.start()

        #create third tab

        thread3 = threading.Thread(target=self.create_tab3(bus, data,bms_com))
        thread3.setDaemon(True)
        thread3.start()

        #create_forth_tab
        '''thread4 = threading.Thread(target=self.create_tab4(bus,data,bms_com))
        thread4.setDaemon(True)
        thread4.start()'''

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def create_tab1(self,bus,data,bms_com):
        self.tab1.layout = QVBoxLayout(self)

        self.first_tab = GeneralsTab(bus, data,bms_com)
        t = threading.Thread(target=self.first_tab.fillBlanks())
        t.setDaemon(True)
        t.start()

        t2 =threading.Thread(target= self.first_tab.startBalancing.clicked.connect(self.first_tab.start_Balancing))
        t2.setDaemon(True)
        t2.start()
        t3 = threading.Thread(target=self.first_tab.HVButton.clicked.connect(self.first_tab.HV_clicked))
        t3.setDaemon(True)
        t3.start()
        t4 = threading.Thread(target= self.first_tab.sld.valueChanged.connect(lambda: self.first_tab.controlFan(self.first_tab.sld.value())))
        t4.setDaemon(True)
        t4.start()

        self.first_tab.sld.valueChanged.connect(self.first_tab.lcd.display)


        self.tab1.layout.addWidget(self.first_tab)

        self.tab1.setLayout(self.tab1.layout)

    def create_tab2(self,bus,data,bms_com):
        self.tab2.layout = QVBoxLayout(self)

        self.second_tab = CellTab(0, 140, bus, data,bms_com)
        # clear button
        self.second_tab.b.clicked.connect(lambda: self.second_tab.clear(self.second_tab.tableWidget, 0, 140))
        # save Button
        self.second_tab.b2.clicked.connect(self.second_tab.save_file)
        # refreshButton
        self.second_tab.b1.clicked.connect(lambda: threading.Thread(target= self.second_tab.refresh(self.second_tab.b1, self.second_tab.v,
                                            self.second_tab.t, self.second_tab.tableWidget,
                                            140)).start())

        # slider bar
        self.second_tab.slider.valueChanged.connect(self.second_tab.v_change)
        self.second_tab.le.returnPressed.connect(self.second_tab.lbl)

        self.tab2.layout.addWidget(self.second_tab)

        self.tab2.setLayout(self.tab2.layout)


    def create_tab3(self,bus,data,bms_com):
        self.tab3.layout = QVBoxLayout(self)
        self.third_tab = ErrorTab(bus, data,bms_com)
        # self.third_tab.error_dar()
        '''t1 = threading.Thread(target=self.third_tab.update_me())
        t1.setDaemon(True)
        t1.start()'''

        self.tab3.layout.addWidget(self.third_tab)

        self.tab3.setLayout(self.tab3.layout)


    '''def create_tab4(self, bus,data, bms_com):
        self.tab4.layout = QVBoxLayout(self)
        self.forth_tab = DriverInformations(bus,data,bms_com)
        t1 = threading.Thread(target=self.forth_tab.HVButton.clicked.connect(self.forth_tab.HV_clicked))
        t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=self.forth_tab.startButton.clicked.connect(self.forth_tab.start_clicked))
        t2.setDaemon(True)
        t2.start()
        t3 = threading.Thread(target=self.forth_tab.rekuButton.clicked.connect(self.forth_tab.Reku_clicked))
        t3.setDaemon(True)
        t3.start()
        t4 = threading.Thread(target=self.forth_tab.lr1.clicked.connect(self.forth_tab.lr1_clicked))
        t4.setDaemon(True)
        t4.start()
        t5 = threading.Thread(target=self.forth_tab.lr2.clicked.connect(self.forth_tab.lr2_clicked))
        t5.setDaemon(True)
        t5.start()
        t6 = threading.Thread(target=self.forth_tab.lr3.clicked.connect(self.forth_tab.lr3_clicked))
        t6.setDaemon(True)
        t6.start()
        t7 = threading.Thread(target=self.forth_tab.lr4.clicked.connect(self.forth_tab.lr4_clicked))
        t7.setDaemon(True)
        t7.start()
        t8 = threading.Thread(target=self.forth_tab.lr5.clicked.connect(self.forth_tab.lr5_clicked))
        t8.setDaemon(True)
        t8.start()
        t9 = threading.Thread(target=self.forth_tab.lr6.clicked.connect(self.forth_tab.lr6_clicked))
        t9.setDaemon(True)
        t9.start()


        self.tab4.layout.addWidget(self.forth_tab)
        self.tab4.setLayout(self.tab4.layout)'''


####################################################################################################################



class Nanni_Main_Window(QMainWindow):

    def __init__(self,bus,data,bms_com):
        super().__init__()

        self.data = data
        self.counter=0
        self.com = bms_com
        self.bus = bus

        self.tabs_widget = MyTabsWidget(self.bus, self.data, self.com)

        self.setCentralWidget(self.tabs_widget)



        #create Menu Bar
        bar = self.menuBar()

        #create root Menus
        file = bar.addMenu('File')
        connection = bar.addMenu('Connection')
        graph =  bar.addMenu('Graphs')

        #find = file.addMenu('Find')

        #create actions to Menus
        save = QAction('Save', self)
        save.setShortcut('Ctrl+S')

        '''open = QAction('Open', self)
        open.setShortcut('Ctrl+O')'''

        new = QAction("New Window", self)
        new.setShortcut("Ctrl+N")

        exit = QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')

        disconnect = QAction('Disconnect', self)

        connect = QAction('Connect', self)


        '''find_action = QAction('find..' , self)
        find_action.setShortcut('Ctrl+F')

        replace_action = QAction('replace..' , self)
        replace_action.setShortcut('Ctrl+R')'''

        v_graph = QAction('Voltage Graph', self)
        t_graph = QAction('Temperature Graph', self)



        #add actions to Menus
        file.addAction(new)
        file.addAction(save)
        #file.addAction(open)

        file.addAction(exit)

        connection.addAction(connect)
        connection.addAction(disconnect)
        #find.addAction(find_action)
        # find.addAction(replace_action)
        graph.addAction(v_graph)
        graph.addAction(t_graph)
        #events

        exit.triggered.connect(self.quite_trigger)
        save.triggered.connect(self.tabs_widget.second_tab.save_file)
        new.triggered.connect(self.new_Widget)
        connect.triggered.connect(self.Connecting) #check it out
        disconnect.triggered.connect(self.deconnecting)
        #refresh.triggered.connect(self.updateComPorts) #check it out

        v_graph.triggered.connect(lambda: self.thread_plot('v'))
        t_graph.triggered.connect(lambda: self.thread_plot('t'))



        self.setWindowTitle("Nanni\'s little helper")
        self.setWindowIcon(QIcon('C:/Users/iheb/BMS_UI/icons/main_logo.png'))
        self.resize(1000, 500)
        self.show()

    def quite_trigger(self):
        qApp.quit()




    def anim_v(self):
        fig = plt.figure('Voltage Graph',figsize= (12,5))
        plt.title('epic graph')
        plt.ylabel('Voltages (mV)')
        plt.xlabel('cells')




        d= self.data

        x = np.array([0]*140)
        y = np.array([0]* 140)
        for i in range(140):
            x[i]= (i+1)
            y[i] = d.getdata(i,'v')

        # data = np.column_stack([np.linspace(0, yi, 50) for yi in y])

        rects = plt.bar(x, y, color='dodgerblue')
        line, = plt.plot(x, y, color='red')
        plt.grid(axis='y')
        plt.ylim(2700)

        def animate(index):

            d.fillData(141, 'v')
            ys = np.array([0.0]*140)

            for j in range(140):

                ys[j] = d.getdata(j,'v')





            for rect, yi in zip(rects, ys):
                rect.set_height(yi)
            line.set_data(x, ys)
            del(ys)


            return rects, line

        refresh_time = self.tabs_widget.second_tab.getRefreshTime()  # this variable must be crated to avoid crashing after dynamically changing the value of refresh time
        ani = animation.FuncAnimation(fig=fig, func=animate, interval=refresh_time)

        plt.show()



    def anim_t(self):
        fig1 = plt.figure('Temperature Graph', figsize=(12, 5))
        plt.title('epic graph')
        plt.ylabel('Temperature')
        plt.xlabel('cells')

        d = self.data

        x = np.arange(1,61,1)
        y = []
        for i in range(80):
            if (i+1)%4!=1:
                y.append(d.getdata(i, 't')/10)



        # data = np.column_stack([np.linspace(0, yi, 50) for yi in y])

        rects1 = plt.bar(x, y, color='tomato')
        line1, = plt.plot(x, y, color='k')
        plt.grid(axis='y')

        def animate(i):
            d.fillData(81, 't')
            ys = []

            for j in range(80):
                if j%4 != 1:

                    ys.append(d.getdata(j, 't')/10)








            for rect, yi in zip(rects1, ys):
                rect.set_height(yi)
            line1.set_data(x, ys)
            del(ys)
            return rects1 , line1


        refresh_time = self.tabs_widget.second_tab.getRefreshTime() #this variable must be crated to avoid crashing after dynamically changing the value of refresh time
        ani = animation.FuncAnimation(fig=fig1, func=animate, interval= refresh_time)

        plt.show()

    def thread_plot(self,type):
        if type == 'v':
            t1 = threading.Thread(target=self.anim_v())
            t1.setDaemon(True)
            t1.start()
        if type == 't':
            t2 = threading.Thread(target=self.anim_t())
            t2.setDaemon(True)
            t2.start()




    '''def draw_v(self):
        if self.tabs_widget.second_tab.tableWidget.rowCount() != 0:
            j = 0
            chk = True
            while (chk):
                if self.tabs_widget.second_tab.tableWidget.item(j, 0).text()[:1] == 'V':
                    self.voltage=[0]
                    for i in range (self.tabs_widget.second_tab.tableWidget.columnCount()):
                        a = self.tabs_widget.second_tab.tableWidget.item(j, i).text()
                        self.voltage.append(int(a[2:]))

                    print(self.voltage[1:])
                    #style.use('seaborn')

                    fig = plt.figure('Voltage Graph',figsize= (12,5))
                    ax = fig.add_subplot(1,1,1,)
                    plt.title('epic graph')
                    plt.ylabel('voltage')
                    plt.xlabel('cells')
                    ax.clear()
                    ax.bar(range(141),self.voltage[:], color='dodgerblue')


                    plt.grid()
                    plt.show()
                    chk = False



                else:
                    j+=1
            return(self.voltage)
        else :
            print('no data to plot')

    def draw_t(self):
        if self.tabs_widget.second_tab.tableWidget.rowCount() != 0:
            j=0
            chk= True
            while (chk):
                print(self.tabs_widget.second_tab.tableWidget.item(j, 0).text()[:1])
                if self.tabs_widget.second_tab.tableWidget.item(j, 0).text()[:1] == 'T':
                    self.temperature=[0]
                    for i in range (self.tabs_widget.second_tab.tableWidget.columnCount()):
                        a = self.tabs_widget.second_tab.tableWidget.item(j, i).text()
                        self.temperature.append(int(a[2:]))

                    print(self.temperature[1:])
                    #style.use('seaborn')
                    a = plt.figure('Temperature Graph',figsize= (12,5))
                    ax = a.add_subplot(1,1,1)
                    plt.title('epic graph')
                    plt.ylabel('Temperature')
                    plt.xlabel('cells')
                    ax.clear()

                    ax.bar(range(141),self.temperature[:],color= 'tomato')
                    plt.grid()
                    plt.show()
                    chk= False
                else:
                    j+=1'''







    def new_Widget(self):
        self.n = MyTabsWidget(self.bus, self.data, self.com)
        self.n.setWindowTitle('Nanni\'s little helper  1.0')
        self.n.setWindowIcon(QIcon('C:/Users/iheb/BMS_UI/icons/main_logo.png'))
        self.n.setGeometry(600,400,1000, 500)
        self.n.show()


    def Connecting(self):
        try:

            self.com.starting(self.bus)
            global Connected
            Connected = True


            #print('hey')
        except TypeError:
            print('error connecting')


    def deconnecting(self):
        try:
            #print('hey')
            self.com.terminate()
            global Connected
            Connected = False
        except TypeError:
            print('error deconnecting')







########################################## Main #######################################################
def main():
    try:
        bms_com = BMS_Communications()
        style.use('seaborn')#style for matplotlib graph

        print('Start')
        try:
            bus = bms_com.initialize_bus()
            atexit.register(bus.shutdown)
            data = Data(150, bus, bms_com)
            app = QApplication(sys.argv)
            a_window = Nanni_Main_Window(bus,data,bms_com)
            a_window.show()
            gui_thread = threading.Thread(target=sys.exit(app.exec_()))
            gui_thread.setDaemon(True)
            gui_thread.start()

        except can.CanError:
            print('No Pcan adapter is connected')
            bus = [1, 2, 3]


            data = Data(150, bus, bms_com)

            app = QApplication(sys.argv)

            a_window = Nanni_Main_Window(bus, data, bms_com)
            a_window.tabs_widget.first_tab.no_pcan()
            a_window.show()
            gui_thread = threading.Thread(target=sys.exit(app.exec_()))
            gui_thread.setDaemon(True)
            gui_thread.start()

    except Exception as e:
        logging.error(traceback.format_exc())

main()