import EasySound as ES
from threading import Thread
import time
import struct

S=ES.openStream()
rec=ES.Record(S)

rec.startRecord()
time.sleep(1)
rec.stopRecord()

frames=rec.getFrames()
frameList=ES.framesToList(frames)
print(frameList)
