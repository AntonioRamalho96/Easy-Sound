import Environment
from Environment import EasySound, Record
from threading import Thread
import time
import struct

ES=EasySound()
S=ES.openStream()
rec=Record(S)

rec.startRecord()
time.sleep(1)
rec.stopRecord()

frames=rec.getFrames()
frameList=ES.framesToList(frames)
print(frameList)
