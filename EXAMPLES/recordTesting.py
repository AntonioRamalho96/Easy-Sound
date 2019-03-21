import Environment
from Environment import Record, EasySound

#Init=tialize recording object wih the stream S
es=EasySound()
S=es.openStream()
rec=Record(S)

input('press ENTER to start recording')
rec.startRecord()
input('press ENTER to end recording')
rec.stopRecord()
input('press ENTER to listen to record')
rec.playRecord()



