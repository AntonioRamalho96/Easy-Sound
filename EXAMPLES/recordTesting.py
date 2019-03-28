import EasySound as es

#Initialize recording object wih the stream S
S=es.openStream()
rec=es.Record(S)

input('press ENTER to start recording')
rec.startRecord()
input('press ENTER to end recording')
rec.stopRecord()
input('press ENTER to listen to record')
rec.playRecord()



