import serial


class Output:
	def __init__(self):
		pass

	def output(self, data):
		raise NotImplementedError;


class SimpleSerial(Output):
	def __init__(self, port="COM10", encoding="RFCA", loopback=False, baudrate=1000000):
		self.port = port
		self.loopback = loopback
		self.baudrate = baudrate
		self.instance = None
		self.tmpContent = None
		self.encoding = encoding
		self._fire_up()

	def _fire_up(self):
		if self.loopback is False:
			self.interface = serial.Serial(self.port, self.baudrate, timeout=0.005, bytesize=serial.EIGHTBITS)
		print("[+]Serial Port Initialized @", self.port, "with baudrate", self.baudrate)

	def output(self, content):
		if content is not None:
			if not self.loopback:
				self.interface.write(content)
	
	def send_image(self,content):
		assert self.encoding in ["RFCA", "RAW"]
		if self.encoding == "RFCA":
			self.output(SimpleSerial.build_package(id=1, content=content))
		elif self.encoding == "RAW":
			self.output(SimpleSerial.build_package(id=0, content=content))

	@staticmethod
	def build_package(id, content):
		if content is None:
			return None
		init = [200, len(content)//255, len(content) % 255, len(content) % 71, id, SimpleSerial._datachecksum(content)]
		if content is None:
			return init
		else:
			return init + list(content)

	@staticmethod
	def _datachecksum(data):
		sum = 0
		for i in range(0,len(data)):
			if (i % 5) == 0:
				sum = sum + data[i] % 7
			elif (i%7) == 0:
				sum = sum + data[i] % 5
			elif (i%11) == 0:
				sum = sum + data[i] % 11
			elif (i%13) == 0:
				sum = sum + data[i] % 13
			elif (i%17) == 0:
				sum = sum + data[i] % 17
			elif (i%19) == 0:
				sum = sum + data[i] % 19
			elif (i%3) == 0:
				sum = sum + data[i] % 3
			else:
				sum = sum + data[i]
			return sum % 255
