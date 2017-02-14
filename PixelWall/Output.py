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
