import EasySound

#Usual Record object creation
stream=EasySound.openStream()
rec=EasySound.Record(stream)

#Usual recording
input('Press ENTER to start recording')
rec.startRecord()
input('Press ENTER to stop recording')
rec.stopRecord()

#Produces a wav file
rec.recordToWav('sample.wav')
#OR
#EasySound.recordToWav(rec, 'sample.wav')