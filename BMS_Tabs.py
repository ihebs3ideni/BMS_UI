''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''


import threading

from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QTabWidget)

import BMS_ControlParameter as p
import BMS_Errors
import BMS_Generals
import BMS_Table


####################################################################################################################

class MyTabsWidget(QWidget):
    def __init__(self,bus,bms_com):
        super().__init__()
        self.layout = QVBoxLayout(self)

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
        thread1 = threading.Thread(target=self.create_tab1(bus, bms_com))
        thread1.setDaemon(True)
        thread1.start()



        # Create second tab

        thread2 = threading.Thread(target=self.create_tab2())
        thread2.setDaemon(True)
        thread2.start()

        #create third tab

        thread3 = threading.Thread(target=self.create_tab3())
        thread3.setDaemon(True)
        thread3.start()

        #create_forth_tab
        '''thread4 = threading.Thread(target=self.create_tab4(bus,data,bms_com))
        thread4.setDaemon(True)
        thread4.start()'''

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def create_tab1(self,bus,bms_com):
        self.tab1.layout = QVBoxLayout(self)

        self.first_tab = BMS_Generals.GeneralsTab(bus, bms_com)
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

        threading.Thread(target= self.first_tab.sld.valueChanged.connect(self.first_tab.lcd.display)).start()

        self.tab1.layout.addWidget(self.first_tab)

        self.tab1.setLayout(self.tab1.layout)
        print('tab 1 done')

    def create_tab2(self):
        self.tab2.layout = QVBoxLayout(self)

        self.second_tab = BMS_Table.CellTab(0, p.numberOfCells)
        # clear button
        self.second_tab.clearButton.clicked.connect(lambda: self.second_tab.clear(self.second_tab.tableWidget, 0, p.numberOfCells))
        # save Button
        self.second_tab.saveButton.clicked.connect(self.second_tab.save_file)
        # refreshButton
        self.second_tab.startRefreshButton.clicked.connect(lambda:  threading.Thread(target= self.second_tab.refresh(
                                                                self.second_tab.startRefreshButton, self.second_tab.voltageCheckBox,
                                                            self.second_tab.temperatureCheckBox, self.second_tab.tableWidget,p.numberOfCells))
                                                           .start())

        # slider bar
        self.second_tab.slider.valueChanged.connect(self.second_tab.v_change)
        self.second_tab.refreshRate.returnPressed.connect(self.second_tab.lbl)

        self.tab2.layout.addWidget(self.second_tab)

        self.tab2.setLayout(self.tab2.layout)
        print('tab 2 done')

    def create_tab3(self):
        self.tab3.layout = QVBoxLayout(self)
        self.third_tab = BMS_Errors.ErrorTab()
        # self.third_tab.error_dar()
        '''t1 = threading.Thread(target=self.third_tab.update_me())
        t1.setDaemon(True)
        t1.start()'''

        self.tab3.layout.addWidget(self.third_tab)

        self.tab3.setLayout(self.tab3.layout)
        print('tab 3 done')

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