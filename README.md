WARNING: this system will most likely not work properly with systems with over 5000 LED's

# PixelWall
"PixelWall" is a python implementation to control lots of individual addressable LED's. This engine is the Server-side implementation, meaning it calculates all pixels and sends it to the PixelWall. It supports full 24bit RGB colors and internal RGBA.
The Renderengine uses PIL.
# TODO list

- [x] Fully implement the compression
- [x] Fully implement the output:TCPclient
- [x] Fully implement the input:TCPserver
- [x] Fully implement the output:serial
- [x] Fully implement the output:callback
- [x] Fully implement the output:toFile (emulator)
- [x] Fully implement basic drawing functions
- [ ] Fully implement halfframes for the animations
- [ ] Fully implement a typeface for 'writeText'
- [ ] Fully implement internal RGBA (internal)
- [ ] Fully implement excptions

# Input options
The engine offers a lot of input options:
 * TCP network stream
 * Pygame [EXPERIMENTAL]
 * Function 

# Output options
The engine offers a lot of output options:
 * TCP network stream 
 * File 
 * Serial

The different output formats use different looseless compressions matching their requirements, which enable them to send large amounts of pixels per second. Enabeling you to build even bigger pixelwalls.
# DBSC (Dynamic Bit Shift Compression)
This is Looseless compression is applied to all outgoing streams. RFCA V2 uses this Compression. DBSC can't be disabled.
This compression checks for each bit how many bits would be saved, if the bits are removed when they are not needed. 
Structure (n-bit mode):
 * **Data Array [DA]** the "cut" bitstrings are stored here. All strings have the length of n bit
 * **Indicator Array [IA]** 1-bit per "cut sequence", which indicated if the number is bigger than the number stored in the "cut sqequence"
 * **Secondary Array [SA]** (8-n)bit array, where the bytes which dont fit in the data array are stored
Single line structure: [Byte] Length DA in bit n*255,[Byte] Length DA in bit +255,[Byte] Length SA in bit n*255,[Byte] Length SA in bit +255,[Byte] Length IA in bit n*255,[Byte] Length IA in bit +255,[DA],[IA],[SA]

For example: *00000111* (7) 8-bit will be shortened in 4 bit mode to *0111* 4-bit. Now a 0 will be stored in IA.
When you have a number *10110110* (182) 8-bit will be shortened in 4-bit mode to *0110*. Now 1 is stored im SA, and therefore indicating, that *1011* is beeing saved in SA.

# Dasychain
The engine offers the possibility to dasychain multiple engines together. This means, that you run your engine on the Raspberry PI near your Pixelwall and set the input to TCP networkstream. This then allows you to stream content from anywhere in the world to your Pixelwall. 
This is especially usefull for debugging.

# The compression
The engine offers 3 basic types of compression:
 * **RAW** stores the pixels without compression. 
 * **LINEAR** a very basic compression. Allready reducing the size im comparison to the RAW compression by up to 50%
 * **RFCA** a more advanced compression, only sending the bytes of the frames which changed between the two frames. This reduces the size by up to 90% im comparison to RAW.
 * **RFCA2** [EXPERIMENTAL] based on the RFCA compression, it only needs 6-bit per color/pixel. Therefor it can display 24bit colors using only 18bit without any loss. In comparison to RFCA it uses about 20% less size.
 * **OBJECT** [EXPERIMENTAL] this only transmits the objects it self, like Rectangles and Circles. So only the parameters like size,  radius, etc. need to be send. And it will then be rendered on the Clientside. But this requires exactly the same implementation of the objects on the Client and Serverside. And a Client which has the performace to do theese type of calculations near Realtime.
 
booth **RFCA** and **RFCA2** are looseless per default, but they offer non-looseless compression, which can be activated.
since the **LINEAR** compression allread offers a lot of compressen VS. computing performance it is used, when setting the Output to TCP or File.

# Animation Engine
This part of the PixelWall engine, can display bitmaps and is enables you to define animations, which can be dynamic, meaning they can change each iteration or static ones which stay the same throughout each loop. I addition it offeres "Halfframe" support, so that Animations running at low FPS look smoother and more refined.

# Requirements
* **Serial** For the Serial Communication to the Teensy
* **PIL** PythonImageLibrary

# Performace
While testing, the Engine was running on a Microsoft surface Pro 4 with intel I7 and 16GB ram. For rendering complex animations at 60fps for a 30x30 pixelwall and sending them via serial, it only took 2% of the processor power.

## License

*****THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY EXPRESSED OR IMPLIED WARRANTIES. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)*****
