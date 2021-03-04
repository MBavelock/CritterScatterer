import sys
import urllib.request
from PyQt5.uic import loadUi
from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QProgressBar
from PyQt5.QtGui import QColor
from waitingspinnerwidget import QtWaitingSpinner

class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super(Downloader, self).__init__()
        self.progressBar = QProgressBar(self)   #Create progress bar
        self.progressBar.setGeometry(25, 45, 210, 30)   #Set progress bar size

        self.spinner = QtWaitingSpinner(self, centerOnParent=False) #Create spinner instance that doesn't center on screen

        self.spinner.setRoundness(60)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(60)
        self.spinner.setNumberOfLines(15)
        self.spinner.setLineLength(6)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(7)
        self.spinner.setRevolutionsPerSecond(3)
        self.spinner.setColor(QColor(7, 47, 157))
        self.spinner.move(70,120)

        self.setGeometry(310, 310, 280, 170)    #Set main window size

        self.button = QPushButton('Start', self)
        self.button.move(50, 100) 
        self.button.clicked.connect(self.Download) #When button is clicked, call Download

        self.grid = QtWidgets.QGridLayout() #Create grid layout to hold button and spinner
        self.grid.addWidget(self.button, 0,0)   #Add button to row 0 column 0
        self.grid.addWidget(self.spinner, 0,1)  #Add spinner to row 0 column 1
        self.setLayout(self.grid)


    def DownProgress(self, blocknum, blocksize, totalsize): 
  
        data = blocknum * blocksize #Calculate data size
  
        if totalsize > 0: 
            self.spinner.start()
            download_percentage = data * 100 / totalsize 
            self.progressBar.setValue(download_percentage) 
            QApplication.processEvents()    #Process events from the current call

    def Download(self): 
  
        url = 'https://speed.hetzner.de/100MB.bin' #URL to download from 

        filename = 'test.txt'
        path = 'C:/ECE 458/GUI/' + filename #Path to download to
        urllib.request.urlretrieve(url,path, self.DownProgress)  #Download using urllib, call DownProgress
        self.spinner.stop()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Downloader()
    w.show()
    sys.exit(app.exec_())