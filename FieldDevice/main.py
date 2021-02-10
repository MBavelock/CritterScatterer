#*main.py will run on startup of system*
#*will run and coordinate all processes within field device*


# import libraries

# Start Main
def main():
  # Init Stuff - Loop on failed?
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
          # Add to record - Classification
          # Send home station an alert about classification
          # Activate deterrent method
          # Record deterrent used and Time/Day
        # else
          # Leave current PIR hit
          # Clear Record Entry - Note hit but not classify?
          # delay?
        # Sample again
          # to ensure critter has left
          # deter again 
          # add to record deterrent time/day
          # loop here until critter left
        # Finalize record - Save to text file - All new entries get !
    # After some amount of time T - connect to home station
    # Time check - might have to skew log entries on failed checks
    # Settings check - (TDB)
    # log check - (TBD)
    # 
    
    
    
  

if __name__ == __main__:
  main()
