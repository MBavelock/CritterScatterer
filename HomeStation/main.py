#*******************************************#
#           Library Imports - Start         #
#*******************************************#
# General Libraries
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import time
from RFM69 import Radio, FREQ_915MHZ

# WPS Libraries
from WPS import CheckWiFiStatus
from WPS import ConnectWifi_WPS

# Radio Libraries
#from RadioRx import Radio_RX
#from RadioTx import Radio_TX, RadioCalibrate

# Server Libraries


#*******************************************#
#           Library Imports - End           #
#*******************************************#

#*******************************************#
#           Control Panel - Start           #
#*******************************************#
# Blink Delay Times on LED in seconds
BlinkDelay = 0.5

# LED Pins
    # Wifi LED - Indicates connection status to Wifi
WIFI_LED_Pin_Number = 35 # Enter pin
GPIO.setup(WIFI_LED_Pin_Number, GPIO.OUT) # Set pin to output 
WIFI_LED_STATE = 0
GPIO.output(WIFI_LED_Pin_Number, WIFI_LED_STATE) # Set pin Low


    # Radio LED - Indicates connection status to Field Device
Radio_LED_Pin_Number = 33 # Enter pin
GPIO.setup(Radio_LED_Pin_Number, GPIO.OUT) # Set pin to output
Radio_LED_STATE = 0
GPIO.output(Radio_LED_Pin_Number, Radio_LED_STATE) # Set pin Low

    # Power LED - Indicates Home Station is powered on - Might also indicate system errors??
Power_LED_Pin_Number = 31 # Enter pin
GPIO.setup(Power_LED_Pin_Number, GPIO.OUT) # Set pin to output
Power_LED_STATE = 0
GPIO.output(Power_LED_Pin_Number, Power_LED_STATE) # Set pin Low

# Button Pin
    # Button Pin - Used to pair the Home Station to the User's WIFI
WPS_BUTTON_Pin_Number = 7 # Enter pin
GPIO.setup(WPS_BUTTON_Pin_Number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(WPS_BUTTON_Pin_Number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Radio
node_id = 1
network_id = 100
recipient_id = 2
Radio_Power_Level = 90 # Between 0 - 100 (dB)
HomeRadio = Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=False)

# Main
TimeBetweenSystemCheck = 3600

#*******************************************#
#           Control Panel - End             #
#*******************************************#


#*******************************************#
#                   Begin                   #
#*******************************************#
# main.py will begin when system starts up using crontab 
def SystemStartUp():
    # Enable Power LED
    Power_LED_STATE = 1
    GPIO.output(Power_LED_Pin_Number, Power_LED_STATE)
    WIFI_LED_STATE = 0
    # check connectivity to user's WIFI - If not connected Blink the WIFI LED & Stay in while loop waiting for WPS to pair
    while(not(CheckWiFiStatus())):
        if(CheckButton()):
            ConnectWifi_WPS()
        else:
            WIFI_LED_STATE  = not(WIFI_LED_STATE) # Toggle state
            GPIO.output(WIFI_LED_Pin_Number, WIFI_LED_STATE) # change state
            time.sleep(BlinkDelay) # blink LED
    # Wifi is connected - LED is set to solid on
    WIFI_LED_STATE = 1
    GPIO.output(WIFI_LED_Pin_Number, WIFI_LED_STATE)

    # Up to this point tested and working on Home Station
    # Check connectivity to field device - if not connected Blink Radio LED & stay in while loop waiting for connection
    # RC Timer Accuracy 4.3.5 pg41
    # Radio auto calibrated on Power Up
    # Applications enduring large temperature variations, and for which the power supply is never removed, RC calibration can  be  performed  upon  user  request.
    # RegOsc1 (0x0A) - RcCalStart, RcCalDone
    HomeRadio.calibrate_radio()
    # Set the transmit power level
    # Value between 0 and 100
    # RegPaLevel - Outputpower: Output power setting, with 1 dB steps
    HomeRadio.set_power_level(Radio_Power_Level)
    Radio_LED_STATE = 0
    delay = 0.5
    delaycount = 0
    HomeToField = False
    FieldToHome = False
    while(not(HomeToField and FieldToHome)):
        # Send a ping to the Field and wait for a response
        if((delaycount % 5)==0):
            HomeRadioStatus = HomeRadio.send(recipient_id, "Hello", attempts=3, waitTime=100)
            HomeToField = True
        if (HomeRadioStatus):
            RadioReturn = HomeRadio.get_packets()
            for packet in RadioReturn:
                if (packet.data == [52]):
                    HomeRadioStatus = HomeRadio.send(recipient_id, "4", attempts=10, waitTime=100)
                    FieldToHome = True
        time.sleep(delay)
        delaycount += delay
        Radio_LED_STATE  = not(Radio_LED_STATE) # Toggle state
        GPIO.output(Radio_LED_Pin_Number, Radio_LED_STATE) # change state
        #time.sleep(BlinkDelay) # blink LED
    # Radio is connected - LED is set to solid on
    print('Done...')
    Radio_LED_STATE = 1
    GPIO.output(Radio_LED_Pin_Number, Radio_LED_STATE)
        
    # Establish Server/GUI
    '''while(SOME_VARIABLE):
        if(not(SOME_FAULT)):
            print('filler') # TO DO - Setup server here
        else: # Blink Power LED to indicate an Error with Server/GUI setup
            Power_LED_STATE  = not(Power_LED_STATE) # Toggle state
            GPIO.output(Power_LED_Pin_Number, Power_LED_STATE) # change state
            time.sleep(BlinkDelay) # blink LED
    # Wifi is connected - LED is set to solid on
    Power_LED_STATE = 1
    GPIO.output(Power_LED_Pin_Number, Power_LED_STATE)
    # Return the time at which the system setup occured
    '''
    return time.time()
       
def CheckButton():
    if GPIO.input(WPS_BUTTON_Pin_Number) == GPIO.LOW:
        return 1
    return 0

# Function to Recieve Data
def Radio_RX():
    # Clear payload
    RXpayload = []
    # Add elements based on length of data
    for i in range(0,len(packet.data)):
        RXpayload.append(i)
        RXpayload[i] = packet.data[i]
    return RXpayload


def main():
    # Init system
    TimeOfLastCheck = SystemStartUp()
    # Loop forever
    while(True):
        # Run Init again after 3600 seconds time has passed to check for system errors
        if(time.time() - TimeOfLastCheck >= TimeBetweenSystemCheck):
            # Init system
            TimeOfLastCheck = SystemStartUp()
        
        # Wait until Field sends info
        # Parse packets into text file/images maybe
        
        # 
        
        

if __name__ == '__main__':
    main()















