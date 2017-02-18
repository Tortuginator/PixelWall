import time
from threading import Thread

class Point():
	def __init__(self,X,Y):
		self.x = X
		self.y = Y

class Color():
	def __init__(self,R,G,B):
		self.r = R
		self.g = G
		self.b = B

	def isColor(self):
		if not 0 <= self.r <= 255:
			return False
		if not 0 <= self.g <= 255:
			return False
		if not 0 <= self.b <= 255:
			return False
		return True

	def get(self):
		return (self.r,self.g,self.b)

	def mix(self,colorB):
		raise NotImplementedError

class CompressionType():
	No = 0
	Linear = 1
	Object = 2

	@staticmethod
	def isCompression(compression):
		if compression in [0,1,2]:
			return True
		return False

def current_milli_time():
    return lambda: int(round(time.time() * 1000))


class PrintRegister():
	def __init__(self):
		self.currentlyPrinting = False
		self.instance = None
		self.register = []
		self.__fireUp();

	def __fireUp(self):
		self.instance = Thread(target = PrintRegister.__print, args = (self, ))
		self.instance.start();

	def __print(self):
		for i in self.register:
			print i
		#reset
		self.register = []

	def doPrint(self,out):
		if not self.instance.isAlive:
			self.__fireUp();
		self.register.append(out);


global PNR
PNR = PrintRegister();
class UtilPrint():
	@staticmethod
	def compose(sign,parent,function,message):
		PNR.doPrint("[" + sign  + "][" +repr(parent)+ "][" +repr(function) + "] " + message)
