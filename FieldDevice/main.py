# Pi Camera Imports
from picamera.array import PiRGBArray
from picamera import PiCamera
# GPIO Imports
import RPi.GPIO as GPIO
# Open CV
import cv2
# Other Imports
import time
import os
import numpy as np
from PIL import Image
# Tensor Flow Lite Imports
#from tflite_runtime.interpreter import load_delegate
#from tflite_runtime.interpreter import Interpreter

#*****Control Panel*****#
# Delay between PIR hits
DelayBetweenPIR = 2

# Number of pictures the camera takes and inferences before a determination is made on whether or not a animals is there
NumberOfImagesPerPIRHit = 2

# Decide if Using Code to debug or real 
Debug = True

# threshold
#threshold = 0.01

# Color of text or bounding boxes
#color = (0,0,255)

# initialize the camera
camera = PiCamera()
# Default image size captured from camera
ImageSize = (640,480)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN) #Define pin 18 as an input pin
PIR18 = GPIO.input(23)

# Take image periodically or bases on PIR hit
TimeLapse = False

# Load Model
#TFLModel = "AnimalModel_v1.0_10000.tflite"
#TFLModel = "AnimalModel_v1.0_100000.tflite"
#TFLLabel = "AnimalModel_v1.0_labels.txt"

# Initalize model
#interpreter = Interpreter(TFLModel,experimental_delegates=[load_delegate('libedgetpu.so.1')])
#interpreter.allocate_tensors()
# Get output for debugging
#input_details = interpreter.get_input_details()
#output_details = interpreter.get_output_details()
#print(input_details)
#print(output_details)
#
#***********************#

def TakeImage():
    # grab a reference to the raw camera capture
    rawCapture = PiRGBArray(camera)
    
    # allow the camera to warmup
    time.sleep(0.1)
    
    # grab an image from the camera
    camera.resolution = ImageSize
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    
    # Verticle flip
    image = cv2.flip(image, 0)
    
    # display the image on screen and wait for a keypress
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    #image = cv2.resize(image,(720, 480))
    return image

def RunOnCamera():
    # Take Image
    ImageToScan = TakeImage()
    
    # Run TFLite Image Classification
    labels = load_labels(TFLLabel)
    #print(labels)
    
    results = RunInference(ImageToScan)
    print(results)
    
    # ScannedImage WILL BE THE IMAGE WIH BOUNDING BOX
    ScannedImage = ImageToScan
    filler = ['Human', 'Dog']
    # determine 
    return filler, ScannedImage

def RunInference(Image):
    # Will run inference on images
    # Of course NOT DONE 3/9/21
    filler = Image
    return filler

def main():
    # Init Stuff - Loop on failed?
    # Check connection with home (radio)
    # Check (maybe) power
    # Check camera status
    # load model and perform inital inference
    # Check (maybe) deterrents
   if Debug:
        count = 0
        if TimeLapse:
            maxcount = 100000
        else:
            maxcount = 100
        while(count <= maxcount):
            if PIR18:
                # Print for debug
                print(count)
                
                # Start timer for debug
                StartTime = time.time()
                
                # Take image at PIR hit 
                ImageToScan = TakeImage()
                
                # Save images with count number
                outfile = './PIR_HIT_%s.jpg' % str(count)
                cv2.imwrite(outfile, ImageToScan)
                
                # Print for debug - time taken
                print("Time from detection to classification: ",time.time() - StartTime)
                count = count + 1
                
            # Delay for amount of time between PIR hits
            time.sleep(DelayBetweenPIR)

  else:
        # First time variables
        Reassess = False
        DogsAllowed = False
        CatsAllowed = False
        LowLight = False
        RadioTime = time.time()
        while True:
            # Assign Threats list - May change based on user input (Default = False)
            Threats = ['nothing','Dog','Cat','3','4','5','6','7','8','9','10','11']
            if DogsAllowed:
                Threats.remove('Dog')
            if CatsAllowed:
                Threats.remove('Cat')    
            # Ensure IR Flood Light is off to save power
            #Disable IR FLOOD LIGHT
            # Poll PIR pin
            PIR18 = GPIO.input(23)
            # When PIR detects record time and run classification
            if PIR18 or Reassess:
                LOG_PIRHit = time.time()
                PositiveClassification = []
                ThreatDetected = False
                for i in range(NumberOfImagesPerPIRHit):
                    if LowLight:
                        #Activate IR Flood Light
                    Labels, Images = RunOnCamera()
                    AllClassifications.append(Labels)
                    AllImages.append(Images)
                    # Check Labels against list of threats - May need a better system of determining a threat = true
                    # Right now its any true beats all falses - MAY want to average (3/9/21)
                    for Label in Labels:
                        for Threat in Threats:
                            if Label == Threat:
                                ThreatDetected = True
                                LOG_ClassifiedEvent = time.time()
                
                # If the found object is a known threat activate deterrents
                if ThreatDetected:
                    # Deterrents to use and when TBD
                    if LowLight:
                        # RUN deterrent (Light?)
                        LOG_DeterrentX = time.time()
                    else:
                        # RUN Deterrent (Audio?)
                        LOG_DeterrentY = time.time()
                    # RUN Deterrent (Water?)
                    LOG_DeterrentZ = time.time()
                    
                    # Recheck area    
                    Reassess = True
                else:
                    Reassess = False
                
                # Add Variables to LOG
                LOG = open("FieldDevice_EventLog.txt", "a")
                LOG.write("New Event:\n"
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
                
            if RadioTime-time.time() >= 360: # Check if time since Start of script 
                # Radio communication here
                RadioTime = time.time()
            # Spin
                 
if __name__ == __main__:
  main()
