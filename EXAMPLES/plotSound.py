import EasySound

#Usual Record object creation
stream=EasySound.openStream()
rec=EasySound.Record(stream)

#Usual recording
input('Press ENTER to start recording')
rec.startRecord()
input('Press ENTER to stop recording')
rec.stopRecord()

#Get the frame list inside the recording
frames=rec.getFrames()

#plots it
EasySound.plotAudio(frames)