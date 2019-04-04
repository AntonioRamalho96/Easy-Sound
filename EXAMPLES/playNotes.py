import EasySound as ES

#Opens a stream
print('openning stream...')
stream=ES.openStream()

#create Record Objects for each tone
input('Done! Press ENTER to load notes')
G=ES.produceTone(stream, 392, 5000, 0.5) #G tone
A=ES.produceTone(stream, 440, 5000.0, 0.5) #A tone
A2=ES.produceTone(stream, 440, 5000.0, 1) #A tone with twice the lenght
A05=ES.produceTone(stream, 440, 5000.0, 0.25) #A tone with 0.5 the lenght
B=ES.produceTone(stream, 493, 5000, 0.5)
B15=ES.produceTone(stream, 493, 5000, 0.75)
C=ES.produceTone(stream, 523, 5000, 0.5)
D=ES.produceTone(stream, 587, 5000, 0.5)
P=ES.produceTone(stream, 0, 0, 0.5) #pause(record with volume=0)

#Plays ode of joy!
input('Done! Press ENTER to play song')
B.playRecord()
B.playRecord()
C.playRecord()
D.playRecord()
D.playRecord()
C.playRecord()
B.playRecord()
A.playRecord()
G.playRecord()
G.playRecord()
A.playRecord()
B.playRecord()
B15.playRecord()
A05.playRecord()
A2.playRecord()
