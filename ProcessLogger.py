from PyQt5 import QtCore, QtGui, QtWidgets
import psutil
import csv
import os

#class MyProcess:
#    processName = str()
#    processExePath = str()
#    processPid = int()
#
#    def __init__(self, processName="", processExePath="", processPid=0):
#        self.processName = processName
#        self.processExePath = processExePath
#        self.processPid = processPid


class ProcessLogger:
    def __init__(self):
        print("init ProcessLogger object")
        self.process_list = set()

    def update_process_list(self):
        print("Updating process list")
        for ps in psutil.process_iter():
            attrs = ps.as_dict(attrs=["name", "exe", "pid"])
            ret = (attrs["name"], attrs["exe"], attrs["pid"])
            self.process_list.add(ret)
        return self.process_list


class Ui_MainWindow(object):
    logger = ProcessLogger()
    #processObjectsList = []
    refresh_rate = 1000

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 758)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.processListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.processListWidget.setGeometry(QtCore.QRect(40, 50, 921, 581))
        self.processListWidget.setObjectName("processorListWidget")
        self.listSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.listSizeLabel.setGeometry(QtCore.QRect(220, 20, 61, 16))
        self.listSizeLabel.setObjectName("listSizeLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(54, 640, 91, 20))
        self.label_2.setObjectName("label_2")
        self.refreshMSLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.refreshMSLineEdit.setGeometry(QtCore.QRect(150, 640, 113, 22))
        self.refreshMSLineEdit.setObjectName("refreshMSLineEdit")
        self.refreshMSSetPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshMSSetPushButton.setGeometry(QtCore.QRect(270, 640, 51, 28))
        self.refreshMSSetPushButton.setObjectName("refreshMSSetPushButton")
        self.exportPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportPushButton.setGeometry(QtCore.QRect(860, 670, 93, 28))
        self.exportPushButton.setObjectName("exportPushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(490, 640, 101, 16))
        self.label_3.setObjectName("label_3")
        self.exportFileNameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.exportFileNameLineEdit.setGeometry(QtCore.QRect(692, 640, 261, 22))
        self.exportFileNameLineEdit.setObjectName("exportFileNameLineEdit")
        self.fileDialogPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileDialogPushButton.setGeometry(QtCore.QRect(590, 640, 93, 28))
        self.fileDialogPushButton.setObjectName("fileDialogPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1009, 26))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuMenu.addAction(self.actionQuit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # my message handler connection
        self.menuMenu.triggered.connect(self.quitApp)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_process_list_widgit)
        self.timer.start(self.refresh_rate)
        self.exportPushButton.clicked.connect(self.export_processes_as_csv)
        self.refreshMSSetPushButton.clicked.connect(self.adjust_refresh_rate)
        self.fileDialogPushButton.clicked.connect(self.csv_file_dialog_open)
        self.exportFileNameLineEdit.setText("./output.csv")

        ##disable timer adjustment as this hasn't been implemented yet
        self.refreshMSSetPushButton.setDisabled(True)
        self.refreshMSLineEdit.setDisabled(True)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Logger QT"))
        self.listSizeLabel.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "Number of processes logged:"))
        self.label_2.setText(_translate("MainWindow", "Refresh in ms:"))
        self.refreshMSSetPushButton.setText(_translate("MainWindow", "Set"))
        self.exportPushButton.setText(_translate("MainWindow", "Export"))
        self.label_3.setText(_translate("MainWindow", "Export file path:"))
        self.fileDialogPushButton.setText(_translate("MainWindow", "Choose"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def update_process_list_widgit(self):
        processList = self.logger.update_process_list()
        self.processListWidget.clear()
        text = []
        for proc in processList:
            text.append("{} - {} - {}".format(proc[0],proc[1], proc[2]))
        self.processListWidget.addItems(text)
        self.listSizeLabel.setText(str(len(processList)))

    def export_processes_as_csv(self):
        filename = self.exportFileNameLineEdit.text()
        print("Writing csv file to {}".format(filename))
        with open(filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=["Name", "Path", "Pid"])
            csv_writer.writeheader()
            for proc in self.logger.process_list:
                p_dict = {"Name": proc[0], "Path": proc[1], "Pid": proc[2]}
                csv_writer.writerow(p_dict)
            csv_file.close()

    def csv_file_dialog_open(self):
        self.exportFileNameLineEdit.setText(os.path.abspath(QtWidgets.QFileDialog.getSaveFileName()[0]))

    def adjust_refresh_rate(self, rate_in_ms):
        print("adjusting refresh rate in ms to {}".format(rate_in_ms))
        # todo: implement changing update frequency

    def quitApp(self):
        exit(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())