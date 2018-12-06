''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''

import atexit
import logging
import threading
import traceback

import can
from can.bus import BusABC
from can.interfaces.pcan import PcanBus

import BMS_ControlParameter as p
import BMS_Data


########################################### communication #############################################################

class Communications(BusABC):
    def __init__(self):
        super().__init__()
        self.connectController=0
        self.disconnectController = 0
        self.startCommunication = False
        self.ReadBusController = False # control

    def comm(self,bus):
        try:
            print('starting communications')
            self.sending(bus, p.dummyBite, id=p.USER_COMMAND_CAN_MESSAGE)
            for msg in bus:
                if self.ReadBusController:


                    threading.Thread(target= self.sending(bus,[0,0,0,0], p.DIS_CAN_MESSAGE)).start()
                    print('DIS')
                    threading.Thread(target= self.sending(bus,p.getVoltagesCommand,id=p.USER_COMMAND_CAN_MESSAGE)).start()
                    print('voltage requested')
                    #print(msg)
                    if msg.arbitration_id in p.voltageIDs:
                        dic = {'ID': 0, 'data': []}
                        dic['ID'] = hex(msg.arbitration_id)
                        for i in range(len(msg.data)):
                            dic['data'].append(msg.data[i])
                        BMS_Data.rawVoltages.append(dic)
                        if len(BMS_Data.rawVoltages) > 500:
                            del (BMS_Data.rawVoltages[0:300])
                    if msg.arbitration_id in p.temperatureIDs:
                        dic1 = {'ID': 0, 'data': []}
                        dic1['ID'] = hex(msg.arbitration_id)
                        for j in range(len(msg.data)):
                            dic1['data'].append(msg.data[j])
                            BMS_Data.rawTemperatures.append(dic1)
                        if len(BMS_Data.rawTemperatures) > 500:
                            del (BMS_Data.rawTemperatures[0:300])
                    if msg.arbitration_id == p.generalsID:

                        list1 = []
                        for i in range(len(msg.data)):
                            list1.append(msg.data[i])
                            BMS_Data.rawGenerals.append(list1)

                        if len(BMS_Data.rawGenerals) > 300:
                            del(BMS_Data.rawGenerals[:200])
                    if msg.arbitration_id == p.ENERGYMETER_STROM_ID:
                        list1 = [88,88,88,88]
                        for i in range(4):
                           list1[i]= msg.data[i+2]
                           BMS_Data.rawStrom.append(list1)

                else:

                    break
            p.setBusStatus(True)
        except can.CanError:
            logging.error(traceback.format_exc())
            p.setBusStatus(False)
            bus.reset()

    def sending(self,bus, d, id):
        try:
            msg = can.Message(arbitration_id=id, data=d, extended_id=False)
            bus.send(msg)
            p.setBusStatus(True)
        except can.CanError:
            logging.error(traceback.format_exc())
            p.setBusStatus(False)
            bus.reset()
    def terminate(self):

        self.ReadBusController = False #Disable reading from bus
        self.connectController = 0
        self.disconnectController +=1
        if self.disconnectController == 2:
            print(BMS_Data.rawVoltages)
            print('v')
        elif self.disconnectController == 3:
            print(BMS_Data.rawTemperatures)
            self.disconnectController=1
            print('t')

    def close(self,bus):
        bus.shutdown()

    def starting(self,bus):
        try:
            self.connectController += 1

            if self.connectController == 1:

                self.disconnectController = 0

                self.ReadBusController = True

                t = threading.Thread(target=lambda: self.comm(bus))
                t.setDaemon(True)
                t.start()

            else:
                pass
            p.setBusStatus(True)
        except can.CanError:
            print('error Can')
            p.setBusStatus(False)
            bus.reset()


    def initialize_bus(self):
        bus = PcanBus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
        atexit.register(bus.shutdown)
        p.setBusStatus(True)
        return bus


    def balancing(self,bus):
        try:
            self.sending(bus,p.startBalancingCommand,id=p.USER_COMMAND_CAN_MESSAGE)
            print('balancing')
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())


    def stop_balancing(self,bus):
        try:
            self.sending(bus, d= p.stopBalancingCommand,id=p.USER_COMMAND_CAN_MESSAGE)
            print('balancing stopped')
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())

    def HV_simulate(self,bus):
        try:
            for i in range(10):
                self.sending(bus, d=p.hvSimulationCommand,id=p.DIS_CAN_MESSAGE)
            print('HV Clicked')
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())

    def sendFanControl(self,bus,data):
        try:

            self.sending(bus,d=[p.fanControlCommand, data],id=p.USER_COMMAND_CAN_MESSAGE)
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())

    def setUserFlag(self, bus):
        try:
            self.sending(bus,d=p.setUserCommand,id=p.USER_COMMAND_CAN_MESSAGE)
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())

    def resetUserFlag(self, bus):
        try:
            self.sending(bus,d=p.resetUserCommand,id=p.USER_COMMAND_CAN_MESSAGE)
            p.setBusStatus(True)
        except can.CanError:
            p.setBusStatus(False)
            logging.error(traceback.format_exc())


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

        print('LR6 Clicked')

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

            a = cell % 4
            return a-1
        else:
            print('item not in the list')
            return 1

    def get_id(self, cell, first_id):
        #if cell in range(1, 141, 1):
        id = first_id + ((cell - 1) // 4)
        return hex(id)

    def get_cell_voltage(self,cell):
        idleVoltage = 3808 #ERRORS
        try:
            for i in range(len(self.Voltages) - 1, 0, -1):

                if self.Voltages[i]['ID'] == self.get_id(cell, p.voltageID[0]):
                    idleVoltage = (self.Voltages[i]['data'][self.get_position(cell) * 2] << 8) + self.Voltages[i]['data'][self.get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break

            return idleVoltage
        except Exception as e:
            logging.error(traceback.format_exc())

    def get_cell_temperature(self,cell):
        idleTemperature = 400 #ERROR
        try:
            for i in range(len(self.Temperatures) - 1, 0, -1):
                if self.Temperatures[i]['ID'] == self.get_id(cell, p.temperatureID[0]):
                    idleTemperature = (self.Temperatures[i]['data'][self.get_position(cell) * 2] << 8) \
                        + self.Temperatures[i]['data'][self.get_position(cell) * 2 + 1]
                    #print('a=',a)
                    #print('V=',self.Voltages)
                    # print(Voltages[i])
                    #print(self.Voltages[i]['ID'])
                    #print(self.Voltages[i]['data'][self.get_position(cell)])

                    break

            return idleTemperature
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
            logging.error(traceback.format_exc())'''



    ################################################################################################################
