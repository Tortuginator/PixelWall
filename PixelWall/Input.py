import socket, sys, time, datetime, serial
from threading import Thread
import Core, Compression, Frame

class Input():
    def __init__(self):
    	self.distinct = None

    def callData(self,dFrame):
    	raise NotImplementedError;

    def updateSinceLastCall(self):
    	raise NotImplementedError;

class PyGame(Input):
	def __init__(self, pyGameobj):
		self.PYobj = pyGameobj

	def callData(self,dFrame):
		raise NotImplementedError

	def updateSinceLastCall(self):
		raise NotImplementedError

class Function(Input):
    def __init__(self, function):
        self.function = function
        self.args = None

    def callData(self,dFrame):
        if not isinstance(dFrame, Frame.Frame):
            print "[!][PixelWall\Input\Function][callData] please return a", repr(Frame.Frame), "from the function."
            return False

    def updateSinceLastCall(self):
        return True;
		#Allways true, because it should be called each time when it gets called from the engine

class TCPServer(Input):
    def __init__(self, ip = '', port = 4000):
        self.ip = ip
        self.port = port
        self.instance = None
        self.socket = None
        self.buffer = 1024*500
        self.distinct = None
        self.failcounter = 0
        self.maxfails = 3
        self.__fireUp();
        self.args = None

	def setBuffer(self, buffer):
		if buffer != int(buffer) or not buffer > 0:
			return False

		self.buffer = buffer
		return True

	def __fireUp(self):
		self.failcounter += 1
		print "[+][PixelWall\Input\TCPServer][__fireUp] Starting..."
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.ip, self.port))
		self.instance = Thread(target = TCPServer.__srvThread, args = (self, ))
		self.instance.start()
		print "[+][PixelWall\Input\TCPServer][__fireUp] Started"

	@staticmethod
	def __srvThread(self):
		self.socket.listen(1)
		while True:
			connection, client_address = self.socket.accept()
			self.failcounter = 0;
			try:
				print "[+][PixelWall\Input\TCPServer][__srvThread] Client connected " + repr(client_address)
				while True:
					data = connection.recv(self.buffer)
					if len(data) == 0: break
					self.__updateIncoming(data);
					#connection.sendall(data)
				print "[+][PixelWall\Input\TCPServer][__srvThread] Client disconnected " + repr(client_address)
			finally:
				connection.close()
				print "[+][PixelWall\Input\TCPServer][__srvThread] (FORCED) Client disconnected " + repr(client_address)

	def __verify(self, data):
		return Compression.toRawfromLinear(Compression.toLinearfromTransport(data))

    def __updateIncoming(self, data):
        isOK = self.__verify(data);
        self.data = isOK
        self.distinct = True

	def callData(self, dFrame,force = False):
		if not self.distinct is True and force is False:
			return False
		self.distinct = False;
		#Check if server is still running
		if not self.instance.isAlive():
			if self.failcounter >= self.maxfails:
				raise failedToReconnect; #LOOK FOR SOMETHING BETTER
			self.__fireUp();

        third = len(self.data)/3
        for i in range(0, third):
            Y = i // dFrame.width
            X = i % dFrame.width
            dFrame.pixel[X, Y] = (self.data[i], self.data[i+third], self.data[i+third*2])

	def updateSinceLastCall(self):
		return self.distinct;
