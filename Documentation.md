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
### Build in Options
### Custom options
## Different Output options
## Example Animations
