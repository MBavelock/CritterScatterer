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
#from RFM69 import Radio, FREQ_915MHZ

# Tensorflowlite
import os
import numpy as np
import cv2
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate

# Audio
import pygame

# Text to speech
import pyttsx3
engine = pyttsx3.init() # object creation
volume = engine.getProperty('volume')
engine.setProperty('volume',1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate',100)

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
#ImageSize = (720,480)
imW = 720
imH = 480
ImageSize = (imW,imH)

# Object Detection
GRAPH_NAME = "4_10b_output_tflite_graph_edgetpu.tflite"
LABELMAP_NAME = "label_map.txt"
min_conf_threshold = float(0.5)

    # Load the label map
with open(LABELMAP_NAME, 'r') as f:
    labels = [line.strip() for line in f.readlines()]
print(labels)
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
#node_id = 2
#network_id = 100
#recipient_id = 1
#Radio_Power_Level = 90 # Between 0 - 100 (dB)
#print('Debug: Making Radio object...')
#FieldRadio = Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=False)
#with Radio(FREQ_915MHZ, node_id, network_id, isHighPower=True, verbose=False) as FieldRadio:
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
HALF_FLOAT = 32 # Enter pin
GPIO.setup(HALF_FLOAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 0% Float Switch
EMPTY_FLOAT = 36 # Enter pin
GPIO.setup(EMPTY_FLOAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Audio
pygame.mixer.init()
AudioFileDir = "/AudioFiles/"

# PIR Sensor
#PIR_PIN = 21 # Enter pin
#GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#DelayBetweenPIR = 0.5 # in seconds

# Errors
RadioError = False
RelayError = False
CameraError = False
ClassifierError = False
FloatError = False
AudioError = False

# Monitoring
SecondsBetweenCameraPoll = 1.5 # in seconds - used to poll area since PIR is non-functioning
#global FileNameCounter
FileNameCounter = 0

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
    #image = cv2.flip(image, 0)
#    filename = 'SavedImage.jpg'
#    cv2.write(filename, image2)
    return image

def SystemStartUp():
    # Radio
    #try:
    #    FieldRadio.calibrate_radio()
    #    FieldRadio.set_power_level(Radio_Power_Level)
    #    FieldToHome = False
    #    HomeToField = False
    #    delay = 0.5
    #    delaycount = 0
    #    TXP = [52]
    #    while(not(FieldToHome and HomeToField)):
    #        # Send a ping to the Homestation and wait for a response
    #        if ((delaycount % 5) == 0):
    #           #print('Debug: Field Waiting For Home To Ack...')
    #            FieldRadioStatus = FieldRadio.send(recipient_id, TXP, attempts=5, waitTime=100)
    #            FieldToHome = True
    #        if (FieldRadioStatus):
    #            #print('Debug: Wating for Home to send...')
    #            RadioReturn = FieldRadio.get_packets()
    #            for packet in RadioReturn:
    #                #print('Debug: RX: ',packet)
    #                if(packet.data == [52]):
    #                    HomeToField = True
    #        time.sleep(delay)
    #        delaycount += delay
    #except:
    #    RadioError = True
    #    print('Debug: Radio Error -', RadioError)
    '''
    FieldRadio.calibrate_radio()
    FieldRadio.set_power_level(Radio_Power_Level)
    FieldToHome = False
    HomeToField = False
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
    '''


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
        BB, ClassifierHits, Scores = RunInference(Image)
        print(ClassifierHits)
    except:
        ClassifierError = True
        print('Debug: Classifier Error -', ClassifierError)

    # Audio
    try:
        LastAudio = AudioDeterrent("AudioFiles/BaldEagle00.mp3",1.0)
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
    return boxes, classes,scores
    '''Detections = []
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
            object_name = labels[int(classes[i])]
            #label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            if Demo:
                engine.say(object_name)
                engine.runAndWait()
                engine.say(str(int(scores[i]*100)))
                engine.runAndWait()
            Detections.append(object_name)
    return Detections'''

def AudioDeterrent(File_Selector, Volume_Lvl):
    pygame.mixer.music.load(File_Selector) #Loading audio file to be played
    pygame.mixer.music.set_volume(Volume_Lvl) #Setting volume, range between 0.0 - 1.0
    pygame.mixer.music.play() 
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.music.unload()
    return time.time()

def VisualDeterrent(On_Off):
    if (On_Off):
        FLOOD_LIGHT_PIN_STATE = 0
        GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE)
    else:
        FLOOD_LIGHT_PIN_STATE = 1
        GPIO.output(FLOOD_LIGHT_PIN, FLOOD_LIGHT_PIN_STATE)
    return time.time()

def WaterDeterrent(On_Off):
    if (CheckWaterLevel() == 0):
        On_Off = False
        print("No Water In Tank or Sensor Error - Pump Disabled")
    elif (CheckWaterLevel() == 1):
        On_Off = False
        print("No Water In Tank - Pump Disabled")
    elif (CheckWaterLevel() == 2):
        print("Water Level At 50%% or More")
    if (On_Off):
        WATER_PUMP_PIN_STATE = 0
        GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
    else:
        WATER_PUMP_PIN_STATE = 1
        GPIO.output(WATER_PUMP_PIN, WATER_PUMP_PIN_STATE)
    return time.time()

def IRLIGHT(On_Off):
    if (On_Off):
        IR_LIGHT_PIN_STATE = 0
        GPIO.output(IR_LIGHT_PIN, IR_LIGHT_PIN_STATE)
    else:
        IR_LIGHT_PIN_STATE = 1
        GPIO.output(IR_LIGHT_PIN, IR_LIGHT_PIN_STATE)
    return time.time()

def CheckWaterLevel():
    if (GPIO.input(HALF_FLOAT) == GPIO.LOW):
        return 2
    if (GPIO.input(EMPTY_FLOAT) == GPIO.LOW):
        return 1
    return 0

#def CheckPIR():
#    if (GPIO.input(PIR_PIN) == GPIO.HIGH):
#        return time.time()
#    return 0

def NightTime():
    # Check if its night or not
    return 0


def NormalOperation():
    # First time variables
    Reassess = False
    DogsAllowed = False
    CatsAllowed = False
    LowLight = False
    RadioTime = time.time()
    while True:
        time.sleep(DelayBetweenPIR)
        # Assign Threats list - May change based on user input (Default = False)
        Threats = ['nothing','dog','cat','fox','heron','human','human face','human legs','kingfisher','minkish','opossum','raccoon']
        if DogsAllowed:
            Threats.remove('dog')
        if CatsAllowed:
            Threats.remove('cat')
        LOG_PIRHit = CheckPIR()
        if LOG_PIRHit:
            engine.say("P I R Motion Detected")
            engine.runAndWait()
        # When PIR detects record time and run classification
        if LOG_PIRHit or Reassess:
            #PositiveClassification = []
            ThreatDetected = False
            AllClassifications = []
            for i in range(NumberOfImagesPerPIRHit):
                if Demo:
                    engine.say("Taking Picture")
                    engine.runAndWait()
                IRLight(True) # Enable IR Flood light - it has a photo sensor on it so it wont turn on unless its in low light
                time.sleep(0.1) # Allow some time for the Light to turn on before taking picture
                Sample = TakeImage()
                IRLight(False)
                ClassifierHits = RunInference(Sample)
                AllClassifications.append(ClassifierHits)
                #AllImages.append(Images)
                # Check Labels against list of threats - May need a better system of determining a threat = true
                # Right now its any true beats all falses - MAY want to average (3/9/21)
                for Label in labels:
                    for Threat in Threats:
                        if Label == Threat:
                            ThreatDetected = True
                            LOG_ClassifiedEvent = time.time()
            # If the found object is a known threat activate deterrents
            if ThreatDetected:
                LOG_DeterrentX = 0
                LOG_DeterrentY = 0
                LOG_DeterrentZ = 0
                # Deterrents to use and when TBD
                if NightTime():
                    # RUN deterrent (Light?)
                    LOG_DeterrentX = time.time()
                else:
                    # RUN Deterrent (Audio?)
                    LOG_DeterrentY = time.time()
                # RUN Deterrent (Water?)
                LOG_DeterrentZ = time.time()
                # Recheck area
                Reassess = True
                EventEnd = 0
            else:
                Reassess = False
                EventEnd = time.time()
            # Add Variables to LOG
            LOG = open("Log.txt", "a")
            LOG.write("New Event:\n")
            LOG.write(LOG_PIRHit)
            LOG.write("\n")
            LOG.write(LOG_ClassifiedEvent)
            LOG.write("\n")
            LOG.write(LOG_DeterrentX)
            LOG.write("\n")
            LOG.write(LOG_DeterrentY)
            LOG.write("\n")
            LOG.write(LOG_DeterrentZ)
            LOG.write("\n")
            LOG.close()
        if RadioTime-time.time() >= 360: # Check if time since last radio communication >= 5 minutes
            # Radio communication here
            # Time Check
            # Send new events
            # Receive Settings
            RadioTime = time.time()
        # Spin


def RunDemo(Confid, FileNameCounter):
    # Demo needs to:
    #   poll area with camera every 1.5? second(s)
    #       run inference on image
    #       display image for demonstrator via remote log in with found BBoxes and labels
    #       Use Visual, Audio, and water deterrent
    # Also used to test power consumption
    #       test drain and charge with camera polling every 1 sec 
    HumanDetection = False
    CatDetection = False
    DogDetection = False
    MinkDetection = False
    CoyoteDetection = False
    RaccoonDetection = False
    OpossumDetection = False
    HeronDetection = False
    KingfisherDetection = False
    
    Sample = TakeImage()
    BBoxes, Classes, Scores = RunInference(Sample)
    ### Add labels, BBox to image
    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(Scores)):
        if ((Scores[i] > Confid) and (Scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(BBoxes[i][0] * imH)))  
            xmin = int(max(1,(BBoxes[i][1] * imW)))   
            ymax = int(min(imH,(BBoxes[i][2] * imH))) 
            xmax = int(min(imW,(BBoxes[i][3] * imW))) 

            cv2.rectangle(Sample, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(Classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(Scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(Sample, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(Sample, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

            # Draw circle in center
            xcenter = xmin + (int(round((xmax - xmin) / 2)))
            ycenter = ymin + (int(round((ymax - ymin) / 2)))
            cv2.circle(Sample, (xcenter, ycenter), 5, (0,0,255), thickness=-1)

            # Print info
            print('Object ' + str(i) + ': ' + object_name + ' at (' + str(xcenter) + ', ' + str(ycenter) + ')')
            if (object_name == 'human') or (object_name == 'human face') or (object_name == 'human legs'):
                HumanDetection = True
            elif (object_name == "cat"):
                CatDetection = True
            elif (object_name == "dog"):
                DogDetection = True
            elif (object_name == "minkish"):
                MinkDetection = True
            elif (object_name == "coyote"):
                CoyoteDetection = True
            elif (object_name == "raccoon"):
                RaccoonDetection = True
            elif (object_name == "heron"):
                HeronDetection = True
            elif (object_name == "kingfisher"):
                KingfisherDetection = True
            elif (object_name == "opossum"):
                OpossumDetection = True
    NewFileName = './CLA/' + str(FileNameCounter) + '.jpg'
    cv2.imwrite(NewFileName, Sample)
    preview = cv2.resize(Sample, (1080, 720))
    cv2.imshow('Object detector', preview)
    cv2.waitKey(2)


    if (HumanDetection):
        print("Human Detected - No deterrents used")
        
    elif (CatDetection):
        print("Cat Detected - Using Audio file of cat hissing")
        #AudioDeterrent("AudioFiles/Dog00.mp3",1.0)
        
    elif (DogDetection):
        print("Dog Detected - Using Audio file of ....")
        #AudioDeterrent("AudioFiles/Blast00.mp3",1.0)
        
    elif (MinkDetection):
        print("Mink or Mink-like animal Detected - Using water deterrent for 5 seconds")
        #WaterDeterrent(True)
        #time.sleep(5)
        #WaterDeterrent(False)
        
    elif (CoyoteDetection):
        print("Coyote Detected - Using water deterrent for 5 seconds")
        #WaterDeterrent(True)
        #time.sleep(5)
        #WaterDeterrent(False)
        
    elif (RaccoonDetection):
        print("Raccoon Detected - Using water deterrent for 5 seconds")
        #WaterDeterrent(True)
        #time.sleep(5)
        #WaterDeterrent(False)
        
    elif (HeronDetection):
        print("Heron Detected - Using Visual and Audio Deterrent")
        #VisualDeterrent(True)
        #AudioDeterrent("AudioFiles/Hawk02.mp3",1.0)
        #time.sleep(3)
        #VisualDeterrent(False)
        
    elif (KingfisherDetection):
        print("Kingfisher Detected - Using Visual and Audio Deterrent")
        #VisualDeterrent(True)
        #AudioDeterrent("AudioFiles/Hawk02.mp3",1.0)
        #time.sleep(3)
        #VisualDeterrent(False)
        #WaterDeterrent(True)
        #time.sleep(5)
        #WaterDeterrent(False)
        
    elif (OpossumDetection):
        print("Opossum Detected - Using water deterrent for 5 seconds")
        #WaterDeterrent(True)
        #time.sleep(5)
        #WaterDeterrent(False) 
        
    else:
        print("No Detections found - Not deterrents activated")
    
    


##############################################################
def main():
    counter = 0
    # Init system
    #TimeOfLastCheck = SystemStartUp()
    #sample = TakeImage()
    #BB, CL, SC = RunInference(sample)
    LastCheck = 0
    # Loop forever
    #VisualDeterrent(True)
    #IRLIGHT(True)
    while(True):
         #sample = TakeImage()
         #cv2.imshow('test', sample)
         #cv2.waitKey(1)
        if ((time.time() - LastCheck) >= SecondsBetweenCameraPoll):
            RunDemo(0.5, counter)
            counter += 1
            LastCheck = time.time()

if __name__ == '__main__':
    main()
