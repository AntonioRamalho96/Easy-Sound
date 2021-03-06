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

# returns a stream object


def openStream():
    return p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)

# closes a stream


def closeStream(stream):
    stream.stop__stream()

# converts time (in seconds) to chunks (groups of CHUNK frames)


def timeToChunks(time):
    return (int)(time*RATE/CHUNK)


def chunksToTime(chunks):
    return chunks*1.0*CHUNK/RATE

# Converts a list to a format playable


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


# Converts a playable list to a integer list
def framesToList(frames):
    sampleList = []
    i = 0
    for miniChunk in frames:
        sampleList = sampleList + \
            list(struct.unpack('='+repr(CHUNK)+'h', miniChunk))
    return copy.copy(sampleList)

# sum chunks in a list of chunks


def sumChunks(chunkList):
    sumChunk = (b'\x00\x00')*CHUNK
    for oneChunk in chunkList:
        sumChunk = tuple(map(operator.add, sumChunk, oneChunk))
    return sumChunk

# Plots the sound in a playable object


def plotAudio(frames):
    try:
        import matplotlib.pyplot as plt
    except:
        print('Something went erong while importing -matplot.pyplot-')
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

# creates a wav file from a record object in the directory of the script that calls this function
def recordToWav(record, outputFileName):
    wf = wave.open(outputFileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(record.getFrames()))
    wf.close()


class Record:
    def __init__(self, stream):
        self.__frames = []  # audio info
        self.__recordLenght = 0
        self.__recording = False
        self.__stream = stream
        self.__rate = RATE
        self.__chunk = CHUNK
        self.__format = FORMAT

    def startRecord(self):
        self.__frames = []
        if self.__recording:
            print('Cant startRecord when there is a record already in process')
            print('use stopRecord first')
            return False
        self.__recording = True
        Thread(target=self.__recordingLoop).start()
        return True

    def recordSpecifiedlenght(self, lenght):
        self.__frames = []
        for i in range(lenght):
            self.__frames.append(self.__stream.read(CHUNK))
        self.__recordLenght = lenght
        return self.__frames.copy()

    def __recordingLoop(self):
        while self.__recording:
            self.__frames.append(self.__stream.read(CHUNK))

    def stopRecord(self):
        self.__recording = False
        self.recordLenght = len(self.__frames)
        return self.__frames.copy()

    def playRecord(self):
        for part in self.__frames:
            self.__stream.write(part)

    def getFrames(self):
        return self.__frames.copy()

    def setFrames(self, frames):
        self.__frames = frames.copy()
        self.__recordLenght = len(frames)

    def getRecordLenght(self):
        return self.__recordLenght

    def recordToWav(self, outputFileName):
        wf = wave.open(outputFileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.__frames))
        wf.close()
