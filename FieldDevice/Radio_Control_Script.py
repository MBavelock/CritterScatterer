# Based off of Example Code from https://rpi-rfm69.readthedocs.io/en/latest/example_basic.html#simple-transceiver

from RFM69 import Radio, FREQ_915MHZ
import datetime
import time

node_id = 1
network_id = 100
recipient_id = 2

# Setup Radio
powerlvl = 90 #0-100

with Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=True, encryptionKey = "1234567890ABCDEF") as radio:
    print ("Starting loop...")
    
    rx_counter = 0
    tx_counter = 0

    # Read Radio Temperature -40C to 85C
    # RegTemp1 (0x4E) - TempMeasStart, TempMeasRunning
    # RegTemp2 (0x4F) - TempValue
    print ("Checking Radio Temp")
    print (radio.read_temperature(0))
    
    # Read Radio Registers
    # Registers (0x00 - 0x50)
    print ("Reading All Registers...")
    print (radio.read_registers())
    
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
        
        # Every 10 seconds get packets
        if rx_counter > 10:
            rx_counter = 0
            
            # Process packets
            for packet in radio.get_packets():
                print (packet)
                
                # Print Out Data Packet
                #for length in packet.data:
                    #print(length)
                
                #Create a list of data from packet
                #data = []
                
                ##Add elements based on length of data
                ##for i in range(0,len(packet.data)):
                    ##data.append(i)
                    ##data[i] = packet.data[i]
                
                #Print out the list of data elements
                #for i in packet.data:
                    #data.append(i)
                    #print ({i}) # size of data =

                #Print out the list of data elements
                #for j in data:
                    #print (j) # size of data =
                    
                ##print(data[0])
                    
        # Every 5 seconds send a message
        if tx_counter > 5:
            tx_counter=0

            # Send
            print ("Sending")
            if radio.send(recipient_id, "C", attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")


        print("Listening...", len(radio.packets), radio.mode_name)
        delay = 0.5
        rx_counter += delay
        tx_counter += delay
        time.sleep(delay)
