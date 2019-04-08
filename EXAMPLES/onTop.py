import EasySound as ES

#Initialize recording object wih the stream S
S=ES.openStream()
rec=ES.Record(S)

rec.prepareRecord()
input('press ENTER to start recording')
rec.startRecord()
input('press ENTER to end recording')
rec.stopRecord()
print(rec.getRecordLenght())
rec2 = ES.Record(S)
rec2.prepareRecord()
input('press ENTER to start recording')

print('recording, wait...')
rec2.recordOnTop(rec.getRecordLenght(), rec.getFrames())
input('press ENTER to play')
rec2.playRecord()