import struct
import pyaudio
import wave
from threading import Lock
from threading import Thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

class EasySound:
    def openStream(self):
        p=pyaudio.PyAudio()
        return p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    #Creates an envirolnment. An envirolnment is an object containning Loops
    #in an environment it is possible to play its loops in a syncronized way
    # Future expantions to be done:
    # add sounds at keypresses
    # record loop 
    class Environment:

        #the stream is a data stream
        #reading from stream we obtain the CHUNK samples from the micro
        #the micro reads RATE samples per second
        def __init__(self):
            self.__stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
            #List of loops in the environment
            self.allLoops=[]
            self.__close=False
            self.__launchFlusher()


            print('Not defined yet...')


        #See flusher, the flusher is launched running
        def __launchFlusher(self):
            self.__mutex=Lock()
            Thread(target=self.__flusherLoop).start()
        #Start flushing
        def __startStreamContinuousFlush(self):
            self.__mutex.release()
        #Stopps flushing
        def __stopStreamContinuousFlush(self):
            self.__mutex.acquire()
        #This loop continuosly reads data from the microphone
        #preventing from a queue of data to be formed in the
        #stream
        def __flusherLoop(self):
            while (self.__close==False):
                print('flushing')
                self.__mutex.acquire()
                self.__stream.read(CHUNK)
                self.__mutex.release()
        
        #Records a loop, finishes recording when user presses ENTER
        def recordLoopOnEnter(self):
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
            return frames
        #thread waiting for user input to stop recording
        def __waitingThread(self):
            input()
            self.keepRecording=False

        #Records a loop, finishes recording when a certain time is lapsed
        def recordLoopOnTime(self, time):
            frames=[]
            count=0
            self.__stopStreamContinuousFlush()
            print('recording...')
            while(count*1024/44100 < time):
                count=count+1
                data = self.__stream.read(CHUNK)
                frames.append(data)
            self.__startStreamContinuousFlush()
            print('Time recorded was'+ repr(count*1024/44100))
            return self.Loop(frames, self.__stream)


        #Close environment
        def closeEverithing(self):
            self.__close=True
            self.__stream.stop_stream()
            p.terminate



        class Loop:
            def __init__(self, framesList, stream):
                self.frames = framesList.copy()
                self.loopLenght=len(self.frames)
                self.active=False
                self.volume=[]
                for i in range(self.loopLenght):
                    self.volume.append(1)
                self.playableFrames=self.frames
                self.stream=stream
                
            def setVolume(self, loopVolume):
                if len(loopVolume)==self.loopLenght:
                    self.volume=loopVolume.copy()
                    self.playableFrames=self.frames.copy()
                    for miniChunkIndex in range(len(self.playableFrames)):
                        miniChunkList=struct.unpack("=" + repr(CHUNK*2)+ "h", self.playableFrames[miniChunkIndex])
                        for miniChunkFrameIndex in range(len(miniChunkList)):
                            miniChunkList[miniChunkFrameIndex]=miniChunkList[miniChunkFrameIndex]*self.volume[miniChunkIndex]
                        self.playableFrames[miniChunkIndex]=struct.pack("=" + repr(CHUNK*2)+ "h", *miniChunkList)
                else:
                    print(" in -set volume- argument must have same lenght as loop")
                    return

            def playLoop(self):
                print('playing loop')
                for data in self.playableFrames:
                    self.stream.write(data)
                print('done playing')

    class Record:
        def __init__(self, stream):
            self.__frames = [] #audio info
            self.__recordLenght=0
            self.__recording=False
            self.__stream=stream

        def startRecord(self):
            self.__frames=[]
            if self.__recording:
                print('Cant startRecord when there is a record already in process')
                print('use stopRecord first')
                return False
            self.__recording=True
            Thread(target=self.__recordingLoop).start()
            return True

        def recordSpecifiedlenght(self, lenght):
            self.__frames=[]
            for i in range(lenght):
                self.__frames.append(self.__stream.read(CHUNK))
            self.__recordLenght=lenght
            return self.__frames.copy()


        def __recordingLoop(self):
            while self.__recording:
                self.__frames.append(self.__stream.read(CHUNK))

        def stopRecord(self):
            self.__recording=False
            self.recordLenght=len(self.__frames)
            return self.__frames.copy()

        def playRecord(self):
            for part in self.frames:
                self.__stream.write(part)

        def getFrames(self):
            return self.__frames.copy()

        def setFrames(self, frames):
            self.__frames=frames.copy()
            self.__recordLenght=len(frames)

        def getRecordLenght(self):
            return self.__recordLenght

        def recordToWav(self, outputFileName):
            wf = wave.open(outputFileName, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.__frames))
            wf.close()
                
			
		