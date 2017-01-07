WARNING: this system will most likely not work properly with systems with over 5000 LED's

# PixelWall
"PixelWall" is a python implementation to control lots of individual addressable LED's. This engine is the Server-side implementation, meaning it calculates all pixels and sends it to the PixelWall. It supports full 24bit RGB colors and internal RGBA.
The PixelWall system is divided into two main parts the RenderEngine and the Frame. The Frame represents only one frame and takes care of all pixels and the colors. The RenderEngine contains some basic drawing functions and more advanced ones like Animations and takes care of the Rendering and the correctly timed output.

#TODO list

-[ ]Fully implement the compression
-[ ]Fully implement the output:TCPclient
-[ ]Fully implement the input:TCPserver
-[ ]Fully implement the output:serial
-[ ]Fully implement the output:callback
-[x]Fully implement the output:toFile (emulator)
-[x]Fully implement basic drawing functions
-[ ]Fully implement halfframes for the animations
-[ ]Fully implement a typeface for 'writeText'
-[ ]Fully implement internal RGBA (internal)
-[ ]Fully implement excptions

#Animation presets
In the second python file you will find some basic animations and examples. As well es test screens to check the performance and every pixel of your screen.

#Example
The Repository includes a file called "test.py". This file includes a setup with all basic functions.

#Client-side implementation
To follow...

#Output options
The engine offers a lot of output options:
-TCP network stream 
-to file 
-to emulator
-to Serial
and offers a compression, so that more than 15000 pixels a second (22x22 pixels @30fps with 255*255*255 RGB colors) are easily posible over a serial port.

#Basic commands


#The compression
The compression currently is in a very early state. Basic commands like setPixel, setRectagle, writeText, drawCircle should work properly when used statically in the external rendering function or in a Animation. But the compression will most likely mess with the transparency of some colors.

#Debugging
I recommand to run a server instance on the PixelWall's computer (RaspberryPI) and connect it to the local Network. Then you can debug using your normal computer and set the output to TCPclient to stream the image to the PixelWall.
The second options is to use the local emulator. It runs in any modern webbrowser and can display up to 45fps


THIS PROGRAMM/SCRIPT IS OFFERED WITHOUT ANY WARRANTY OR WHAT SO EVER AND CAN NOT BE HELD LIABLE FOR ANY DAMAGES...
