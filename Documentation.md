# Documentation
## Getting started

## Different Input options
Basically there are 3 different output options
### Serial output
The serial output is the connection to the teensy. In Theory the output could be exchanged while being executed. This would work, bug might lead to problems.
```python
OutOptionOne = PixelWall.Output.Serial(port = "COM6", compression = "RFCA", loopback = False)
```
parameters:

parameter | value | default | optional
--- | --- | --- | ---
port | The Windows/Linux serial port | None | No
compression | the Compression algorithm used | "RFCA" | Yes
loopback | Simulates the serial output | False | Yes
baudrate | sets the Baudrate of the Serial connection | 1000000 | Yes

the compression parameter can be used with `"RAW","LINEAR", "RFCA"` compression.
there are muliple inner variables/options like `self.initbyte, self.skips, CompressionInstance, self.showrecv` which can be modified

### Binary output
Saves the image in raw format in a binary file non compressed
```python
OutOptionTwo = PixelWall.Output.BinaryFile(path = "",filename = "example.bin")
```
parameters:

parameter | value | default | Optional
--- | --- | --- | ---
path | path to the file | "" | Yes
filename | filename of the file where the frame will be saved to | frame.bin | Yes

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

there are interal options like `self.failmax or self.failcounter` which control the reconnect attempts

### Custom Output
```python
class Output():
	def __init__(self):
	def output(self, data):
	def autoFPS(self):
```
in general you **NEED** support, when you create a new output option, following functions:
*`__init__` to initialize your instance
*`óutput` this is the function which recieves the data in a color channel array ( `[[],[],[]]`)

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
Currently there are 5 Different Example Animations / Functions / Generators

### Matrix (Matrix.py)

### GIF (GIF.py)
As the title allready says. This Animation is capable of playing Gifs
```python
exampleGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Boxes.gif",Position = (-2,-2))
Ani = PixelWall.Animations.Animation(rFunc = exampleGIF, startframe = 0, infinity = True, tourCount = 0)
```
Parameters:

parameter | value | default | Optional
--- | --- | --- | ---
path | the  path and filename to the Gif file | "" | No
position | the top left position of the gif | (0,0) or (-2,-2) | Yes

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

### Clock (Clock.py)

### Circle2 (Circle2.py)

