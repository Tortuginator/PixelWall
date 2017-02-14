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
			Core.UtilPrint.compose("!",self.__class__,__name__,"Recived corrupt package data. Dumping Frame")

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
