#https://rpi-rfm69.readthedocs.io/en/latest/example_basic.html#simple-transceiver

#Test Packet RX Software Version #1
from RFM69 import Radio, FREQ_915MHZ
import datetime
import time

# Function to Recieve Data
def Radio_RX():
    # Clear payload
    payload = []
    # Add elements based on length of data
    for i in range(0,len(packet.data)):
        payload.append(i)
        payload[i] = packet.data[i]
    return payload


#node_id = 1
#network_id = 100
#recipient_id = 2

# Log Data = 1, Sensor Status = 2, Picture Data = 3
#datatype = 1;
# Payload Intialize
#payload = [datatype, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#                255, 255, 255, 255, 255, 255, 255, 255, 255, 255];

# Setup Radio
#powerlvl = 90 #0-100