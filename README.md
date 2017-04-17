WARNING: this system was only tested with ~1000 LED's

# PixelWall
"PixelWall" is a python implementation to control lots of individual addressable LED's. This engine is the Server-side implementation, meaning it calculates the values for all pixels and sends them to the PixelWall. It supports full 24bit RGB colors and internal RGBA.
The Renderengine is based on PIL. And the digital interface controlling the LED's is a Teensy 3.2

# Input options
The engine offers 3 input options:
 * TCP network stream
 * Pygame [EXPERIMENTAL/PLANNED]
 * Function 

# Output options
The engine offers 3 output options:
 * TCP network stream 
 * File 
 * Serial

The different output formats use different looseless compressions matching their requirements, which enable them to send large amounts of pixels per second. Enabeling you to build even bigger pixelwalls or higher framerates.

# Dasychain
The engine offers the possibility to dasychain multiple engines together. This means, that you run your engine on the Raspberry PI near your Pixelwall and set the input to TCP networkstream. This then allows you to stream content from anywhere in the world to your Pixelwall. 
This is especially usefull for debugging.

# The compression
The engine offers 3 basic types of compression:
 * **RAW** stores the pixels without compression. 
 * **LINEAR** a very basic compression. Allready reducing the size im comparison to the RAW compression by up to 50%
 * **RFCA** (V2.0) is a more advanced compression. It only sends the bytes from the which have changed. This reduces the size by up to 75% im comparison to RAW compression.
 * **OBJECT** [EXPERIMENTAL/PLANNED] this only transmits the objects it self, like Rectangles and Circles. So only the parameters like size,  radius, etc. need to be send. And it will then be rendered on the Clientside. But this requires exactly the same implementation of the objects on the Client and Serverside. And a Client which has the performace to do theese type of calculations near Realtime. 
 
**RFCA** is looseless per default, but is offers non-looseless compression, which can be activated.
since the **LINEAR** compression allread offers a lot of compressen VS. computing performance it is used, when setting the Output to TCP or File.

# Animation Engine
This part of the PixelWall engine, can display bitmaps and is enables you to define animations, which can be dynamic, meaning they can change each iteration or static ones which stay the same throughout each loop.

# DBSC (Dynamic Bit Shift Compression) [EXPERIMENTAL]
This compression needs no context, and works fine with allready compressed data. It can save about 20% of space. Depending on the dataset. This Compression is allready fully implemented serversided. But not Clientwise.

# Requirements
* **Serial** For the Serial Communication to the Teensy
* **PIL** PythonImageLibrary

# Performace
While testing, the Engine was running on a Microsoft surface Pro 4 with intel I7 and 16GB ram. For rendering complex animations at 45fps for a 28x28 pixelwall and sending them via serial, it only took 5% of the processor power.

# The Client aka. Teensy
This system uses a Teensy 3.2 as Client to control all LED's, using the OCTOWS2811 library and shield.
The Firmware currently supports on-the-fly configuration, meaning, that configurations can be made over the Serial connection, without having to reupload the Firmware or having to restart.
It currently supports RFCA and RAW compression

# Getting started
## First Steps
First import the Engine:
```python
import Pixelwall
```
Secondly, we will initialize our Input:
using myframe.img or myframe.pixel you now be able to access the PIL object of each frame when rendered and modify it.
```python
def exampleFunction(myframe):
   pass

myInput = PixelWall.Input.Function(exampleFunction)
```

and then Output:
```python
myOutput = PixelWall.Output.Serial(port = "COM6")
```
or:
```python
myOutput = PixelWall.Output.BinaryFile()
```
then we initialize the engine:
```python
myPixelwall = PixelWall.Engine(width = 32, height = 32, XInput = myInput, XOutput = myOutput, fps = 25)
```
now finally start the engine:
```python
myPixelwall.fireUp()
```
## Animations
using the code from above:
```python
def exampleFunction(myframe):
   pass

myInput = PixelWall.Input.Function(exampleFunction)
myOutput = PixelWall.Output.Serial(port = "COM6")
myPixelwall = PixelWall.Engine(width = 32, height = 32, XInput = myInput, XOutput = myOutput, fps = 25)
myPixelwall.fireUp()
```
we will now add a animation:
```python
gifAnimation = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\example.gif",Position = (-1,-1))
localAnimation = PixelWall.Animations.Animation(rFunc = gifAnimation, startframe = 0, infinity = True, tourCount = 0)
myPixelwall.AnimationManagementSystem.addAimation(localAnimation);
```

## License
*****THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY EXPRESSED OR IMPLIED WARRANTIES. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)*****
