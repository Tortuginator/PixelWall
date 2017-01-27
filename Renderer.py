import socket,sys
import time,datetime,serial
from threading import Thread

current_milli_time = lambda: int(round(time.time() * 1000))

class CompressionType():
	No = 0
	Linear = 1
	Object = 2

	@staticmethod
	def isCompression(compression):
		if compression in [0,1,2]:
			return True
		return False

class failedToReconnect(Exception):
	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return "The socket tried 3 times in a row to connect to the server without success"+ "\n" + repr(self.value)

class wrongObject(Exception):
	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return "It seems like a other object was expected: "+ "\n" + repr(self.value)

class InvalidCompression(Exception):
	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return "It seems like the Compression given was not recognized "+ "\n" + repr(self.value)

class socketNotInitialized(Exception):
	def __init__(self, value = None):
		self.value = value

	def __str__(self):
		return "The socket was not initialized. I seems like you forgot that when you initialized the <TCPClient>. The socket can be initialized by calling \"reconnect()\""+ "\n" + repr(self.value)

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

class FrameFormat():
	def __init__(self,data = None,compression = None,objects = None):
		if compression == None:
			self.compression = None
		else:
			if CompressionType.isCompression(compression) :
				self.compression = compression
			else:
				raise InvalidCompression;

		self.data = data
		self.objects = objects

	def fromTransport(self,data):
		#Convert:
		data = bytearray(data);
		Ldat = len(data);
		#Structure:
		#[Compression (0,1,2)][EXTRA+6]
		if int(data[0]) in [CompressionType.No,CompressionType.Linear]:
			#[Lengtha1][lengtha2][Lengthb1][lengthb2][lengthc1][lengthc2]
			#totalLength = 255*Lengthxa[0-255] + Lengthxb[0-255]|| MAX: 65280bytes length*3 + 7
			totalLengthR = int(ldat[1]) * 254 + int(ldat[2])
			totalLengthG = int(ldat[3]) * 254 + int(ldat[4])
			totalLengthB = int(ldat[5]) * 254 + int(ldat[6])
			if Ldat != (totalLengthR + totalLengthG + totalLengthB+7):
				UtilPrint.compose("!",self.__class__,__name__,"failed to decode. The lengths do not match. The packet will be ignored.")
				return False
			newdata = [[],[],[]]
			newdata[0] = data[8:8+totalLengthR]
			newdata[1] = data[totalLengthR+8+1:totalLengthG+8+totalLengthR]
			newdata[2] = data[totalLengthG+8+totalLengthR+1:totalLengthG+8+totalLengthR+totalLengthB]
			self.data = newdata
			self.compression = int(data[0])
			return True
		elif int(data[0]) == CompressionType.Object:
			raise NotImplementedError;
		return False

	def toTransport(self,forceRaw = False):
		if self.compression == CompressionType.Object:
			try:
				self.__convObjToRaw();
			except Exception,e:
				print e
		if self.compression == CompressionType.No:
			if not forceRaw:
				self.data = FrameFormat.__convertRawToLin(self.data)
				self.compression = CompressionType.Linear
			else:
				lenR = len(self.data[0])
				lenG = len(self.data[1])
				lenB = len(self.data[2])
				if lenG != lenR != lenB:
					UtilPrint.compose("!",self.__class__,__name__,"the lenghts of the color arrays do not match in RAW mode!")
				header = bytearray([0,lenR//255,lenR%255,lenG//255,lenG%255,lenB//255,lenB%255])
				if type(self.data[0]) == list:
					R = bytearray(self.data[0])

				if type(self.data[1]) == list:
					G = bytearray(self.data[1])

				if type(self.data[2]) == list:
					B = bytearray(self.data[2])

				return (header + R + G + B)

		if self.compression == CompressionType.Linear:
			lenR = len(self.data[0])
			lenG = len(self.data[1])
			lenB = len(self.data[2])
			print [1,lenR//254,lenR%254,lenG//254,lenG%254,lenB//254,lenB%254]
			header = bytearray([1,lenR//254,lenR%254,lenG//254,lenG%254,lenB//254,lenB%254])
			if type(self.data[0]) == list:
				R = bytearray(self.data[0])
				print self.data[0]
			if type(self.data[1]) == list:
				G = bytearray(self.data[1])

			if type(self.data[2]) == list:
				B = bytearray(self.data[2])

			return (header + R + G + B)

	def toRaw(self):
		if self.compression == 0:
			return self.data
		elif self.compression == 1:
			return FrameFormat.__convertLinToRaw(self.data)
		elif self.compression == 2:
			return self.__convObjToRaw()
		return None

	def toLinear(self):
		if self.compression == 0:
			return FrameFormat.__convertRawToLin(self.data);
		elif self.compression == 1:
			return self.data
		elif self.compression == 2:
			self.__convObjToRaw()
			return FrameFormat.__convertRawToLin(self.data)
		return None

	def toObject(self):
		if self.compression == 0:
			return None
		elif self.compression == 1:
			return None
		elif self.compression == 2:
			return self.data;
		return None

	def setSize(self,height,width):
		self.fHeight = height
		self.fWidth = width

	def __convObjToRaw(self):
		self.compression = CompressionType.No
		x = Frame(self.fWidth,self.fHeight)
		x.R = self.data[0]
		x.G = self.data[1]
		x.B = self.data[2]
		for i in self.objects:
			i.Render(x)

		self.data = x.getColorArr()
		self.objects = []
		return True

	@staticmethod
	def __convertLinToRaw(data):
		indicator = 1;
		new = [[],[],[]]
		cnt = -1
		for i in data:
			locked = None
			cnt +=1
			for x in range(0,len(i)):
				if i[x] == indicator:
					if x + 2 <= len(i):
						#[Indicator][Value][Count]
						for r in range(0,i[x+2]+1):
							new[cnt].append(i[x+1])#new value
						locked = x+2;
					else:
						UtilPrint.compose("!","UDN",__name__,"found indicator byte at unintended position please check you indicator bytes")
				elif x <= locked:
					pass
					#to be ignored, because theese are the indicator and value bytes
				else:
					new[cnt].append(i[x])

		len_old = len(data[0])+ len(data[1]) + len(data[2])
		len_new = len(new[0])+ len(new[1]) + len(new[2])
		UtilPrint.compose("+","UDN",__name__,"compression efficiency: " + repr(100-int((float(len_old)/float(len_new))*100)) + "%")
		return new

	@staticmethod
	def __convertRawToLin(data):
		indicator = 1;replacement = 2;new = [[],[],[]];
		for channel in range(0,len(data)):
			temporary = []
			lastPoint = None
			for point in range(0,len(data[channel])):
				if lastPoint != data[channel][point]:
					if len(temporary) <= 3:
						if len(temporary) != 0:
							for i in temporary:
								if i == indicator:
									new[channel].append(replacement)
								else:
									new[channel].append(i)
					else:
						if len(temporary) > 255:
							for i in range(1,(len(temporary)-1)//254):
								new[channel].append(indicator)
								new[channel].append(temporary[0])
								new[channel].append(254)
							new[channel].append(indicator)
							new[channel].append(temporary[0])
							new[channel].append((len(temporary)-1)%254)
						else:
							new[channel].append(indicator)
							new[channel].append(temporary[0])
							new[channel].append(len(temporary)-1)
					lastPoint = data[channel][point]
					temporary = [data[channel][point]]
				else:
					if data[channel][point] == indicator:
						temporary.append(replacement)
					else:
						temporary.append(data[channel][point])

			if len(temporary) > 255:
				for i in range(1,(len(temporary)-1)//254):
					new[channel].append(indicator)
					new[channel].append(temporary[0])
					new[channel].append(254)
				new[channel].append(indicator)
				new[channel].append(temporary[0])
				new[channel].append((len(temporary)-1)%254)
			elif len(temporary) > 0:
				new[channel].append(indicator)
				new[channel].append(temporary[0])
				new[channel].append(len(temporary)-1)
			else:
				if lastPoint == indicator:
					new[channel].append(replacement)
				else:
					new[channel].append(lastPoint)
		print "COMPLETE"
		return new

	def setData(self,data,compression):
		self.data = data
		self.compression = compression

class Output():
	def __init__(self):
		self.type = None
		self.compression = False
		self.fps = 30
		self.supportedCompression = [None]

	def setCompression(self,compression):
		if not type(compression) is bool:
			return False
		self.compression = compression
		return True

	def setFPS(self,fps):
		fps = int(fps)
		if fps <= 0:
			return False
		self.fps = fps
		return True

	#ABSTRACT
	def output(self,data):
		raise NotImplementedError;

class Serial(Output):
	def __init__(self,port = "COM3"):
		self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]
		self.port = port
		self.baudrate = 9600
		self.ser = None
		self.__fireUp();
	def __fireUp(self):
		self.ser = serial.Serial(self.port, self.baudrate, timeout=0.5,bytesize = serial.EIGHTBITS)
		self.ser.close()#WTF?, BUGFIX
		self.ser.open()

	#ABSTRACT
	def output(self,data):
		data = data.toTransport();
		print "Sending", len(data), "bytes"
		self.ser.write(bytes(data))

class BinaryFile(Output):
	def __init__(self, filename = "output.bin", path = ""):
		self.filename = filename
		self.filepath = path
		self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]

	def __prepareData(self, data):
		return data.toTransport()

	def output(self,data):
		print "saving"
		data = self.__prepareData(data);
		print "Datalength:", len(data)
		with open(self.filepath + self.filename, "wb") as f:
			f.write(data)
		print "complete"

class TCPClient(Output):
	def __init__(self,ip,port,connectOnInit = True):
		self.ip = ip
		self.port = port
		self.failcounter = 0;
		self.failmax = 3;
		self.socket = None
		self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]

		if connectOnInit:
			self.__connect();

	def __connect(self,force = False):
		if (self.failcounter >= self.failmax) and not force:
			raise failedToReconnect;
		try:
			UtilPrint.compose("+",self.__class__,__name__,"Connecting ",repr(self.ip),"@",repr(self.port))
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.ip, self.port))
			self.failcounter = 0
		except Exception,e :
			self.failcounter += 1
			self.__connect()
			UtilPrint.compose("+",self.__class__,__name__,"Socket excption, trying to reconnect: ", repr(e))

	def reconnect(self,force = False):
		self.__connect(force);

	def resetReconnectAttemps(self):
		self.failcounter = 0
		return True

	def __prepareData(self,data):
		return data.toTransport();

	def output(self,data):
		data = self.__prepareData(data)
		if socket == None:
			raise socketNotInitialized;
		try:
			self.socket.send(data)
		except socket.timeout:
			UtilPrint.compose("!",self.__class__,__name__,"Socket timeout",repr(self.ip),"@",repr(self.port))
			self.reconnect();
		#Connect
	def close(self):
		self.socket.close();

class Input():
	def __init__(self):
		self.fps = 30
		self.data = None
		self.distinct = None
		self.supportedCompression = [None]

	def setFPS(self,fps):
		fps = int(fps)
		if fps <= 0:
			return False
		self.fps = fps
		return True

	def callData(self):
		raise NotImplementedError;

	def updateSinceLastCall(self):
		raise NotImplementedError;

	def setArgs(self):
		pass #only used sometimes

class PyGame(Input):
	def __init__(self,pyGameobj):
		self.PYobj = pyGameobj
		self.supportedCompression = [CompressionType.No,CompressionType.Linear]

	def callData(self):
		raise NotImplementedError

	def updateSinceLastCall(self):
		raise NotImplementedError

class Function(Input):
	def __init__(self,function):
		self.function = function
		self.supportedCompression = [CompressionType.No,CompressionType.Object]
		self.args = None

	def callData(self):
		X = self.function(self.args);
		#def __init__(self,data = None,compression = None,objects = None):
		return FrameFormat(data = X.getColorArr(),compression = CompressionType.Object,objects = X.getObjects())

	def updateSinceLastCall(self):
		return True;
		#Allways true, because it should be called each time when it gets called from the engine
	def setArgs(self,args):
		self.args = args

class TCPServer(Input):
	def __init__(self,ip = '',port = 4000):
		self.ip = ip;
		self.port = port;
		self.instance = None
		self.socket = None
		self.buffer = 1024*500
		self.distinct = None
		self.failcounter = 0
		self.maxfails = 3
		self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]
		self.__fireUp();

	def setBuffer(self,buffer):
		if buffer != int(buffer) or not buffer > 0:
			return False

		self.buffer = buffer
		return True

	def __fireUp(self):
		self.failcounter += 1
		UtilPrint.compose("+",self.__class__,__name__,"Starting...")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.ip,self.port))
		self.instance = Thread(target = TCPServer.__srvThread, args = (self, ))
		self.instance.start();
		UtilPrint.compose("+",self.__class__,__name__,"Started")

	@staticmethod
	def __srvThread(self):
		self.socket.listen(1)
		while True:
			connection, client_address = self.socket.accept()
			self.failcounter = 0;
			try:
				UtilPrint.compose("+",self.__class__,__name__,"Client connected " + repr(client_address))
				while True:
					data = connection.recv(self.buffer)
					if len(data) == 0: break
					self.__updateIncoming(data);
					#connection.sendall(data)
				UtilPrint.compose("+",self.__class__,__name__,"Client disconnected " + repr(client_address))
			finally:
				connection.close()
				UtilPrint.compose("+",self.__class__,__name__,"Client disconnected "+ repr(client_address))

	def __verify(self,data):
		return FrameFormat.fromTransport(data);

	def __updateIncoming(self,data):
		isOK = self.__verify(data);
		if isOK is not False:
			self.data = isOK
			self.distinct = True
		else:
			UtilPrint.compose("!",self.__class__,__name__,"Recived corrupt package data. Dumping Frame")

	def callData(self,force = False):
		if not self.distinct is True and force is False:
			return False
		self.distinct = False;
		#Check if server is still running
		if not self.instance.isAlive():
			if self.failcounter >= self.maxfails:
				raise failedToReconnect; #LOOK FOR SOMETHING BETTER
			self.__fireUp();
		return self.data

	def updateSinceLastCall(self):
		return self.distinct;

class TimeTrigger():
	def __init__(self,timesPerSecond,function,args):
		self.timesPerSecond = timesPerSecond
		self.function = function
		self.args = args
		self.__setVars();
		self.isSleeping = True
		self.next = datetime.datetime.now()

	def __setVars(self):
		self.msDelta = float(1)/float(self.timesPerSecond)

	def isDue(self):
		if self.next < datetime.datetime.now():
			return True
		return False

	def doExecute(self, args = None):
		if self.isDue() is False:return False;
		self.next = datetime.datetime.now() + datetime.timedelta(seconds = self.msDelta)
		if args != None:
			self.args = args
		self.isSleeping = False
		self.function(self.args);
		self.isSleeping = True
		return True

class TimeManager():
		def __init__(self):
			self.baseFrequency = 120
			self.instance = None
			self.triggers = []

		def fireUp(self):
			self.instance = Thread(target = TimeManager.__tmeThread, args = (self,self.triggers))
			self.instance.start();

		def __tmeThread(self,triggers):
			#innerTiming = datetime.datetime.now()
			innerStep = 0
			innerMicrosecondDelta = (int(float(1)/float(self.baseFrequency))*100000)
			while(True):
				#if not(innerStep*innerMicrosecondDelta <= ((datetime.datetime.now() - innerTiming).microseconds)):
				if innerStep*innerMicrosecondDelta > current_milli_time():
					time.sleep(0.001)
					continue
				#Start Inner Time measurenemt, for Calculations
				if innerStep >= self.baseFrequency-1:
					innerStep = 0
					innerTiming = datetime.datetime.now()
				innerStep +=1
				for i in triggers:
					if i.isSleeping is True:
						try:
							i.doExecute()
						except Exception,e:
							UtilPrint.compose("!",self.__class__,__name__,"Exception occured for " + repr(i.function)  + " @iteration " + repr(innerStep))
							UtilPrint.compose("!",self.__class__,__name__,repr(e))

		def __tmeExec(self,function,args):
			pass

class FrameFunction():
	def __init__(self):
		raise NotImplementedError

	def Render(self,dFrame):
		raise NotImplementedError

	def Object(self):
		raise NotImplementedError

class Rectangle(FrameFunction):
	def __init__(self,startPoint,endPoint,color,opacity):
		self.color = color
		self.startPoint = startPoint
		self.endPoint = endPoint
		self.opacity = opacity

	def Render(self,dFrame):
		if not Frame.isColor(self.color):return 0;
		Yoffset = self.endPoint.Y - self.startPoint.Y
		if Yoffset >= 0:
			Yoffset +=1;
		else:
			Yoffset -=1;

		Xoffset = self.endPoint.X - self.startPoint.X
		if Xoffset >=0:
			Xoffset += 1;
		else:
			Xoffset -= 1;

		for p in range(0,Yoffset):
			if not dFrame.isPixel(self.startPoint.X,self.startPoint.Y+p):continue;
			Ioffset = dFrame.getOffset(self.startPoint.X,self.startPoint.Y+p)
			for i in range(0,Xoffset):
				dFrame.R[Ioffset+i] = int(self.color[0]*self.opacity)
				dFrame.G[Ioffset+i] = int(self.color[1]*self.opacity)
				dFrame.B[Ioffset+i] = int(self.color[2]*self.opacity)

		def Object(self):
			return (self.startPoint,self.endPoint,self.color,self.opacity)

class Circle(FrameFunction):
	def __init__(self,centerPoint,color,radius,fill = False,fillcolor = 0,opacity = 1):
		self.centerPoint = centerPoint
		self.color = color
		self.radius = radius
		self.fill = fill
		self.fillcolor = fillcolor
		self.opacity = opacity

	def Render(self,dFrame):
		x0 = self.centerPoint.X
		y0 = self.centerPoint.Y
		if dFrame.isColor(self.color) is False:return 0;
		colour = Frame.isColor(self.color);
		#if Frame.isColor(fillColor) is False:return 0;
		if self.radius <= 0:	return 0;

		#Adjust the location

		f = 1 - self.radius
		ddf_x = 1
		ddf_y = -2 * self.radius
		x = 0
		y = self.radius
		self.setPixel(x0, y0 + self.radius, colour,merge = True,ignore = True)
		self.setPixel(x0, y0 - self.radius, colour,merge = True,ignore = True)
		self.setPixel(x0 + self.radius, y0, colour,merge = True,ignore = True)
		self.setPixel(x0 - self.radius, y0, colour,merge = True,ignore = True)
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			self.setPixel(x0 + x, y0 + y, colour,merge = True,ignore = True)
			self.setPixel(x0 - x, y0 + y, colour,merge = True,ignore = True)
			self.setPixel(x0 + x, y0 - y, colour,merge = True,ignore = True)
			self.setPixel(x0 - x, y0 - y, colour,merge = True,ignore = True)
			self.setPixel(x0 + y, y0 + x, colour,merge = True,ignore = True)
			self.setPixel(x0 - y, y0 + x, colour,merge = True,ignore = True)
			self.setPixel(x0 + y, y0 - x, colour,merge = True,ignore = True)
			self.setPixel(x0 - y, y0 - x, colour,merge = True,ignore = True)

	def Object(self):
		return (self,centerPoint,color,radius)

class Text(FrameFunction):
	def __init__(self,positionY,text,color):
		self.text = text
		self.color = color
		self.positionY = positionY

	def Render(self,dFrame):
		if not Frame.isColor(self.color):return 0;
		if not self.isPixel(self.position.X,self.position.Y):return 0;
		spaces = {"!":1,"|":1,":":1,".":1}
		chars = {	"0":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,0)],
					"1":[(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,4),(0,3)],
					"2":[(0,0),(1,0),(2,0),(0,1),(1,2),(2,3),(2,4),(1,5),(0,4)],
					"3":[(0,0),(1,0),(2,1),(1,2),(2,3),(1,4),(0,4)],
					"4":[(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4),(0,5),(2,3),(2,4)],
					"5":[(0,1),(1,0),(2,1),(1,3),(0,3),(0,4),(0,5),(1,5),(2,5),(2,2)],
					"6":[(0,1),(0,3),(1,0),(2,1),(1,2),(0,4),(1,5),(2,5),(0,2)],
					"7":[(0,0),(0,1),(1,2),(1,3),(2,4),(0,5),(1,5),(2,5)],
					"8":[(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(0,3),(2,3),(0,4),(1,4),(2,4)],
					"9":[(2,0),(2,1),(2,2),(2,3),(2,4),(1,4),(0,4),(0,3),(0,2),(1,2)],

					"a":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,2)],
					"b":[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(2,0),(1,2),(2,2),(2,1)],
					"c":[(0,0),(0,1),(0,2),(1,0),(2,0),(1,2),(2,2)],
					"d":[(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(0,1),(0,2),(1,2)],

					"-":[(0,2),(1,2),(2,2)],
					"_":[(0,0),(1,0),(2,0)],
					":":[(0,1),(0,3)],
					".":[(0,0)],
					"|":[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)],
					"!":[(0,0),(0,2),(0,3),(0,4),(0,5)],
					"+":[(1,1),(1,2),(1,3),(0,2),(2,2)]}
		given = list(text)
		pos = 0;
		for i in text:
			if i in chars:
				for p in chars[i]:
					self.setPixel(pos+p[0],self.positionY-p[1],color,ignore = True)
			if i in spaces:
				pos +=1+spaces[i]
			else:
				pos +=4;

class Frame():
	def __init__(self,height,width):
		self.height = height;
		self.width = width;
		self.PixelCount = height*width
		self.FunctionStorage = []
		self.R = [0 for i in range(0,self.PixelCount)]
		self.G = [0 for i in range(0,self.PixelCount)]
		self.B = [0 for i in range(0,self.PixelCount)]
		self.object = []
	def __str__(self):
		return self.R,self.G,self.B
	def __add__(self,other):
		if not self.PixelCount == other.PixelCount:
			return #EXCEPTION
		for i in range(0,self.PixelCount):
			self.R[i] = (other.R[i]+self.R[i])/2
			self.G[i] = (other.G[i]+self.G[i])/2
			self.B[i] = (other.B[i]+self.B[i])/2

	def __sub__(self,other):
		if not self.PixelCount == other.PixelCount:
			return #EXCEPTION
		for i in range(0,self.PixelCount):
			self.R[i] -= other.R[i]
			if self.R[i] < 0:
				self.R[i] = 0
			self.G[i] = other.G[i]
			if self.G[i] < 0:
				self.G[i] = 0
			self.B[i] = other.B[i]
			if self.B[i] < 0:
				self.B[i] = 0

	def AddObject(self,obj):
		self.object.append(obj);

	def getObjects(self):
		return self.object

	def getColorArr(self):
		return [self.R,self.G,self.B]

	def __getPixel(self,X,Y):#WARNING no checks performed
		return self.getPixel(X,Y,True);

	def getOffset(self,X,Y):
		return (Y*self.width)+X;

	def getPixel(self,X,Y,performance = False):
		if not performance :
			if not self.isPixel(X,Y):return [];
		Ioffset = self.getOffset(X,Y);
		return [self.R[Ioffset],self.G[Ioffset],self.B[Ioffset]];

	def isPixel(self,X,Y):
		if not X <= self.width-1:
			return False
		if not Y <= self.height-1:
			return False
		return True

	def __setPixel(self,X,Y,color):#WARNING, no checks will be performed
		return self.setPixel(X,Y,color,merge = True)

	def setPixel(self,X,Y,color,merge = False,offset = -1):
		if not self.isPixel(X,Y):
			return 0
		if not Frame.isColor(color):
			return 0

		if offset != -1:
			Ioffset = offset;
			if not self.PixelCount < Ioffset:
				return 0
		else:
			if not X >= 0 or not Y >= 0:return 0;
			Ioffset = self.getOffset(X,Y);

		if (self.R[Ioffset] != 0 or self.G[Ioffset] != 0 or self.B[Ioffset] != 0) and merge == True:
			self.R[Ioffset] = color[0]/2 + self.R[Ioffset]/2
			self.G[Ioffset] = color[1]/2 + self.G[Ioffset]/2
			self.B[Ioffset] = color[2]/2 + self.B[Ioffset]/2
		else:
			self.R[Ioffset] = color[0]
			self.G[Ioffset] = color[1]
			self.B[Ioffset] = color[2]

		return 1

	@staticmethod
	def mixGradientColor(colorA,colorB,steps,step):
		if not Frame.isColor(colorA):return 0
		if not Frame.isColor(colorB):return 0

		colorC = []
		colorC.append(colorA[0] + (colorA[0]-colorB[0])*(step/steps))
		colorC.append(colorA[1] + (colorA[1]-colorB[1])*(step/steps))
		colorC.append(colorA[2] + (colorA[2]-colorB[2])*(step/steps))
		return (int(colorC[0]),int(colorC[1]),int(colorC[2]))

	@staticmethod
	def isColor(color):
		if not 0 <= int(color[0]) <= 255:
			return False
		if not 0 <= int(color[1]) <= 255:
			return False
		if not 0 <= int(color[2]) <= 255:
			return False
		return (int(color[0]),int(color[1]),int(color[2]))

class Pixel():
	def __init__(self,X,Y):
		self.X = X
		self.Y = Y

class Color():
	def __init__(self,R,G,B):
		self.R = R
		self.G = G
		self.B = B

	def isColor(self):
		if not 0 <= self.R<= 255:
			return False
		if not 0 <= self.G <= 255:
			return False
		if not 0 <= self.B <= 255:
			return False
		return True

	def get(self):
		return (self.R,self.G,self.B)

	def mix(self,colorB):
		raise NotImplementedError

class Engine():
	def __init__(self,height,width,Xinput,Xoutput):
		self.baseFrequency = 30
		self.frameHeight = height
		self.frameWidth = width
		self.brightness = float(1)
		self.Xinput = Xinput
		self.Xoutput = Xoutput
		self.lastFrame = None

	def fireUp(self):
		self.TimeManagementSystem = TimeManager();
		self.RenderTrigger = TimeTrigger(self.baseFrequency,Engine.Render,self)
		self.TimeManagementSystem.triggers.append(self.RenderTrigger)
		self.TimeManagementSystem.fireUp();

	def __adjustBrightness(self):
		raise NotImplementedError

	def setBrightness(self,brightness):
		raise NotImplementedError

	def getBrightness(self):
		return self.brightness;

	def Render(self):
		dFrame = Frame(self.frameHeight,self.frameWidth)
		updatedFrame = self.Xinput.updateSinceLastCall()
		if not updatedFrame:
			return
		self.Xinput.setArgs(dFrame)
		A = self.Xinput.callData()
		try:
			A.setSize(self.frameHeight,self.frameWidth);
			self.Xoutput.output(A)
			self.lastFrame = A
		except Exception,e:
			print e

if __name__ == "__main__":
	def testRND(dFrame):
		try:
			p = Rectangle(Pixel(0,0),Pixel(0,26),(100,100,100),1)
			dFrame.AddObject(p);
		except Exception,e:
			print e
		return dFrame
	F = Function(testRND);
	#O = BinaryFile()
	O = Serial(port = "COM10")
	R = Engine(28,28,F,O)
	R.baseFrequency = 2
	R.fireUp();
