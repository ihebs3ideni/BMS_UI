''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''

import logging
import os
import pathlib
import sys
import threading
import traceback

import can
import matplotlib.animation as animation
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QHBoxLayout,
                             QVBoxLayout, QWidget, QLabel)
from matplotlib import pyplot as plt
from matplotlib import style

import BMS_Communications
import BMS_ControlParameter
import BMS_Data
import BMS_Tabs

##################################### Graphical Design #####################################################

connectingClicked = 0
alreadyClicked = 0
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

class Nanni_Main_Window(QMainWindow):

    def __init__(self,bus,bms_com):
        super().__init__()

        #self.data = data
        self.counter=0
        self.com = bms_com
        self.bus = bus

        self.tabs_widget = BMS_Tabs.MyTabsWidget(self.bus, self.com)

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

        exit.triggered.connect(self.quit_trigger)
        save.triggered.connect(self.tabs_widget.second_tab.save_file)
        new.triggered.connect(self.new_Widget)
        connect.triggered.connect(self.Connecting) #check it out
        disconnect.triggered.connect(self.disconnecting)
        #refresh.triggered.connect(self.updateComPorts) #check it out

        v_graph.triggered.connect(lambda: self.thread_plot('v'))
        t_graph.triggered.connect(lambda: self.thread_plot('t'))



        self.setWindowTitle("Nanni\'s little helper")
        self.setWindowIcon(QIcon('C:/Users/iheb/BMS_UI/icons/main_logo.png'))
        self.resize(1000, 500)
        self.show()

    def quit_trigger(self):
        qApp.quit()




    def anim_v(self):
        fig = plt.figure('Voltage Graph',figsize= (12,5))
        plt.title('epic graph')
        plt.ylabel('Voltages (mV)')
        plt.xlabel('cells')

        #data= self.data

        x = np.array([0]*140)
        y = np.array([0]* 140)
        for i in range(140):
            x[i]= (i+1)
            y[i] = BMS_Data.getdata(i,'v')


        # data = np.column_stack([np.linspace(0, yi, 50) for yi in y])

        rects = plt.bar(x, y, color='dodgerblue')
        line, = plt.plot(x, y, color='red')
        plt.grid(axis='y')
        plt.ylim(2700)

        def animate(index):

            #data.fillData(141, 'v')
            ys = np.array([0.0]*140)

            for j in range(140):

                ys[j] = BMS_Data.getdata(j,'v')


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

        #data = self.data

        x = np.arange(1,61,1)
        y = []
        for i in range(80):
            if (i+1)%4!=1:
                y.append(BMS_Data.getdata(i, 't')/10)



        # data = np.column_stack([np.linspace(0, yi, 50) for yi in y])

        rects1 = plt.bar(x, y, color='tomato')
        line1, = plt.plot(x, y, color='k')
        plt.grid(axis='y')

        def animate(i):
            #data.fillData(81, 't')
            ys = []

            for j in range(80):
                if j%4 != 1:

                    ys.append(BMS_Data.getdata(j, 't')/10)

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



    def new_Widget(self):
        self.newWidget = BMS_Tabs.MyTabsWidget(self.bus, self.com)
        self.newWidget.setWindowTitle('Nanni\'s little helper  1.0')
        self.newWidget.setWindowIcon(QIcon('C:/Users/iheb/BMS_UI/icons/main_logo.png'))
        self.newWidget.setGeometry(600,400,1000, 500)
        self.newWidget.show()


    def Connecting(self):
        global connectingClicked, alreadyClicked
        connectingClicked += 1
        alreadyClicked += 1
        if connectingClicked == 1:
            self.tabs_widget.first_tab.enable.setChecked(False)
            BMS_ControlParameter.setLogDataControl(True)
            logdata = threading.Thread(target=self.timeLogData())
            logdata.start()
        try:
            self.com.starting(self.bus)

            BMS_ControlParameter.setConnectionState(True)
            #self.tabs_widget.second_tab.startRefresh(self.tabs_widget.second_tab.tableWidget, BMS_ControlParameter.numberOfCells)
        except TypeError:
            print('error connecting')



    def disconnecting(self):
        try:
            self.com.terminate()
            BMS_ControlParameter.setConnectionState(False)
            BMS_ControlParameter.setLogDataControl(False)
            global connectingClicked
            connectingClicked = 0
            self.tabs_widget.second_tab.stopRefresh(self.tabs_widget.second_tab.tableWidget,
                                                     BMS_ControlParameter.numberOfCells)

        except TypeError:
            print('error disconnecting')

    def timeLogData(self):
        global alreadyClicked
        path = str(os.getcwd()) + "\\logdata"  # create a new directory path
        pathlib.Path(path).mkdir(exist_ok=True)  # create the directory if it doesn't exist

        if alreadyClicked == 1:
            file = BMS_ControlParameter.createLogDataFile()  # create a file for the logdata
            BMS_Data.logData(file)# create first logdata
            timer = QTimer()
            timer.timeout.connect(lambda: BMS_Data.logData(file))
            timeToLogData = 10*1000 #5min
            timer.start(timeToLogData)
            import atexit
            atexit.register(timer.stop)

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

   ###################################################################################################


class NoPcan(QMainWindow):
    def __init__(self):
        super().__init__()
        BMS_ControlParameter.setBusStatus(False)
        self.window = QWidget(self)
        self.setCentralWidget(self.window)

        self.setWindowIcon(QIcon('C:/Users/iheb/BMS_UI/icons/error.png'))
        self.window.setGeometry(600, 400, 500, 200)
        self.setWindowTitle("Error Message")
        self.l = QLabel("No pcan adapter is detected, please check the connection and restart the app, thanks :) ")

        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.l)
        v_box.addStretch()

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.window.setLayout(h_box)

"""def endLog(start, file):
    BMS_ControlParameter.incrimentTimeLog()
    end= time.time()
    log= end-start
    
    print(end-start)
    file.write('this session took %f to execute\n' %log  )"""


########################################## Main #######################################################
def main_BMS():
    global connectingClicked
    connectingClicked = 0
    try:
        bms_com = BMS_Communications.Communications()
        style.use('seaborn')  # style for matplotlib graph
        try:

            bus = bms_com.initialize_bus()
            #bus=[1,2,3]
            #atexit.register(bus)


            app = QApplication(sys.argv)
            a_window = Nanni_Main_Window(bus, bms_com)
            a_window.show()

            gui_thread = threading.Thread(target=sys.exit(app.exec_()))
            gui_thread.setDaemon(True)
            gui_thread.start()

        except can.CanError:
            print('No Pcan adapter is connected')
            app = QApplication(sys.argv)
            a_window = NoPcan()
            a_window.show()
            print('bus is okay: ', BMS_ControlParameter.getBusStatus())
            gui_thread = threading.Thread(target=sys.exit(app.exec_()))
            gui_thread.setDaemon(True)
            gui_thread.start()
        '''finally:
            bus.shutdown()'''

    except Exception as e:
        logging.error(traceback.format_exc())



if __name__ == "__main__":
    main_BMS()



