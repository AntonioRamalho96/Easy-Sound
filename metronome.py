from Environment import EasySound, Record
import numpy as np
import struct

ES=EasySound()
S=ES.openStream()
rec=Record(S)
input('press enter to start recording')
input('finished recording, press enter to play')

def produceTone(record, freq, Volume, time):
    frames=[]
    count=0
    for i in range(ES.timeToChunks(time)):
        thisChunk=()
        for j in range(2048):
            thisChunk=thisChunk+((np.int16)(Volume*np.cos(freq*np.pi*2*2048/44100*count)),)
            count=count+1
            if count>(16*np.pi):
                count=count-16*np.pi
        frames.append(struct.pack("=2048h", *thisChunk))
    record.setFrames(frames)
    record.playRecord()

produceTone(rec, 7500, 5000, 3)


