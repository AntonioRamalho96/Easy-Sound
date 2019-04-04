import Environment
from Environment import EasySound, Record

ES=EasySound()
S=ES.openStream()
rec=Record(S)


rec.prepareRecord() #This allows recording to start instantainiously


input('Press ENTER to start recording')
rec.startRecord()
input('Press ENTER to stop recording')
rec.stopRecord()

times=int(input('Loop how many times?'))
frames=rec.getFrames()
rec.setFrames(frames*times)
rec.playRecord()