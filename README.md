# Easy-Sound
Why isn't there any simple library to interact with audio inputs/outputs on the computer? Where you could just go like:
**record.startRecording()**

**record.stopRecording()**

for recording and then **record.playRecord()** to play it?? Well, now there is!

## What is Easy-Sound?
Easy sound is a library built on top of PyAudio to allow a simple use of audio interface. It aims to allow record, play, generate audiofiles and much more. It aslo allows to manipulate the audio as a list of integers in order to make signal processing easier!

## How to use it
In the beginning of your script insert:

*import EasySound*

EasySound contains some usefull methods to open streams, convert data etc... To open a stream:

*stream=EasySound.openStream()*

To create an object of the type record you first need a stream:

*rec=EasySound.Record(stream)*

Now is easy to do the basics! For mic recording use *record.startRecording()* and *record.stopRecording()* like mentioned above.

It does much more, take a look at the examples to see some functionalities!

## Methods
The file EasySound contains several useful methods for playing with audio and the object Record. Before starting lets mention what a **frame list** is. A **frame list** is a list which is playable e.g. sounds in this context are stored as a **frame list** (see technical stuff for more)
### EasySound methods
**openStream()** - returns a stream object, allowing to interact with microphone and speakers.

**closeStream(stream)** - closes access to the audio trough the object *stream*

**recordToWav(record, outputFileName)** - Creates a *.wav* file with name *outputFileName* (remember to add .wav) from the record object *record*

**plotAudio(frames)** - plots the audio, you'll look like a professional working with audio signals :sunglasses: 

**produceTone(stream, freq, Volume, time)** - returns a record object with frequency *freq* in Hz, volume *Volume* (from 0 to 32000) and *time* seconds of lenght.

**timeToChunks(time)** - converts a given *time* in seconds to the number of chunks that it represents. (see technical stuff).

**listToFrames(list)** - converts a list of numbers (float or int for example) to a frame list (playable) which is returned **(NOT TESTED)**

**framesToList(frames)** - oposit process, the result is returned as a list of 16bit integers



## Some technical stuff...
### Frame list format
What is a frame list?? well a frame list is a list of chunks of frames. Each chunk of frames contains EasySound.CHUNK frames as a single byte string. Each frame is represented using 16 bits, therefor each CHUNK has EasySound.CHUNK*16 bits. What is a frame?? It is a raw value of the audio.

Put plot of a chunk

Confused?? Lets make a scheme:

Put scheme

