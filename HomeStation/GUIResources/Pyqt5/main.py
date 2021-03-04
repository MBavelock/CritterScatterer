import sys
import urllib.request
from PyQt5.uic import loadUi
from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QProgressBar
from PyQt5.QtGui import QColor
from waitingspinnerwidget import QtWaitingSpinner

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("UIs/main.ui", self)
        self.Options.clicked.connect(self.SwitchOptions)    #When options button is clicked, call SwitchOptions
        self.Events.clicked.connect(self.SwitchEvents)      #When events button is clicked, call SwitchEvents

    def SwitchOptions(self):
        widget.setCurrentIndex(1)   #Options menu is index 1 in stack

    def SwitchEvents(self):
        widget.setCurrentIndex(2)   #Events menu is index 2 in stack


class OptionsMenu(QDialog):
    def __init__(self):
        super(OptionsMenu, self).__init__()
        loadUi("UIs/options.ui", self)
        self.goBack.clicked.connect(self.GoBack)            #When goBack button is clicked, call GoBack
        self.optEvents.clicked.connect(self.OptionsToEvents)    #When Events button is clicked, switch to Events dialog

    def OptionsToEvents(self):
        widget.setCurrentIndex(2)   #Events menu is index 2 in stack

    def GoBack(self):
        widget.setCurrentIndex(0)   #Mainwindow is index 0 in stack


class EventsMenu(QDialog):
    def __init__(self):
        super(EventsMenu, self).__init__()
        loadUi("UIs/events.ui", self)
        self.goBack.clicked.connect(self.GoBack)            #When goBack button is clicked, call GoBack
        self.evntOptions.clicked.connect(self.EventsToOptions)    #When Options button is clicked, switch to Options dialog
        self.SpinnerInit()
        self.RefreshGrid.addWidget(self.spinner, 0, 1, 1, 2)  #Add spinner to column 1 of the RefreshGrid
        self.refresh.clicked.connect(self.Download)    #If refresh button is clicked, start downloader

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

    def ToggleSpinner(self):
        if self.spinner.isSpinning():
            self.spinner.stop()
        else:
            self.spinner.start()

    def EventsToOptions(self):
        widget.setCurrentIndex(1)   #Options menu is index 2 in stack

    def GoBack(self):
        widget.setCurrentIndex(0)   #Mainwindow is index 0 in stack

    def DownProgress(self, blocknum, blocksize, totalsize): 
        data = blocknum * blocksize #Calculate data size

        if totalsize > 0: 
            QApplication.processEvents()    #Process events from the current call

    def Download(self): 
  
        url = 'https://speed.hetzner.de/100MB.bin' #URL to download from 

        filename = 'test.txt'
        path = 'C:/ECE 458/GUI/' + filename #Path to download to
        self.ToggleSpinner()
        urllib.request.urlretrieve(url, path, self.DownProgress)  #Download using urllib, call DownProgress
        self.ToggleSpinner()

    


#Main
if __name__ == "__main__":
    app = QApplication(sys.argv)        #Initialize GUI
    widget = QtWidgets.QStackedWidget() #Create stacked widget to store windows in an array (0,1,2...)
    mainwindow = MainWindow()           #Initialize mainwindow
    widget.addWidget(mainwindow)        #Add mainwindow widget to widget stack
    optionsmenu = OptionsMenu()         #Initialize optionsmenu
    widget.addWidget(optionsmenu)       #Add optionsmenu widget to widget stack
    eventsmenu = EventsMenu()           #Initialize eventsmenu
    widget.addWidget(eventsmenu)        #Add eventsmenu widget to widget stack
    widget.setFixedHeight(481)          #Set mainwindow height
    widget.setFixedWidth(781)               #and width
    widget.show()                       #Show the widget


try:
    sys.exit(app.exec_())
except:
    print("Exiting")