import struct
import pyaudio
import numpy as np
import wave
from threading import Lock
from threading import Thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()


class EasySound:

    def __init__(self):
        self.__rate=RATE
        self.__chunk=CHUNK
        self.__format=FORMAT

    # creates a stream from which is possible to read (from microphone) and write (to speakers)
    def openStream(self):
        return p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      output=True,
                      frames_per_buffer=CHUNK)

    # Closes a stream
    def closeStream(self, stream):
        stream.stop__stream()

    def timeToChunks(self, time):
        return (int)(time*RATE/CHUNK)

    def getRate(self):
        return self.__rate

    def getChunk(self):
        return self.__chunk

    def getFormat(self):
        return self.__format

    def listToFrames(self, list):
        frames=[]
        for i in list:
            chunkBit=()
            for j in range(self.__chunk):
                chunkBit=chunkBit+(((np.int16)(i)),)
            frames.append(struct.pack("="+repr(self.__chunk)+"h", *chunkBit))
        return frames

    def framesToList(self, frames):
        sampleList=[]
        for miniChunk in frames:
            sampleList+list(struct.unpack("="+repr(self.__chunk)+"h", miniChunk))
        return sampleList
    # Creates an envirolnment. An envirolnment is an object containning Loops
    # in an environment it is possible to play its loops in a syncronized way
    # Future expantions to be done:
    # add sounds at keypresses
    # record loop

        

class Record:
    def __init__(self, stream):
        self.__frames = []  # audio info
        self.__recordLenght = 0
        self.__recording = False
        self.__stream = stream
        self.__rate=RATE
        self.__chunk=CHUNK
        self.__format=FORMAT

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
