from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QLineEdit,
    QApplication,
    QCompleter,
)
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize, Qt
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap


from ui.mainwindow_ui import Ui_MainWindow


import sys
from os import path
import wmi
# from gspread import *

if getattr(sys, "frozen", False):
    dirname = path.join(path.dirname(sys.executable))
elif __file__:
    dirname = path.join(path.dirname(__file__))


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QIcon()
        icon.addFile(path.join(path.dirname(__file__), "icon.ico"), QSize(), QIcon.Normal, QIcon.Off)
        
        self.setWindowIcon(icon)
        
        info = dict()
        w = wmi.WMI()
        bios = dict()
        biosraw = w.Win32_BIOS()[0]
        info['computer_system'] = dict(self.wmiToDict(w.Win32_ComputerSystem()[0]))

        bios = {
            "Manufacturer": biosraw.Manufacturer,
            "Version": biosraw.SMBIOSBIOSVersion,
            "ReleaseDate": biosraw.ReleaseDate,
            "SerialNumber": biosraw.SerialNumber,
            "Description": biosraw.Description,
            "InstallableLanguages": biosraw.InstallableLanguages,
            "LanguageEdition": biosraw.LanguageEdition,
            "Name": biosraw.Name,
            "PrimaryBIOS": biosraw.PrimaryBIOS,
            "Status": biosraw.Status,
            "caption": biosraw.caption,
        }
        self.ui.LbSerialNumber.setText(bios['SerialNumber'])
        self.ui.LbModel.setText(info["computer_system"]["Model"])


    def wmiToDict(self,wmi_object):
        return dict((attr, getattr(wmi_object, attr)) for attr in wmi_object.__dict__['_properties'])

if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec())
