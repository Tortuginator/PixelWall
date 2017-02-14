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
