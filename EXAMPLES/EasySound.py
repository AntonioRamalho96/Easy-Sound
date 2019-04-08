import struct
import pyaudio
import operator
import numpy as np
import wave
import copy
from threading import Lock
from threading import Thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

#Returns a stream object
def openStream():
    return p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)

    # Closes a stream

#closes stream
def closeStream(stream):
    stream.stop__stream()

#converts time in seconds to chunks (groups of CHUNK frames)
def timeToChunks(time):
    return (int)(time*RATE/CHUNK)

#converts a list of integers to a playable list
def listToFrames(list):
    frames = []
    for i in list:
        chunkBit = ()
        for j in range(CHUNK):
            chunkBit = chunkBit+(((np.int16)(i)),)
        if(len(chunkBit) < CHUNK):
            chunkBit = chunkBit+((np.int16)(0),)*(CHUNK-len(chunkBit))
        frames.append(struct.pack("="+repr(CHUNK)+"h", *chunkBit))
    return frames

#converts a playable list to a list of integers
def framesToList(frames):
    sampleList = []
    i = 0
    for miniChunk in frames:
        sampleList = sampleList + \
            list(struct.unpack('='+repr(CHUNK)+'h', miniChunk))
    return copy.copy(sampleList)

#Sums a list of chunks
def sumChunks(chunkList):
    sumChunk = (b'\x00\x00')*CHUNK
    for oneChunk in chunkList:
        sumChunk = __sumTwoChumks(sumChunk, oneChunk)
    return sumChunk

def __sumTwoChumks(chunk1, chunk2):
    tuple1=tuple(struct.unpack('='+repr(CHUNK)+'h', chunk1))
    tuple2=tuple(struct.unpack('='+repr(CHUNK)+'h', chunk2))
    tuple3=()
    for i in range(CHUNK):
        tuple3=tuple3+(((np.int16)(tuple1[i]+tuple2[i])),)
    return struct.pack("="+repr(CHUNK)+"h", *tuple3)

def sumFrames(frames1, frames2):
    frames3=[]
    if(len(frames1) < len(frames2)):
        print("Length of first argument should be at least the length of 2nd")
    else:
        for i in range(len(frames2)):
            chunkList=[frames1[i], frames2[i]]
            frames3.append(sumChunks(chunkList))
    return frames3


#plots the audio in a frames object
def plotAudio(frames):
    try:
        import matplotlib.pyplot as plt
    except:
        print("Couldn't import matplotlib.plot")
        return False
    plt.plot(tuple(framesToList(frames)))
    plt.show()
    return True

# returns a record object with frequency -freq- in Hz, volume -Volume- (from 0 to 32000)
# and -time- seconds of lenght
def produceTone(stream, freq, Volume, time):
    frames = []
    plotFrames = ()
    count = 0
    for i in range(timeToChunks(time)):  # for all the chunks of the record
        thisChunk = ()
        for j in range(1024):  # for each of the samples in each chunk
            # put samples representing a cosine function
            thisChunk = thisChunk + \
                (((np.int16)(Volume*np.cos(freq*np.pi*2/44100*count))),)
            count = count+1
        frames.append(struct.pack("=1024h", *thisChunk))
        plotFrames = plotFrames+thisChunk
    record = Record(stream)
    record.setFrames(frames)
    return copy.copy(record)

#Creates a .wav file from a record object
def recordToWav(record, outputFileName):
    wf = wave.open(outputFileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(record.getFrames()))
    wf.close()

#Record object
class Record:
    def __init__(self, stream):
        self.__frames = []  # audio info
        self.__recordLenght = 0
        
        self.__stream = stream
        self.__rate=RATE
        self.__chunk=CHUNK
        self.__format=FORMAT
        
        self.__recording = False
        self.__alive=True
        self.__prepare=False

    #Prepares for recording
    def prepareRecord(self):
        self.__prepare=True
        Thread(target=self.__flushing).start()

    #Starts recording (unblocking)
    def startRecord(self):
        self.__frames = []
        if self.__recording:
            print('Cant startRecord when there is a record already in process')
            print('use stopRecord first')
            return False
        self.__recording = True
        if(not self.__prepare):
            self.__prepare=True
            Thread(target=self.__flushing).start()
        return True

    #Records a specific lenght
    def recordSpecifiedlenght(self, lenght):
        self.__frames = []
        if self.__recording:
            print('Cant startRecord when there is a record already in process')
            print('use stopRecord first')
            return False
        self.__prepare=False
        for i in range(lenght+1):
            self.__frames.append(self.__stream.read(CHUNK))
        self.__recordLenght = lenght
        return True

    #Stops recording
    def stopRecord(self):
        self.__recording = False
        self.__recordLenght = len(self.__frames)
        self.__prepare=False
        return self.__frames.copy()

    #Plays a record (blocking)
    def playRecord(self):
        for part in self.__frames:
            self.__stream.write(part)

    #Plays a loop times times
    def playLoop(self, times):
        playFrames=self.__frames*times
        for part in playFrames:
            self.__stream.write(part)

    #returns the audio info
    def getFrames(self):
        return self.__frames.copy()

    #sets the audio info
    def setFrames(self, frames):
        self.__frames = frames.copy()
        self.__recordLenght = len(frames)

    #Returns record lenght in chunks (groups of CHUNK frames)
    def getRecordLenght(self):
        return self.__recordLenght

    def recordToWav(self, outputFileName):
        wf = wave.open(outputFileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.__frames))
        wf.close()

    #Colntinuously discards/records the information in the mic 
    def __flushing(self):
        while(self.__alive and self.__prepare):
            if(self.__recording):
                self.__frames.append(self.__stream.read(self.__chunk))
            else:
                self.__stream.read(self.__chunk)

    #closes a record, important when recording is 'prepared'
    def close(self):
        self.__alive=False