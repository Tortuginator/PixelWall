import serial
import sys

scon = serial.Serial("COM10", 9600, timeout=0.5,bytesize = serial.EIGHTBITS)
scon.close()
scon.open()


testscreen = bytearray([200,0,11,0,100,200,200,100,100,200,200,100,100,200,200,100])
scon.write(bytes(testscreen))
lastVal = False
while True:
	x = scon.readline() 
	if x != "":
		print x