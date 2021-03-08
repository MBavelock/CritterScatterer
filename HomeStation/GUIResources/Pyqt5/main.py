#-------------------------------------------------------------------------#
#University of Massachusetts Darmouth, College of Engineering             #
#Class:     ECE 457/458                                                   #
#Team:      ECE-3 Critter Scatterer                                       #
#Author:    Adam Cunningham                                               #
#Purpose:   This main python program holds all the information for the GUI#
#           to function properly.                                         #
#Credit:    z3ntu - QtWaitingSpinner                                      #
#-------------------------------------------------------------------------#

import sys
import pathlib
import urllib.request
from os import path
from PyQt5.uic import loadUi
from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from waitingspinnerwidget import QtWaitingSpinner
from functools import partial
from downloader import Downloader

#Main window
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("UIs/main.ui", self) #Load the main UI created with Qt Designer
        self.ButtonIcons()

        #When options is clicked, switch to the options window
        self.Options.clicked.connect(partial(WindowSwitch.Switch, name = 'Options'))
        #When events is clicked, switch to the events window
        self.Events.clicked.connect(partial(WindowSwitch.Switch, name = 'Events'))

    def ButtonIcons(self): 
        #Set icon and size for options button
        self.Options.setIcon(QIcon("Images/Options Button.svg"))
        self.Options.setIconSize(QSize(170,170))

        #Set icon and size for events button
        self.Events.setIcon(QIcon("Images/Events Button.svg"))
        self.Events.setIconSize(QSize(170,170))

        #Set icon and size for on/off button
        self.OnOff.setIcon(QIcon("Images/Off Button.svg"))
        self.OnOff.setIconSize(QSize(170,170))

#Options window
class Options(QDialog):
    def __init__(self, parent=None):
        super(Options, self).__init__(parent)
        loadUi("UIs/options.ui", self)  #Load the options UI created with Qt Designer

        #When go back is clicked, switch to the main menu
        self.goBack.clicked.connect(partial(WindowSwitch.Switch, name = 'Main'))
        #When events is clicked, switch to the events menu
        self.optEvents.clicked.connect(partial(WindowSwitch.Switch, name = 'Events'))

#Event window
class Events(QDialog):
    def __init__(self, parent=None):
        super(Events, self).__init__(parent)
        loadUi("UIs/events.ui", self)   #Load the events UI created with Qt Designer

        #When go back is clicked, switch to the main menu
        self.goBack.clicked.connect(partial(WindowSwitch.Switch, name = 'Main'))
        #When options is clicked, switch to the options window
        self.evntOptions.clicked.connect(partial(WindowSwitch.Switch, name = 'Options'))

        self.SpinnerInit()
        self.RefreshLayout.addWidget(self.spinner)  #Add spinner to column 1 of the RefreshGrid
        self.refresh.clicked.connect(self.run_Downloader)    #If refresh button is clicked, start downloader

    def run_Downloader(self):   #Call to download method
        Downloader().Download(self.spinner)

    #Method to initialize the waiting spinner
    def SpinnerInit(self):
        self.spinner = QtWaitingSpinner(self, centerOnParent=False)   #Create new spinner
        self.spinner.setRoundness(60)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(60)
        self.spinner.setNumberOfLines(15)
        self.spinner.setLineLength(6)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(7)
        self.spinner.setRevolutionsPerSecond(3)
        self.spinner.setColor(QColor(7, 47, 157))
        self.spinner.move(30,450)

    #Toggle the status of the waiting spinner (on or off)
    def ToggleSpinner(self):
        if self.spinner.isSpinning():
            self.spinner.stop()
        else:
            self.spinner.start()

#Event Alt Window (Used to download event file when not found)
class EventAlt(QMainWindow):
    def __init__(self):
        super(EventAlt, self).__init__()
        loadUi("UIs/eventalt.ui", self)     #Load the eventalt UI created with Qt Designer

        #When go back is clicked, switch to the main menu
        self.goBack.clicked.connect(partial(WindowSwitch.Switch, name = 'Main'))

        self.SpinnerInit()
        self.verticalLayout.insertWidget(3, self.spinner2, 0, Qt.AlignHCenter)  #Add spinner to row 3 of the verticallayout
        self.download.clicked.connect(self.run_Downloader)  #If download button is clicked, start downloader

    def run_Downloader(self):   #Call to download method
        Downloader().Download(self.spinner2)
        WindowSwitch().Switch(name = 'Events')

    #Method to initialize the waiting spinner
    def SpinnerInit(self):
        self.spinner2 = QtWaitingSpinner(self, centerOnParent=False)   #Create new spinner
        self.spinner2.setRoundness(60)
        self.spinner2.setMinimumTrailOpacity(15.0)
        self.spinner2.setTrailFadePercentage(60)
        self.spinner2.setNumberOfLines(15)
        self.spinner2.setLineLength(6)
        self.spinner2.setLineWidth(5)
        self.spinner2.setInnerRadius(7)
        self.spinner2.setRevolutionsPerSecond(3)
        self.spinner2.setColor(QColor(7, 47, 157))

#Class method to switch windows using the stacked widget
class WindowSwitch():
    def Switch(self, name):
        if name == 'Main':
            stack.setCurrentIndex(0)    #Main window index is 0
        elif name == 'Options':
            stack.setCurrentIndex(1)    #Options window index is 1
        elif name == 'Events':
            if path.exists("C:/ECE 458/GUI/test.txt"):
                stack.setCurrentIndex(2)    #Events window index is 2
            else:
                stack.setCurrentIndex(3)    #Events alt window index is 3

#Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stack = QtWidgets.QStackedWidget()  #Create stacked widget to hold all windows
    home = MainWindow()
    stack.addWidget(home)
    options = Options()
    stack.addWidget(options)
    events = Events()
    stack.addWidget(events)
    eventalt = EventAlt()
    stack.addWidget(eventalt)
    stack.setMinimumSize(781, 481)
    stack.show()

#On program exit, print "Exiting" to console
try:
    sys.exit(app.exec_())
except:
    print("Exiting")