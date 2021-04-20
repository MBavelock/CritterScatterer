#*******************************************#
#           Library Imports - Start         #
#*******************************************#
# General Libraries
import time

# Pi Camera
from picamera.array import PiRGBArray
from picamera import PiCamera

# GPIO
import RPi.GPIO as GPIO

# Radio RFM69
from RFM69 import Radio, FREQ_915MHZ

# Tensorflowlite
import os
import numpy as np
import cv2
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate

# Audio
import pygame

#*******************************************#
#           Library Imports - End           #
#*******************************************#

#*******************************************#
#           Control Panel - Start           #
#*******************************************#
# Camera
# initialize the camera
camera = PiCamera()
# Default image size captured from camera
ImageSize = (1080,720)

# Object Detection
GRAPH_NAME = "4_10b_output_tflite_graph_edgetpu.tflite"
LABELMAP_NAME = "label_map.txt"
min_conf_threshold = float(0.5)

    # Load the label map
with open(LABELMAP_NAME, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

    # Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=GRAPH_NAME,
                          experimental_delegates=[load_delegate('libedgetpu.so.1.0')])

interpreter.allocate_tensors()

    # Get model details
input_details = interpreter.get_input_details()
#output_details = interpreter.get_output_details()
height = 300
width = 300
input_mean = 127.5
input_std = 127.5

# Radio
node_id = 2
network_id = 100
recipient_id = 1
Radio_Power_Level = 90 # Between 0 - 100 (dB)
#print('Debug: Making Radio object...')
FieldRadio = Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=False)
#print('Debug: Radio Object Made')

# Relay Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
    # Water pump
WATER_PUMP_PIN = 33 # Enter pin
GPIO.setup(WATER_PUMP_PIN, GPIO.OUT) # Set pin to output 
WATER_PUMP_PIN_STATE = 1
GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE) # Set pin High
    # Flood Light
FLOOD_LIGHT_PIN = 31 # Enter pin
GPIO.setup(FLOOD_LIGHT_PIN, GPIO.OUT) # Set pin to output 
FLOOD_LIGHT_PIN_STATE = 1
GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE) # Set pin High
    # IR Light
IR_LIGHT_PIN = 35 # Enter pin
GPIO.setup(IR_LIGHT_PIN, GPIO.OUT) # Set pin to output 
IR_LIGHT_PIN_STATE = 1
GPIO.output(IR_LIGHT_PIN, IR_LIGHT_PIN_STATE) # Set pin High

# Water Sensors
    # 50% Float Switch
HALF_FLOAT = 36 # Enter pin
GPIO.setup(HALF_FLOAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 0% Float Switch
EMPTY_FLOAT = 32 # Enter pin
GPIO.setup(EMPTY_FLOAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Audio
pygame.mixer.init()
AudioFileDir = "/AudioFiles/"

# PIR Sensor
    # Motion Detection
PIR_PIN = 21 # Enter pin
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Errors
RadioError = False
RelayError = False
CameraError = False
ClassifierError = False
FloatError = False
AudioError = False

#*******************************************#
#           Control Panel - End             #
#*******************************************#


#*******************************************#
#                   Begin                   #
#*******************************************#
# Take Image from camera
def TakeImage():
    # grab a reference to the raw camera capture
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    camera.resolution = ImageSize
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    # Verticle flip - MAYBE?
    image = cv2.flip(image, 0)
    return image

def SystemStartUp():
    # Radio
    try:
        FieldRadio.calibrate_radio()
        FieldRadio.set_power_level(Radio_Power_Level)
        FieldToHome = True #False
        HomeToField = True #False
        delay = 0.5
        delaycount = 0
        TXP = [52]
        while(not(FieldToHome and HomeToField)):
            # Send a ping to the Homestation and wait for a response
            if ((delaycount % 5) == 0):
                #print('Debug: Field Waiting For Home To Ack...')
                FieldRadioStatus = FieldRadio.send(recipient_id, TXP, attempts=5, waitTime=100)
                FieldToHome = True
            if (FieldRadioStatus):
                #print('Debug: Wating for Home to send...')
                RadioReturn = FieldRadio.get_packets()
                for packet in RadioReturn:
                    #print('Debug: RX: ',packet)
                    if(packet.data == [52]):
                        HomeToField = True
            time.sleep(delay)
            delaycount += delay
    except:
        RadioError = True
        print('Debug: Radio Error -', RadioError)

    # Relays
    try:
        #print('Debug: Testing Relays...')
        time.sleep(1)
        # Water Pump
        WATER_PUMP_PIN_STATE = 0
        GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
        time.sleep(2)
        WATER_PUMP_PIN_STATE = 1
        GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
        time.sleep(1)
        # Flood Light
        FLOOD_LIGHT_PIN_STATE = 0
        GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE)
        time.sleep(2)
        FLOOD_LIGHT_PIN_STATE = 1
        GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE)
        time.sleep(1)
        # IR Light
        IR_LIGHT_PIN_STATE = 0
        GPIO.output(IR_LIGHT_PIN, IR_LIGHT_PIN_STATE)
        time.sleep(2)
        IR_LIGHT_PIN_STATE = 1
        GPIO.output(IR_LIGHT_PIN, IR_LIGHT_PIN_STATE)
        time.sleep(1)
    except:
        RelayError = True
        print('Debug: Relay Error -', RelayError)

    # Camera
    try:
        Image = TakeImage()
    except:
        CameraError = True
        print('Debug: Camera Error -', CameraError)

    # Classifier
    try:
        ClassifierHits = RunInference(Image)
        print(ClassifierHits)
    except:
        ClassifierError = True
        print('Debug: Classifier Error -', ClassifierError)

    # Audio
    try:
        LastAudio = AudioDeterrent("AudioFiles/BaldEagle00.mp3",0.5)
    except:
        AudioError = True
        print('Debug: Audio Error -', AudioError)
                                   
    # Floats
    try:
        WaterLevel = CheckWaterLevel()
        print(WaterLevel)
    except:
        FloatError = True
        print('Debug: Float Error -', FloatError)
    # Return the time at which the system setup occured
    return time.time()

def RunInference(frame):
    #frame = cv2.imread(directory + filename)
    imH, imW, c = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)
    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    # Retrieve detection results 
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    return classes

def AudioDeterrent(File_Selector, Volume_Lvl):
    pygame.mixer.music.load(File_Selector) #Loading audio file to be played
    pygame.mixer.music.set_volume(Volume_Lvl) #Setting volume, range between 0.0 - 1.0
    pygame.mixer.music.play() 
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.music.unload()
    return time.time()

def VisualDeterrent(UseTime):
    WATER_PUMP_PIN_STATE = 1
    GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
	time.sleep(UseTime)
	WATER_PUMP_PIN_STATE = 0
    GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
    return time.time()

def WaterDeterrent(UseTime):
    FLOOD_LIGHT_PIN_STATE = 1
    GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE))
	time.sleep(UseTime)
    FLOOD_LIGHT_PIN_STATE = 0
    GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE))
    return time.time()

def CheckWaterLevel():
    if (GPIO.input(HALF_FLOAT) == GPIO.LOW):
        return 2
    if (GPIO.input(EMPTY_FLOAT) == GPIO.LOW):
        return 1
    return 0

def CheckPIR():
    if (GPIO.input(PIR_PIN) == GPIO.HIGH):
        return time.time()
	return 0


##############################################################
def main():
    LastSystemStartUp = SystemStartUp()
    print('System Ready')


if __name__ == '__main__':
    main()
