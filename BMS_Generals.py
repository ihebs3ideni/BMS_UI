''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''

import logging
import threading
import traceback

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import (QHBoxLayout,
                             QVBoxLayout,
                             QPushButton, QWidget, QCheckBox, QSlider, QLabel, QLineEdit, QLCDNumber)

import BMS_ControlParameter
import BMS_Data


##########################################GenerlsTab #########################################################

class GeneralsTab(QWidget):
    def __init__(self,bus, bms_com):
        super().__init__()
        self.com1 = bms_com
        self.bus = bus

        '''self.warning_label = QLabel()
        warning_layout = QHBoxLayout()
        warning_layout.addStretch()
        warning_layout.addWidget(self.warning_label)
        warning_layout.addStretch()'''



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


        #HV_Button_simuator
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

        self.comment = QLabel('Enable')
        self.enable = QCheckBox()
        self.fan = QLabel('Fan Controller: ')
        self.lcd = QLCDNumber(self)
        self.sld = QSlider(Qt.Horizontal,self)
        self.sld.setMinimum(0)
        self.sld.setMaximum(100)
        self.sld.setTickInterval(1)
        palette = self.lcd.palette()
        palette.setColor(palette.Light, QColor(255, 0, 0))
        self.lcd.setPalette(palette)
        self.lcd.setFixedSize(55, 30)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.comment)
        hbox.addWidget(self.enable)
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
        #v_box0.addLayout(warning_layout)
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
        """self.d = self.data
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
        threading.Thread(target=self.d.fillData(140, 'mnT')).start()"""
        self.line.setText(str(BMS_Data.getdata(cell=1, type='soc')))

        self.line1.setText(str(BMS_Data.getdata(cell=1, type='cs')))
        #print(str(BMS_Data.getdata(cell=1, type='cs')))
        self.line2.setText(str(BMS_Data.getdata(cell=1, type='bv')))
        #print(str(BMS_Data.getdata(cell=1, type='bv')))
        self.line3.setText(str(BMS_Data.getdata(cell=1, type='sc')))
        #print(str(BMS_Data.getdata(cell=1, type='sc')))
        self.line4.setText(str(BMS_Data.getdata(cell=1, type='bc')))
        #print(str(BMS_Data.getdata(cell=1, type='bc')))
        self.line5.setText(str(BMS_Data.getdata(cell=1, type='mxV')))
        #print(str(BMS_Data.getdata(cell=1, type='mxV')))
        self.line6.setText(str(BMS_Data.getdata(cell=1, type='mnV')))
        #print(str(BMS_Data.getdata(cell=1, type='mnV')))
        self.line7.setText(str(BMS_Data.getdata(cell=1, type='mxT')))
        #print(str(BMS_Data.getdata(cell=1, type='mxT')))
        self.line8.setText(str(BMS_Data.getdata(cell=1, type='mnT')))
        #print(str(BMS_Data.getdata(cell=1, type='mnT')))
        self.line9.setText(str(BMS_Data.getdata(cell=1, type='hvb')))
        #print(str(BMS_Data.getdata(cell=1, type='hvb')))
        self.line10.setText(str(BMS_Data.getdata(cell=1, type='te')))
        #print(str(BMS_Data.getdata(cell=1, type='te')))
        #self.line11.setText(str(self.d.getdata(cell=1, type='airLsAux')))
        #self.line12.setText(str(self.d.getdata(cell=1, type='airHsAux')))
        #self.line13.setText(str(self.d.getdata(cell=1, type='hvb')))
        #self.line14.setText(str(self.d.getdata(cell=1, type='sl')))



    def start_Balancing(self):

        self.respond.setMinimumSize(30, 30)

        if BMS_ControlParameter.getConnectionState():
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

        if BMS_ControlParameter.getConnectionState():
            try:
                BMS_Data.setHv(1)
                self.com1.HV_simulate(self.bus)

                self.respond1.setPixmap(self.i_hv.scaled(30, 30))

                #self.t1.timeout.connect(lambda: threading.Thread(target=self.response(self.t1,self.respond1)).start())
                #self.t1.start(2000)

            except Exception as e:
                self.respond1.setPixmap(self.ie.scaled(30, 30))

                logging.error(traceback.format_exc())
        else:
            print("you need to be connected")

    """def no_pcan(self):
        self.warning_label.setText('NO PCAN ADAPTER IS DETECTED, PLEASE PLUG ADAPTER AND RESTART THE PROGRAM')"""

    def controlFan(self,x):

        if self.enable.isChecked(): #the check box needs to be checked in order to execute any command
            if BMS_ControlParameter.getConnectionState(): #there needs to be connection in order to execute any command
                try:
                    print(x)

                    if (x >= 0) and (x <= 100):
                        self.com1.sendFanControl(self.bus, x)

                except Exception as e:
                    #self.enable.setChecked(False)
                    logging.error(traceback.format_exc())
            else:
                print("you need to be connected")




####################################################################################################################