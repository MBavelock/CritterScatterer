# This library will have a function to check if the Raspberry Pi is connected to a wifi network and a function to connect to a wifi network using a WPS button

import urllib
import re
import subprocess
import time


def CheckWiFiStatus(): # NOT TESTED
  ''' 
  Function will check if currenty connected to an internet network. If connected return 1 else return 0  
            two ways to do this
  1st - open a url to a website (www.google.com) and see it it connects or not
  2nd - run subprocess to check if the Pi as an IP address
  '''
  # 1st
  try:
    urllib.request.urlopen("http://google.com") # URL is closed as soon as the connection is reached
  except:
    return 0 # Connection failed
  return 1 # Connection successfull
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
  '''

# Example usage
def main():
  ButtonPressed = True 
  while True:
    if not(CheckWiFiStatus):
      if ButtonPressed:
        ConnectWiFi_WPS()

if __name__ == __main__:
    main()
