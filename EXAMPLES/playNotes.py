from Environment import EasySound, Record
import numpy as np
import struct
import matplotlib.pyplot as plt
import copy

#returns a record object with frequency -freq- in Hz, volume -Volume- (from 0 to 32000)
#and -time- seconds of lenght
def produceTone(record, freq, Volume, time):
    frames=[]
    plotFrames=()
    count=0
    for i in range(ES.timeToChunks(time)): #for all the chunks of the record
        thisChunk=()
        for j in range(1024): #for each of the samples in each chunk
            thisChunk=thisChunk+(((np.int16)(Volume*np.cos(freq*np.pi*2/44100*count))),)  #put samples representing a cosine function
            count=count+1
        frames.append(struct.pack("=1024h", *thisChunk))
        plotFrames=plotFrames+thisChunk
    record.setFrames(frames)
    return copy.copy(record)

#creates a Record object
print('openning stream...')
ES=EasySound()
S=ES.openStream()
rec=Record(S)

#create Record Objects for each tone
input('Done! Press ENTER to load notes')
G=produceTone(rec, 392, 5000, 0.5) #G tone
A=produceTone(rec, 440, 5000.0, 0.5) #A tone
A2=produceTone(rec, 440, 5000.0, 1) #A tone with twice the lenght
B=produceTone(rec, 493, 5000, 0.5)
B2=produceTone(rec, 493, 5000, 1)
C=produceTone(rec, 523, 5000, 0.5)
D=produceTone(rec, 587, 5000, 0.5)
P=produceTone(rec, 0, 0, 0.5) #pause(record with volume=0)

#Plays ode of joy!
input('Done! Press ENTER to play song')
B.playRecord()
B.playRecord()
C.playRecord()
D.playRecord()
D.playRecord()
C.playRecord()
B.playRecord()
A.playRecord()
G.playRecord()
G.playRecord()
A.playRecord()
B.playRecord()
B.playRecord()
P.playRecord()
A.playRecord()
A2.playRecord()
