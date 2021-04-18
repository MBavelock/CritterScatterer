import pygame, time
pygame.mixer.init()

def PlayAudioDeterrent(File_Selector, Volume_Lvl):
    
    pygame.mixer.music.load(File_Selector) #Loading audio file to be played
    
    pygame.mixer.music.set_volume(Volume_Lvl) #Setting volume, range between 0.0 - 1.0
    
    print ("Playing: %s" %(File_Selector))
    print ("Volume: ", pygame.mixer.music.get_volume())
    print ("")
    
    pygame.mixer.music.play() 
    
#while(1):

 #   PlayAudioDeterrent("Cat3.mp3", .1)
  #  time.sleep(5)

PlayAudioDeterrent("Heron1.mp3", .1)
time.sleep(5)
PlayAudioDeterrent("Heron2.mp3", .1)
time.sleep(5)

PlayAudioDeterrent("Cat1.mp3", .7)
time.sleep(3)
PlayAudioDeterrent("Cat2.mp3", .02)
time.sleep(5)
PlayAudioDeterrent("Cat3.mp3", .1)

#PlayAudioDeterrent("Heron1.mp3", .1)
#time.sleep(5)
#PlayAudioDeterrent("Heron2.mp3", .15)
#time.sleep(5)

#PlayAudioDeterrent("Cat1.mp3", 1)
#time.sleep(3)
#PlayAudioDeterrent("Cat2.mp3", .1)
#time.sleep(5)
#PlayAudioDeterrent("Cat3.mp3", .1)

