from Environment import EasySound, Record
import numpy as np
import struct
import matplotlib.pyplot as plt
import copy

print('openning stream...')
ES=EasySound()
S=ES.openStream()
rec=Record(S)

def produceTone(record, freq, Volume, time):
    frames=[]
    plotFrames=()
    count=0
    for i in range(ES.timeToChunks(time)):
        thisChunk=()
        for j in range(1024):
            thisChunk=thisChunk+(((np.int16)(Volume*np.cos(freq*np.pi*2/44100*count))),)  #could be done more efficiently
            count=count+1
        frames.append(struct.pack("=1024h", *thisChunk))
        plotFrames=plotFrames+thisChunk
    record.setFrames(frames)
    record.playRecord()
    return copy.copy(record)
    #plt.plot(plotFrames)
    #plt.show()

input('Done! Press ENTER to load notes')
G=produceTone(rec, 392, 5000, 0.5)
A=produceTone(rec, 440, 5000.0, 0.5)
A2=produceTone(rec, 440, 5000.0, 1)
B=produceTone(rec, 493, 5000, 0.5)
B2=produceTone(rec, 493, 5000, 1)
C=produceTone(rec, 523, 5000, 0.5)
D=produceTone(rec, 587, 5000, 0.5)
P=produceTone(rec, 0, 0, 0.5)

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







