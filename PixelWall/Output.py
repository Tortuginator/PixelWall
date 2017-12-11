import serial, sys, time, datetime,socket,json
sys.path.append('.\PixelWall')
from PixelWall import Frame, DBSC
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
		self.compression = compression
		self.loopback = loopback
		self.baudrate = baudrate
		self.instance = None
		self.backlog = 0
		self.tmpContent = None
		self.stattime = current_milli_time() +1000
		self.statcount = 0
		self.statlen = 0
		self.statre = 0
		self.Reader = None
		self.__fireUp()
		self.sendq = None
		self.Writer = None

	def __fireUp(self):
		if self.loopback is False:
			self.interface = serial.Serial(self.port, self.baudrate, timeout=0.005,bytesize = serial.EIGHTBITS)
		print "[+]Serial Port Initialized @",self.port,"with baudrate",self.baudrate
		if self.Reader==None:
			self.Reader = Thread(target = Serial.__asyncRead, args = (self, ))
			self.Reader.start()

	def output(self,content):
		while(self.backlog != 0 and self.loopback is False):
			time.sleep(0.003)
		if self.Writer == None:
			self.Writer = Thread(target = Serial.__asyncSend, args = (self,))
			self.Writer.start()
		self.sendq = content

	def __asyncSend(self):
		while True:
			try:
				if self.sendq != None:
					if self.stattime <= current_milli_time():
						if self.statcount !=0 and self.baudrate != 0:
							print "[+][Serial] effective FPS: " + str(self.statcount)+ "| avg. bypF " + str(self.statlen/self.statcount)+ " | Re "+str(self.statre)+" | total usage "+str(int((float(self.statlen)/(self.baudrate/8))*100))+"%"
							self.stattime = current_milli_time()+1000
							self.statcount = 0
							self.statlen = 0
							self.statre = 0
					if self.sendq != None:
						self.backlog = 1
						self.statlen+=len(self.sendq)
						self.statcount+=1
						self.tmpContent = self.sendq
						if not self.loopback:self.interface.write(self.sendq)
						self.sendq = None
			except Exception,e:
				print e

	def __asyncRead(self):
		while True:
			line = ""
			if not self.loopback:line = self.interface.readline()
			if line != "":
				print line
				if "RNDcomplete" in line:
					self.backlog = 0
				if "RCVmissing" in line:
					#print line
					self.statre +=1
					self.interface.write(self.tmpContent)

	def sendImage(self,content,RFCA = True,RAW = False):
		assert RFCA != RAW,"Only one option can be selected"
		if RFCA:
			self.output(Serial.buildpackage(ID = 1,Content = content))
		elif RAW:
			self.output(Serial.buildpackage(ID = 0,Content = content))
		else:
			print "error RAW RFCA match"

	@staticmethod
	def buildpackage(ID,Content):
		if Content == None:
			return None
		init = [200, len(Content)//255, len(Content)%255,len(Content)%71,ID,Serial._datachecksum(Content)]
		print init
		if Content is None:
			return init
		else:
			return init + list(Content)
	@staticmethod
	def _datachecksum(data):
		sum = 0;
		for i in range(0,len(data)):
			if (i % 5) == 0:
				sum = sum + data[i]%7;
			elif (i%7) == 0:
				sum = sum + data[i]%5;
			elif (i%11) == 0:
				sum = sum + data[i]%1;
			elif (i%13) == 0:
				sum = sum + data[i]%13;
			elif (i%17) == 0:
				sum = sum + data[i]%17;
			elif (i%19) == 0:
				sum = sum + data[i]%19;
			elif (i%3) == 0:
				sum = sum + data[i]%3;
			else:
				sum = sum + data[i];
  		return (sum/255)
#Protocoll

#SENDER CONSTRUCT EXPRESSION

#New Packet Sequence
####	200

#Abort Packet Sequence
####	001 - 001 - 002 - 002

#Header Packet Sequence
####	[LENGTH (1)] - [LENGTH (2)] - [TYPE/COMPRESSION] + [ID] + [CONTENT atLENGHT]

#TYPE/COMPRESSION
#000 - SETTINGS
#100 - IMAGE

#IMAGE ID
#101 - IMAGE / RAW
#102 - IMAGE / RFCA

#SETTING ID[Length]
#000 - Packet Recieved [000]
#001 - Packet Aborted [000]
#002 - No Packet to Abort [000]
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
