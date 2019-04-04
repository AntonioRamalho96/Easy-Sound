import EasySound as ES

S=ES.openStream()
rec=ES.Record(S)


rec.prepareRecord() #This allows recording to start instantainiously


input('Press ENTER to start recording')
rec.startRecord()
input('Press ENTER to stop recording')
rec.stopRecord()

times=int(input('Loop how many times?'))
frames=rec.getFrames()
rec.setFrames(frames*times)
rec.playRecord()