# This library will have a function to check if the Raspberry Pi is connected to a wifi network and a function to connect to a wifi network using a WPS button

import urllib
import re
import subprocess
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def CheckWiFiStatus(): # tested - 2nd method works best
  ''' 
  Function will check if currenty connected to an internet network. If connected return 1 else return 0  
            two ways to do this
  1st - open a url to a website (www.google.com) and see it it connects or not
  2nd - run subprocess to check if the Pi as an IP address
  '''
  # 1st
  #try:
  #  urllib.request.urlopen("http://google.com") # URL is closed as soon as the connection is reached
  #except:
  #  return 0 # Connection failed
  #return 1 # Connection successfull

  # 2nd - Source (https://www.raspberrypi.org/forums/viewtopic.php?t=77277)
  ret = subprocess.check_output(["ifconfig", "wlan0"]).decode("utf-8")
  reg = re.search("inet (\d+\.\d+\.\d+\.\d+)", ret)
  if reg is None:
      return False
  else:
      return True
  
  
def ConnectWifi_WPS(): # NOT TESTED
  '''
  Funtion should be called when the button designated as our WPS is pressed
  Function will connect to the WIFI network which has has it's routers WPS pressed
  (Source = https://www.raspberrypi.org/forums/viewtopic.php?t=77277)
  '''
  # run until we are sure that WiFi is connected and running
  #while not(IPStatus):
  # no IP address, so start looking for WPS-PBC network
  # scan networks on interface wlan0, to see some nice networks
  subprocess.check_output(["wpa_cli", "-i", "wlan0", "scan"])
  time.sleep(1)
  # get and decode results
  wpa = subprocess.check_output(["wpa_cli", "-i", "wlan0", "scan_results"]).decode("UTF-8")
  # parse response to get MAC address of router that has WPS-PBC state
  active_spot_reg = re.search("(([\da-f]{2}:){5}[\da-f]{2})(.*?)\[WPS-PBC\]", wpa)
  # check if we found any
  if not(active_spot_reg is None):
    if active_spot_reg.group(1):
      #connect via wps_pbc
      subprocess.check_output(["wpa_cli", "-i", "wlan0", "wps_pbc", active_spot_reg.group(1)])
