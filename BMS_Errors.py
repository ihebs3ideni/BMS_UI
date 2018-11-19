''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''
import threading

import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QRadioButton, QHBoxLayout,
                             QVBoxLayout,
                             QWidget, QGridLayout, QLabel)

import BMS_ControlParameter as p
import BMS_Data


####################################################################################################################

class ErrorTab(QWidget):
    def __init__(self):
        super().__init__()
       # self.error_dar("Voltage Error:",self.checkVerror(), self.checkTerror())

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
        '''threading.Thread(target=self.data.fillData(150,'v')).start()
        threading.Thread(target=self.data.fillData(80, 't')).start()
        threading.Thread(target=self.data.fillData(150, 'c')).start()'''


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
                if not(self.getErrors(value,'v')): #check errors for every cell while creating the radiobutton
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
                if not(self.getErrors(value,'t')):
                    self.b.setChecked(True)

                else:
                    self.b.setChecked(False)

                if value %4 ==1:
                    self.b.setChecked(True)

                self.grid.addWidget(self.b, *position)

            h_box2.addLayout(self.grid)
            return h_box2



        '''elif types == 'c':
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
            if not(self.getErrors(1,'c')):
                self.b1.setChecked(True)
            else:
                self.b2.setChecked(True)

            return h_box'''



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









    def getErrors(self, cell , type): #methode that returns the errors from the Data class


        threading.Thread(target=BMS_Data.setErrors(p.numberOfCells, 'v')).start()
        threading.Thread(target=BMS_Data.setErrors(p.numberOfTempSensors, 't')).start()


        if (type == 'v'):
            return BMS_Data.getErrors(cell-1,'v')
        if (type == 't'):
            return BMS_Data.getErrors(cell-1,'t')













####################################################################################################################