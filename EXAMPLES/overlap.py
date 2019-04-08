import EasySound as ES

#Initialize recording object wih the stream S
S=ES.openStream()
met=ES.Record(S)

met.prepareRecord()
input('press ENTER to start recording metronome')
met.startRecord()
input('press ENTER to end recording')
met.stopRecord()
met.setFrames(met.getFrames()*10)


rec = ES.Record(S)
rec.prepareRecord()
input('press ENTER to start recording channel 1')
rec.recordOnListenning(met.getRecordLenght(), met.getFrames())

rec2 = ES.Record(S)
rec2.prepareRecord()
input('press ENTER to start recording channel 2')
rec2.recordOnListenning(met.getRecordLenght(), met.getFrames())


#sets rec frames as the sum of both frames
print('Merging the channels...')
rec.setFrames(ES.sumFrames(rec.getFrames(), rec2.getFrames()))
input('press ENTER to play')
rec.playRecord()