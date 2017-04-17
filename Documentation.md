# Documentation
## Getting started

## General
### Frame data Structure
The frame's datastructure is a simple 2-Dimensional list with three sublists. One for reach color. The Pixels are simply saved in this list, without any position information. The position will later be recovered, by using modulo width on the index of the sub-list
Basically: `[Red[],Green[],Blue[]]`

## Different **input** options
Basically there are 3 different output options
### Serial output
The serial output is the connection to the teensy. In theory the output could be exchanged while being executed. This would work, but might lead to problems.
```python
OutOptionOne = PixelWall.Output.Serial(port = "COM6", compression = "RFCA", loopback = False)
```
parameters:

parameter | value | default | optional
--- | --- | --- | ---
port | The Windows/Linux serial port | None | No
compression | The compression algorithm used | "RFCA" | Yes
loopback | Simulates the serial output | False | Yes
baudrate | Sets the baudrate of the serial connection | 1000000 | Yes

The compression parameter can be used with `"RAW","LINEAR", "RFCA"` compression.
There are muliple inner variables/options like `self.initbyte, self.skips, CompressionInstance, self.showrecv` which can be modified

### Binary output
Saves the image in raw format in a binary file non compressed
```python
OutOptionTwo = PixelWall.Output.BinaryFile(path = "",filename = "example.bin")
```
parameters:

parameter | value | default | Optional
--- | --- | --- | ---
path | Path to the file | "" | Yes
filename | Filename of the file where the frame will be saved to | "frame.bin" | Yes

### TCP output
This output options makes it possible, to setup a TCP client, connecting to a TCP server and sending the output frame of this instance.
Currently the data sending process and encoding, works, but is very sloppy. This will be imporved in the future.
```python
OutOptionThree = PixelWall.Output.TCPClient(ip = "172.0.0.1", port = 4000, connectOnInit = True)
```
parameters:

parameter | value | default | Optional
--- | --- | --- | ---
ip | the IP of the server | None | No
port | the Port of the server | 4000 | Yes
connectOnInit | makes it possible to later connect to the server and not instantly | True | Yes

There are interal options like `self.failmax or self.failcounter` which control the reconnect attempts

### Custom Output
```python
class Output():
	def __init__(self):
	def output(self, data):
	def autoFPS(self):
```
in general you **NEED** support, when you create a new output option, following functions:
* `__init__` to initialize your instance
* `óutput` this is the function which recieves the data in a color channel array ( `[[],[],[]]`)

so your code should look then like this:
```python
class MyOwnOutput(PixelWall.Output):
  def __init__(some,option)
    #my code
    pass
   
   def output(self,data):
    #do something with my data
    pass
```
and then your output module should work fine
## Example Animations
Currently there are 5 different example Animations / Functions / Generators

### Matrix (Matrix.py)
The Matrix generator procudes a black image with particles falling down from the top, leaving a trace. Basically the typical Hackerlike "Hackerscreen" from the original Movie "The Matrix"

```python
exampleMatrix = PixelWall.PresetAnimations.Matrix.Matrix()
Ani = PixelWall.Animations.Animation(rFunc = exampleMexample, startframe = 0, infinity = True, tourCount = 0)
```
Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
Color | The Color of the fading particles | `(0,255,0)` | Yes
Length | The length of the fade | 10 | Yes
TipColor | The color of the Tip, the Particle | `self.Color` | Yes

Unless otherwise set, the `Tipcolor` is allways the same as the normal Color parameter, therefore optional.

### GIF (GIF.py)
As the title allready says. This Animation is capable of playing Gifs
```python
exampleGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Boxes.gif",Position = (-2,-2))
Ani = PixelWall.Animations.Animation(rFunc = exampleGIF, startframe = 0, infinity = True, tourCount = 0)
```
Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
path | The  path and filename to the Gif file | "" | No
position | The top left position of the gif | (0,0) or (-2,-2) | Yes

Be aware, that PIL does not corretly interpret GIFs with transparent as color.
Some example GIFs are in the GIF folder in the parent dictionary.

### Game of Live (GameOfLive.py)
This Animation is a standart implementation of the famous Game of Live. It uses the "offical" rules.
```python
exampleGoF = PixelWall.PresetAnimations.GameOfLife.GameOfLife(position = (10,10),pattern = [[0,1,1],[1,1,0],[0,1,0]])
Ani = PixelWall.Animations.Animation(rFunc = exampleGoF, startframe = 0, infinity = True, tourCount = 0)
```
Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
position | the position for the patter. Top-left. | (0,0) | Yes
pattern | the start pattern out of `1 and 0`. saved as array like [[0,1,1],[1,0],[1,1,1,1]]. One sub-list per row. | None | Yes
rules | this uses the default ruleset. but it can be customized, by referencing a new function | `GameOfLive.Rules` | Yes
color | the color of the living pixels | (255,255,255,255) | Yes

There are some well known examples in the comment upper section of the file for the pattern parameter.
In general a rules function should look like this (excerpt from the GameOfLive.py)

```python
def Rules(input,isalive):
	count = GameOfLife.countlivingCells(input)
        if count == 2 and isalive == 1:
            return 1#LIVE
        elif count == 3:
            return 1#LIVE
        return 0
```

### Chill (Chill.py)
The Chill generator produces random pixels with random colors, which are Fading-IN/OUT. Controlled by a COS curve. This is later blurred to create a calm image with slow moving circles and shaped.
```python
exampleChill = PixelWall.PresetAnimations.Chill.Chill(ColorLower=(150,100,0),ColorHigher = (255,200,0))
Ani = PixelWall.Animations.Animation(rFunc = exampleChill, startframe = 0, infinity = True, tourCount = 0)
```
To Clarify, speed is ment by how many colorsteps from 0 to 255 the pixel gets forward for each frame calculated
Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
ColorLower | The lower limit for the random colors | `(100,100,100)` | Yes 
ColorHigher | The upper limit of the random colors | `(255,255,255)` | Yes
Points | The number of piles which are calculated and later blurred | 80 | Yes
SpeedMin | The minimal amount of speed | 0.05 | Yes
SpeedMax | The maximal amount of speed | 2.0 | Yes

### Clock (Clock.py)
The clock is a system, which shows the time in a 24H format, by placing faded Circles. Theese are fully animated

Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
ColorSeconds | The color of the circle showing the Seconds | `(0,0,200)` | Yes
ColorMinutes | The color of the circle showing the Minutes | `(0,200,0)` | Yes
ColorHours | The color of the circle showing the Hours | `(200,0,0)` | Yes
CenterPosition | The Center of the clock, usually the center of the screen | None | No
HoursRad | The (additional-)radius of the hour circle | 10 | Yes
MinutesRad | The (additional-)radius of the minutes circle | 10 | Yes
SecondsRad | The (additional-)radius of the seconds circle | 10 | Yes
Interpolate | The values for minutes are calculated and displayed more smoothly, but still acurate | True | Yes

### Circle2 (Circle2.py)

## Custom Drawing Functions (Drawing.py)

