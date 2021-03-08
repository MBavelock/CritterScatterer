import sys
import urllib.request
from PyQt5.QtWidgets import *
from waitingspinnerwidget import QtWaitingSpinner
from functools import partial

class Downloader():
    def __init__(self):
        super(Downloader, self).__init__()

    #Calculate download progress and show spinner during that time
    def DownProgress(self, blocknum, blocksize, totalsize):
        data = blocknum * blocksize #Calculate data size for progress bar
        if totalsize > 0: 
            download_percentage = data * 100 / totalsize 
            QApplication.processEvents()    #Process events from the current call

    def Download(self, spinner): 
        url = 'https://speed.hetzner.de/100MB.bin' #URL to download from
        filename = 'test.txt'
        path = 'C:/ECE 458/GUI/' + filename #Path to download to

        spinner.start()
        urllib.request.urlretrieve(url, path, self.DownProgress)  #Download using urllib, call DownProgress with reporthook of urlretrieve
        spinner.stop()