#*main.py will run on startup of system*
#*will run and coordinate all processes within field device*


# import libraries

# Start Main
def main():
  # Init Stuff
    # Check connection with home (radio)
    # Check (maybe) power
    # Check camera status
    # load model and perform inital inference
    # Check (maybe) deterrents
  while true:
    # PIR monitoring (either parallel script or poll in main)
      # if PIR hit
        # Start Record entry - Time/Date
        # Sample monitored space (either parallel script take main space)
        # for loop i = 5?
          # take picture
          # inference picture
        # determine possitive classification (either parallel script take main space)
        # if possitive classification
          # 
        # else
          # Leave current PIR hit
          # Clear Record Entry - Note hit but not classify?
    
    
    
  

if __name__ == __main__:
  main()
