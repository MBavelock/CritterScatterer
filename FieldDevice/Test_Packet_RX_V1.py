#https://rpi-rfm69.readthedocs.io/en/latest/example_basic.html#simple-transceiver

#Test Packet RX Software Version #1


from RFM69 import Radio, FREQ_915MHZ
import datetime
import time

# Function to Send Data
def Radio_RX (payload):
           
    # Process packets
    for packet in radio.get_packets():
        print("Packet Values:")
        print (packet)

    # Clear payload
    payload = []

    # Add elements based on length of data
    for i in range(0,len(packet.data)):
        payload.append(i)
        payload[i] = packet.data[i]

    # Print out Datatype
    if payload[0] == 1:
        print("Log Data")
    elif payload[0] == 2:
        print("Sensor Status")
    elif payload[0] == 3:
        print("Picture Data")

    print("Payload Values:")

    #Print out the list of data elements
    for i in payload:
        print(i, end = ' ')
        
    print()

    return


node_id = 1
network_id = 100
recipient_id = 2

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