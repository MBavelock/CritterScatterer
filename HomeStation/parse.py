#*******************************************#
#          Script to parse eventlog         #
#             into multiple logs            #
#*******************************************#
import sys
import os
from pathlib import Path

#Parsing for main event log file into smaller files
class MainFileParse():
    def __init__(self):

        #Try to open file for reading
        filepath = Path('HomeStation/EventFiles/EventLog.txt')
        
        try:
            infile = open(filepath, 'r')
        except:
            print('File not found!')
            return
        
        #Read line by line
        Lines = infile.readlines()
        toggle = False
        count = 0
        buffer = []

        #Iterate through lines to find filename and store each entry in a buffer
        for line in Lines:
            #Iterate
            count += 1

            #If ! then toggle write, set count for multiple files
            if '!' in line:
                toggle = not toggle
                count = 1
                filename = ''
                continue

            #While toggle is on, manipulate output log file
            while toggle:
                inline = line.split()
                buffer.append(inline[0] + ' ' + inline[1] + '\n')

                #If reading second line, store the date
                if count == 2:
                    filename = inline[1] + '_'
                    break
                #If reading third line, store the time
                elif count == 3:
                    filename += inline[1]
                    #Create outfile using filename
                    outfile = open('HomeStation/EventFiles/' + filename + '.txt', 'w')
                    break
                else:
                    break

            #When toggle turns off, write buffer to file
            while not toggle:
                #Write to outfile
                for i in buffer:
                    outfile.write('{}'.format(i))

                #Close outfile to confirm write and empty buffer
                buffer = []
                outfile.close()
                break

        #############################################
        #    Outside buffer write for final entry   #
        #############################################
        while not toggle:
            #Write to outfile
            for i in buffer:
                outfile.write('{}'.format(i))

            #Close outfile to confirm write and empty buffer
            buffer = []
            outfile.close()
            break
    
        #Close infile once completely done
        infile.close()

if __name__ == '__main__':
    MainFileParse()