''' Author: Saidani Iheb
    Season: 2018-2019
    Project: Nanni's Little Helper 2.0
    '''



import csv
import logging
import os
import threading
import traceback

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout,
                             QVBoxLayout,
                             QPushButton, QWidget, QTableWidget, QCheckBox, QSlider, QTableWidgetItem,
                             QAbstractItemView, QLabel, QLineEdit)

import BMS_ControlParameter
import BMS_Data


#####################################################################################################################


class CellTab(QWidget):

    def __init__(self, rowCount , columnCount):
        super().__init__()

        self.tableWidget = QTableWidget(rowCount, columnCount)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  #makes table read only

        for i in range(columnCount):
            self.tableWidget.setColumnWidth(i,90)
        #adjuct cells to the size of the contents
        #self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #self.tableWidget.resizeColumnsToContents()
        col_headers = []
        for i in range(columnCount):
            a = 'cell:' + str(i + 1)
            col_headers += [a]
        self.tableWidget.setHorizontalHeaderLabels(col_headers)



        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1000)
        self.slider.setMaximum(15000)
        self.slider.setTickInterval(1000)

        self.slider.setTickPosition(QSlider.TicksBelow)

        self.refreshRate = QLineEdit('1000ms')
        self.refreshRate.setFixedWidth(60)

        self.clearButton = QPushButton("Clear")
        self.startRefreshButton = QPushButton("Start Refresh")
        self.saveButton = QPushButton("Save")

        self.voltageCheckBox = QCheckBox("Voltage")
        self.temperatureCheckBox = QCheckBox("Temperature")
        self.voltageCheckBox.setChecked(True)
        self.temperatureCheckBox.setChecked(True)







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
        h_box.addWidget(self.refreshRate)
        h_box.addWidget(self.slider)
        h_box.addWidget(self.startRefreshButton)
        h_box.addWidget(self.saveButton)
        h_box.addWidget(self.clearButton)

        h_box.addStretch()

        h_box.addWidget(self.voltageCheckBox)
        h_box.addWidget(self.temperatureCheckBox)
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




    def clear(self,table,rowCount,columnCount): #methode that clears the table cells

        table.clearContents()
        table.setColumnCount(columnCount)
        table.setRowCount(rowCount)


    def refresh(self, button, v_check, t_check, table, columnCount): #methode that times the updating of the table
        sender = self.sender()
        #timer
        self.timer = QTimer()
        #connectTimer

        if sender.text() == 'Start Refresh' and BMS_ControlParameter.getConnectionState():
            button.setText('Stop Refresh')

            threading.Thread(target= self.timer.timeout.connect(lambda: self.thread_refill1(v_check, t_check, table, columnCount, self.timer))).start()
            #t1.setDaemon(False)

        elif sender.text() == 'Stop Refresh':
            button.setText('Start Refresh')

            threading.Thread(target=self.timer.timeout.connect(lambda: self.thread_refill2(v_check, t_check, table, columnCount, self.timer))).start()


            #t2.setDaemon(False)

            print('not refreshing')
        #startTimer
        refresh_time = self.getRefreshTime()
        self.timer.start(refresh_time)

    def thread_refill1(self,v_check, t_check, table, columnCount, timer):
        t1 = threading.Thread(target=self.tab_refill(v_check, t_check, table, columnCount, True, timer))
        t1.setDaemon(True)
        t1.start()

    def thread_refill2(self,v_check, t_check, table, columnCount,timer):
        t2 = threading.Thread(target=self.tab_refill(v_check, t_check, table, columnCount, False, timer))
        t2.setDaemon(True)
        t2.start()

    def tab_refill (self,v_checkBox,t_checkBox, table, columnCount,ok, timer): #methode that refill the cell table
        try:
            if ok:
                """threading.Thread(target=self.data.fillData(140, 'v')).start()
                threading.Thread(target=self.data.fillData(80, 't')).start()"""
                self.av =0 # averageVoltage
                if v_checkBox.isChecked():
                    table.insertRow(0)
                    for i in range(columnCount):
                        v = self.getCells(i,'v')

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

                    for i in range(columnCount-60):
                        t= self.getCells(i,'t')
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


    def getCells(self,cell,type): #methode that get's the cell data from the Data class

        #self.data.fillVData(num = 140, type='v')

        if type =='v':


            return BMS_Data.getdata(cell,'v')/1000

        elif type == 't':

            return BMS_Data.getdata(cell,'t')/10

    def getErrors(self, cell, type): #methode that get's the errors from the Data class
        #self.dataError = BMS_Data.Data(140, bus=self.bus, com=self.com)
        #threading.Thread(target= BMS_Data.setErrors(140, 'c')).start()
        threading.Thread(target=BMS_Data.setErrors(140, 'v')).start()
        threading.Thread(target=BMS_Data.setErrors(80, 't')).start()




        return not(BMS_Data.getErrors(cell, type))



    def v_change(self): #methode that tracks the value changes of the Slider therefore for the time of refresh
        my_value = str(self.slider.value())
        self.refreshRate.setText(my_value+'ms')

    def lbl(self): #methoe that overwrites the value of the slider when manually written in the label
        if int(self.refreshRate.text()) >= 1000 and  int(self.refreshRate.text())<=15000:
            self.slider.setValue(int(self.refreshRate.text()))

        elif self.refreshRate.text() is '':
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

    """def save_file(self):
        filename = QFileDialog.getSaveFileName(self.tableWidget, 'Save xls', os.getenv('HOME') , ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        self.add2(sheet)
        wbk.save(filename)

    def add2(self, sheet):
        for currentColumn in range(self.tableWidget.columnCount()):
            for currentRow in range(self.tableWidget.rowCount()):
                try:
                    teext = str(self.tableWidget.item(currentRow, currentColumn).text())
                    sheet.write(currentRow, currentColumn, teext)
                except AttributeError:
                    pass"""

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