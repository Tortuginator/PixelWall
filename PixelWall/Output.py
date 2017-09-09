import serial, sys, time, datetime,socket,json
sys.path.append('.\PixelWall')
from PixelWall import Core, Exceptions, Compression, Frame,DBSC
from threading import Thread
import RFCA

current_milli_time = lambda: int(round(time.time() * 1000))

class Output():
	def __init__(self):
		pass
	#ABSTRACT
	def output(self, data):
		raise NotImplementedError;

	def autoFPS(self):
		return -100;

class Serial(Output):
	def __init__(self, port = "COM10", compression = "RFCA",loopback = False,baudrate = 1000000):
		self.port = port
		self.baudrate = baudrate
		self.ser = None
		self.initbyte = 200
		self.compression = compression
		self.showrecv = True
		self.skips = 0
		self.loopback = loopback
		self.storage = None
		self.instance = None
		self.CompressionInstance = None
		self.prepared = None
		if self.compression == "RFCA":
			self.CompressionInstance = RFCA.RFCA(LOD = 0);
		self.__fireUp();
		if loopback is True:
			print "[!]WARNING: Loopback on the Serialoutput is Enabled"

	def __fireUp(self):
		if self.loopback is False:
			self.ser = serial.Serial(self.port, self.baudrate, timeout=0.005,bytesize = serial.EIGHTBITS)
		#self.ser.open()
		print "[+]Serial Port Initialized @",self.port,"with baudrate",self.baudrate
		self.instance = Thread(target = Serial.__asyncOutput, args = (self, ))
		self.instance.start()
		pass

	def __prepareData(self, data):
		#data needs to be in raw format
		if not isinstance(data, Frame.Frame):
			raise unexpectedType(variable = "data", type="Frame.Frame")
		if self.compression == "RFCA":
			tmp = data.getColorArr()
			self.CompressionInstance.addFrame(tmp);
			return bytearray(self.CompressionInstance.getByteCode())

		elif self.compression == "RAW":
			tmp = data.getColorArr()
			return bytearray([item for sublist in tmp for item in sublist]);

		elif self.compression == "LINEAR":
			tmp = data.getColorArr()
			tmp = Compression.toLinearfromRaw(tmp)
			return bytearray([item for sublist in tmp for item in sublist])

		print "[!] Compression not found"
	def __correctFormat(self, data):
		#The Firmware currently can only decode RFCA and RAW
		if self.compression == "LINEAR":
			x = 2
		elif self.compression == "RAW":
			x = 0
		elif self.compression == "RFCA":
			x = 3
		init = [self.initbyte, (len(data)+3)//255, (len(data)+3)%255, x]
		tmp = list(bytearray(init) + data + bytearray([233,244,245]))
		#t = DBSC.DBSC(tmp).CalculateShiftMode()
		#print "[+] Length Comparison:",t[1], "VS",len(tmp)," Savings:",len(tmp)-t[1]
		return tmp

	def output(self, data):
		if self.storage !=None:
			self.skips +=1
			print "[!] Skipping Frame"
		self.storage = data

	def __asyncOutput(self):
		framecount = 0
		framesize = 0
		frametime = datetime.datetime.now() + datetime.timedelta(seconds = 1)
		lockSend = False
		print "[+][Serial] Serial async started"
		while True:
			line = ""
			if not self.loopback:line = self.ser.readline()
			if line != "":
				self.handleResponse(line)
				if "RNDcomplete" in line:
					lockSend = False
				if "RCVmissing" in line:
					self.ser.write(tmp)
					print "[!][Serial] Autorecover"
				if self.showrecv is True:
					pass#print line

			if self.storage != None and lockSend is False:
				tmp = self.__correctFormat(self.__prepareData(self.storage))
				if self.CompressionInstance is not None:
					self.CompressionInstance.setLastFrame(self.storage.getColorArr())
				if self.loopback is False:self.ser.write(tmp)
				if frametime < datetime.datetime.now():
					print "[+][Serial] effective FPS:",framecount, "| avg. bypF",framesize/framecount,  "|skips",self.skips,"| total usage",(float(framesize)/(self.baudrate/8))*100,"%"
					framecount = 0
					framesize = 0
					self.skips = 0
					frametime = datetime.datetime.now() + datetime.timedelta(seconds = 1)
				framesize += len(tmp)
				framecount +=1
				self.storage = None
				if not self.loopback:lockSend = True

	def handleResponse(self,response):
		if response == "0RNDfaildivby3":
			print "[!][SERIALDEVICE][RAW] WARNING: Serialdevice skipped one frame, because of a transmission fault [divby3]"
		elif response == "DFFBfrtyNotFound":
			print"[!][SERIALDEVICE] WARNING: Serialdevice skipped one frame, because of a error while interpreting the INIT bytes"
		elif response == "3RNDcounterNmatch":
			print "[!][SERIALDEVICE][RFCA] WARNING: Serialdevice skipped one frame, because of a bufferlength deocding error"
		elif response == "DFFB2notsupp":
			print "[!][SERIALDEVICE][LINEAR] WARNING: Serialdevice skipped one frame, because the compression is not supported"
		elif response == "DFFB3notsupp":
			print "[!][SERIALDEVICE][RFCA] WARNING: Serialdevice skipped one frame, because the compression is not supported"

class BinaryFile(Output):
	def __init__(self, filename = "frame.bin", path = ""):
		self.filename = filename
		self.filepath = path

	def __prepareData(self, data):
		if not isinstance(data, Frame.Frame):
			raise Exceptions.unexpectedType(variable = "data", type="Frame.Frame")
			return False
		a = data.getColorArr()
		return bytearray(a[0] + a[1] + a[2])

	def output(self, data):
		data = self.__prepareData(data);
		if data is None:
			print "[!][PixelWall/Output/BinaryFile][output] Something went wrong."
			return False

		with open(self.filepath + self.filename, "wb") as f:
			f.write(data)

class TCPClient(Output):
	def __init__(self, ip, port = 4000, connectOnInit = True):
		self.ip = ip
		self.port = port
		self.failcounter = 0;
		self.failmax = 3;
		self.socket = None

		if connectOnInit:
			self.__connect();

	def __connect(self, force = False):
		if (self.failcounter >= self.failmax) and not force:
			print "Failed to reconnect"
			exit()
		try:
			print "[+][PixelWall/Output/TCPClient][__connect] Connecting", repr(self.ip), "@", repr(self.port)

			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.ip, self.port))
			self.failcounter = 0

		except Exception, e :
			self.failcounter += 1
			print e
			raise e
			self.__connect()
			print "[!][PixelWall/Output/TCPClient][__connect] Socket excption, trying to reconnect:", repr(e)

	def reconnect(self, force = False):
		self.__connect(force);

	def resetReconnectAttemps(self):
		self.failcounter = 0
		return True

	def __prepareData(self, data):
		if not isinstance(data, Frame.Frame):
			print "[!][PixelWall/Output/TCPClient][__prepareData] wrong type. Excepting:", repr(Frame.Frame)
			return False
		return data.getColorArr()

	def output(self, data):
		data = list(self.__prepareData(data));
		if data is None:
			print "[!][PixelWall/Output/TCPClient][output] Something went wrong."
			return False

		if data is False:
			return False

		if socket == None:
			raise socketNotInitialized;
		try:
			self.socket.send(json.dumps(data))
		except socket.timeout:
			print "[!][PixelWall/Output/TCPClient][output] Socket timeout", repr(self.ip), "@", repr(self.port)
			self.reconnect();
		#Connect
	def close(self):
		self.socket.close();
