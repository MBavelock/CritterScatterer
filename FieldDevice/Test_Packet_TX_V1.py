#https://rpi-rfm69.readthedocs.io/en/latest/example_basic.html#simple-transceiver

#Test Packet TX Software Version #1

from RFM69 import Radio, FREQ_915MHZ
import datetime
import time

# Function to Send Data
def Radio_TX (payload):
    
    # Send
    print ("Sending")
    if radio.send(recipient_id, payload, attempts=3, waitTime=100):
        print ("Acknowledgement received")
        print ("Payload Sent")
        print (payload)
    else:
        print ("No Acknowledgement")
    
    return


node_id = 2
network_id = 100
recipient_id = 1

tx_counter = 0

dataset = 1

# Log Data = 1, Sensor Status = 2, Picture Data = 3
datatype = 1;
# Payload Intialize
payload = [datatype, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                255, 255, 255, 255, 255, 255, 255, 255, 255, 255];

# Setup Radio
powerlvl = 90 #0-100

with Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=True) as radio:
    print ("Radio Initialized...")
    
    # RC Timer Accuracy 4.3.5 pg41
    # Radio auto calibrated on Power Up
    # Applications enduring large temperature variations, and for which the power supply is never removed, RC calibration can  be  performed  upon  user  request.
    # RegOsc1 (0x0A) - RcCalStart, RcCalDone
    print ("Calibrating Radio...")
    radio.calibrate_radio()
    
    # Set the transmit power level
    # Value between 0 and 100
    # RegPaLevel - Outputpower: Output power setting, with 1 dB steps
    print ("Setting Power Level...")
    radio.set_power_level(powerlvl)
    
    while True:
        # Every 5 seconds send a message
        if tx_counter > 0.5:
            tx_counter=0

            #Call Function to Send Payload
            Radio_TX(payload)
        
        # Transmit Delay/Counter
        delay = 1
        tx_counter += delay
        time.sleep(delay)
    
        # Simulate Different Datatypes/Payloads
    
        # Datatype 1 to 3
        datatype = datatype + 1
        
        if datatype > 3:
            datatype =1
        
        # Dataset (only datatype and 60 bytes can be recieved)
        if dataset > 1:
        
            payload = [datatype, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                                31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                                61, 62, 63, 64, 65, 66, ];
            dataset = 1
        else:
            payload = [datatype, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,];
            dataset = 2
        
        # Display current dataset and datatype
        print( "dataset is", dataset, "dataype is", datatype)

