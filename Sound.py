import struct
import pyaudio
from threading import Lock
from threading import Thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

#Creates an envirolnment. An envirolnment is an object containning Loops
#in an environment it is possible to play its loops in a syncronized way
# Future expantions to be done:
# add sounds at keypresses
# record loop 
class Sound:

    #the stream is a data stream
    #reading from stream we obtain the CHUNK samples from the micro
    #the micro reads RATE samples per second
    def __init__(self):
        self.__frames=[]
        print('Not defined yet...')


    
    #Records a loop, finishes recording when user presses ENTER
    def recordOnEnter(self):
        self.__stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
        print('press ENTER to finish recording')
        self.keepRecording=True
        Thread(self.__waitingThread).start()
        count=0
        frames=[]
        while(self.keepRecording):
            count=count+1
            data = self.__stream.read(CHUNK)
            frames.append(data)
        print('Time recorded was'+ repr(count*1024/44100))
        self.__closeEverithing()

        self.__frames = frames.copy()
    #thread waiting for user input to stop recording
    def __waitingThread(self):
        input()
        self.keepRecording=False

    #Records a Sound, finishes recording when a certain time is lapsed
    def recordOnTime(self, time):
        self.__stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
        frames=[]
        count=0
        input('press ENTER to start recording')
        print('recording...')
        while(count*1024/44100 < time):
            count=count+1
            data = self.__stream.read(CHUNK)
            frames.append(data)

        print('Time recorded was'+ repr(count*1024/44100))
        self.__closeEverithing()
        self.__frames = frames.copy()

    def setFrames(frames):
        self.__frames=frames.copy()

    def getFrames()
        return self.__frames.copy()



    #Close environment
    def __closeEverithing(self):
        self.__stream.stop_stream()
        p.terminate