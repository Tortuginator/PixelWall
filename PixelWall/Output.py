import serial,Core,Compression
from threading import Thread
import Frame,Exceptions

class Output():
	def __init__(self):
		pass
	#ABSTRACT
	def output(self,data):
		raise NotImplementedError;

class Serial(Output):
	def __init__(self,port = "COM3"):
		self.port = port
		self.baudrate = 1000000
		self.ser = None

	def __fireUp(self):
		self.ser = serial.Serial(self.port, self.baudrate, timeout=0.5,bytesize = serial.EIGHTBITS)
		self.ser.open()

	#ABSTRACT
	def output(self,data):
		self.ser.write(bytes(data))

class BinaryFile(Output):
	def __init__(self, filename = "output.bin", path = ""):
		self.filename = filename
		self.filepath = path

	def __prepareData(self, data):
		if not isinstance(data,Frame.Frame):
			raise Exceptions.unexpectedType(variable = "data",type="Frame.Frame")
			return False
		return Compression.toTransportfromLinear(Compression.toLinearfromRaw(data.getColorArr()))

	def output(self,data):
		data = self.__prepareData(data);
		print data
		if data is None:
			print "[!][PixelWall/Output/BinaryFile][output] Something went wrong."
			return False
		with open(self.filepath + self.filename, "wb") as f:
			f.write(data)

class TCPClient(Output):
	def __init__(self,ip,port,connectOnInit = True):
		self.ip = ip
		self.port = port
		self.failcounter = 0;
		self.failmax = 3;
		self.socket = None

		if connectOnInit:
			self.__connect();

	def __connect(self,force = False):
		if (self.failcounter >= self.failmax) and not force:
			raise Exceptions.failedToReconnect;
		try:
			print "[+][PixelWall/Output/TCPClient][__connect] Connecting",repr(self.ip),"@",repr(self.port)

			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.ip, self.port))
			self.failcounter = 0
		except Exception,e :
			self.failcounter += 1
			self.__connect()
			print "[!][PixelWall/Output/TCPClient][__connect] Socket excption, trying to reconnect:", repr(e)

	def reconnect(self,force = False):
		self.__connect(force);

	def resetReconnectAttemps(self):
		self.failcounter = 0
		return True

	def __prepareData(self,data):
		if not isinstance(data,Frame.Frame):
			print "[!][PixelWall/Output/TCPClient][__prepareData] wrong type. Excepting:",repr(Frame.Frame)
			return False
		return Compression.toTransportfromLinear(Compression.toLinearfromRaw(data.getColorArr()))

	def output(self,data):
		data = self.__prepareData(data);
		if data is None:
			print "[!][PixelWall/Output/TCPClient][output] Something went wrong."
			return False
		if data is False:
			return False

		if socket == None:
			raise socketNotInitialized;
		try:
			self.socket.send(data)
		except socket.timeout:
			print "[!][PixelWall/Output/TCPClient][output] Socket timeout",repr(self.ip),"@",repr(self.port)
			self.reconnect();
		#Connect
	def close(self):
		self.socket.close();
