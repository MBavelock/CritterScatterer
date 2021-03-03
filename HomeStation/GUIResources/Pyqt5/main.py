import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication

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

    def EventsToOptions(self):
        widget.setCurrentIndex(1)   #Options menu is index 2 in stack

    def GoBack(self):
        widget.setCurrentIndex(0)   #Mainwindow is index 0 in stack



# main
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