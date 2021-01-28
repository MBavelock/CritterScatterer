# This library will have a function to check if the Raspberry Pi is connected to a wifi network and a function to connect to a wifi network using a WPS button

import urllib


def CheckWiFiStatus():
  ''' 
  Function will check if currenty connected to an internet network. If connected return 1 else return 0  
            two ways to do this
  1st - open a url to a website (www.google.com) and see it it connects or not
  2nd - run subprocess to check connection status and parse the output
  '''
  # 1st
    try:
        urllib.request.urlopen("http://google.com") # URL is closed as soon as the connection is reached
    except:
        ret 0 # Connection failed
    ret 1 # Connection successfull
  # 2nd
  # https://stackoverflow.com/questions/50388069/check-status-if-raspberry-pi-is-connected-to-any-wifi-network-not-internet-nece
  
  
def ConnecttoWifi_WPS():

