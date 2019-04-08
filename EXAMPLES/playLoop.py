import EasySound

#Usual Record object creation
stream=EasySound.openStream()
rec=EasySound.Record(stream)

#Usual recording
input('Press ENTER to start recording')
rec.startRecord()
input('Press ENTER to stop recording')
rec.stopRecord()

times=int(input("how many times should I loop?"))
#Plays the record times times in a rows
rec.playLoop(times)