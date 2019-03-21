# Easy-Sound
Why isn't there any simple library to interact with audio inputs/outputs on the computer? Where you could just go like:
**record.startRecording()**

**record.stopRecording()**

for recording and then **record.playRecord()** to play it?? Well, now there is!

## What is Easy-Sound?
Easy sound is a library built on top of PyAudio to allow a simple use of audio interface. It aims to allow record, play, generate audiofiles and much more. It aslo allows to manipulate the audio as a list of integers in order to make signal processing easier!

## How to use it
In the beginning of your script insert:

from Environment import EasySound, Record

EasySound contains some usefull methods to open streams, convert data etc... To open a stream:

ES=EaySound()
stream=ES.openStream()

To create an object of the type record you first need a srream:

rec=Record(stream)

Take a look at the examples to see some functionalities!

## Methods

## Some technical stuff...

