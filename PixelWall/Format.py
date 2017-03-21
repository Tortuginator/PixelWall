import Core
import Exceptions

class FrameFormat():
	def __init__(self, data = None, compression = None, objects = None):
		if compression == None:
			self.compression = None
		else:
			if Core.CompressionType.isCompression(compression) :
				self.compression = compression
			else:
				raise Exceptions.InvalidCompression;

		self.data = data
		self.objects = objects

	def fromTransport(self, data):
		#Convert:
		data = bytearray(data);
		Ldat = len(data);
		#Structure:
		#[Compression (0,1,2)][EXTRA+6]
		if int(data[0]) in [CompressionType.No, CompressionType.Linear]:
			#[Lengtha1][lengtha2][Lengthb1][lengthb2][lengthc1][lengthc2]
			#totalLength = 255*Lengthxa[0-255] + Lengthxb[0-255]|| MAX: 65280bytes length*3 + 7
			totalLengthR = int(ldat[1]) * 254 + int(ldat[2])
			totalLengthG = int(ldat[3]) * 254 + int(ldat[4])
			totalLengthB = int(ldat[5]) * 254 + int(ldat[6])
			if Ldat != (totalLengthR + totalLengthG + totalLengthB+7):
				UtilPrint.compose("!", self.__class__, __name__, "failed to decode. The lengths do not match. The packet will be ignored.")
				return False
			newdata = [[], [], []]
			newdata[0] = data[8:8+totalLengthR]
			newdata[1] = data[totalLengthR+8+1:totalLengthG+8+totalLengthR]
			newdata[2] = data[totalLengthG+8+totalLengthR+1:totalLengthG+8+totalLengthR+totalLengthB]
			self.data = newdata
			self.compression = int(data[0])
			return True
		elif int(data[0]) == CompressionType.Object:
			raise NotImplementedError;
		return False

	def toTransport(self, forceRaw = False):
		if self.compression == Core.CompressionType.Object:
			try:
				self.__convObjToRaw();
			except Exception,e:
				print e
		if self.compression == Core.CompressionType.No:
			if not forceRaw:
				self.data = FrameFormat.__convertRawToLin(self.data)
				self.compression = Core.CompressionType.Linear
			else:
				lenR = len(self.data[0])
				lenG = len(self.data[1])
				lenB = len(self.data[2])
				if lenG != lenR != lenB:
					Core.UtilPrint.compose("!", self.__class__, __name__, "the lenghts of the color arrays do not match in RAW mode!")
				header = bytearray([0, lenR//255, lenR%255, lenG//255, lenG%255, lenB//255, lenB%255])
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
			print [1, lenR//254, lenR%254, lenG//254, lenG%254, lenB//254, lenB%254]
			header = bytearray([1, lenR//254, lenR%254, lenG//254, lenG%254, lenB//254, lenB%254])
			if type(self.data[0]) == list:
				R = bytearray(self.data[0])

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

	def setSize(self, height, width):
		self.fHeight = height
		self.fWidth = width

	def __convObjToRaw(self):
		self.compression = CompressionType.No
		x = Frame(self.fWidth, self.fHeight)
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
		new = [[], [], []]
		cnt = -1
		for i in data:
			locked = None
			cnt +=1
			for x in range(0, len(i)):
				if i[x] == indicator:
					if x + 2 <= len(i):
						#[Indicator][Value][Count]
						for r in range(0, i[x+2]+1):
							new[cnt].append(i[x+1])#new value
						locked = x+2;
					else:
						UtilPrint.compose("!", "UDN", __name__, "found indicator byte at unintended position please check you indicator bytes")
				elif x <= locked:
					pass
					#to be ignored, because theese are the indicator and value bytes
				else:
					new[cnt].append(i[x])

		len_old = len(data[0]) + len(data[1]) + len(data[2])
		len_new = len(new[0]) + len(new[1]) + len(new[2])
		UtilPrint.compose("+", "UDN", __name__, "compression efficiency: " + repr(100-int((float(len_old)/float(len_new))*100)) + "%")
		return new

	@staticmethod
	def __convertRawToLin(data):
		indicator = 1;replacement = 2;new = [[], [], []];
		for channel in range(0, len(data)):
			temporary = []
			lastPoint = None
			for point in range(0, len(data[channel])):
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
							for i in range(1, (len(temporary)-1)//254):
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
				for i in range(1, (len(temporary)-1)//254):
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

		return new

	def setData(self, data, compression):
		self.data = data
		self.compression = compression
