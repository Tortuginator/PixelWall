class RenderEngine():
	def __init__(self,height,width,Hz):
		self.brightness = 1;

	def setFPS(self,FPS):


	def getHalfframes(self):
		return self.Halfframes;

	def setHalfframes(self,value):
		if value == True or value == False:
			self.Halfframes  = value;

	def setBrightness(self,brightness):
		if not 0 <= brightness <= 1: 
			return 0
		self.brightness = brightness
		return 1

	def getBrightness(self):
		return self.brightness;

class Frame():
	def __init__(self,height,width):
		self.height = height;
		self.width = width;
		self.PixelCount = height*width;
		self.R = [0 for i in range(0,Self.PixelCount-1)]
		self.G = [0 for i in range(0,self.PixelCount-1)]
		self.B = [0 for i in range(0,self.PixelCount-1)]

	def __getPixel(self,X,Y):#WARNING no checks performed
		return self.getPixel(X,Y,True);

	def getPixel(self,X,Y,performance = False):
		if not performance :
			if not self.isPixel(X,Y):return [];
		Ioffset = self.getoffset(X,Y);
		return [self.R[Ioffset],self.G[Ioffset],self.B[Ioffset]];

	def isPixel(self,X,Y):
		if not X <= self.width-1:
			return False
		if not Y <= self.height-1:
			return False
		return True

	def setRectangle(self,Xa,Xb,Ya,Yb,color):
		if not self.isPixel(Xa,Ya):return 0;
		if not self.isPixel(Xb,Yb):return 0;

		if not Frame.isColor(color):return 0;

		#XaYa----|
		#|		 |
		#|		 |
		#|----XbYb
		Yoffset = Yb-Ya
		if Yoffset >= 0:
			Yoffset +=1;
		else
			Yoffset -=1;

		Xoffset = Xb-Xa
		if Xoffset >=0:
			Xoffset += 1;
		else
			Xoffset -= 1;

		for p in range(0,Yoffset):
			Ioffset = self.getOffset(Xa,Yb+p)
			for i in range(Xa,Xoffset):
				self.R[Ioffset+i] = color[0]
				self.G[Ioffset+i] = color[1]
				self.B[Ioffset+i] = color[2]

		return 1

	def __setPixel(self,X,Y,color):#WARNING, no checks will be performed
		return self.setPixel(X,Y,color,True)

	def setPixel(self,X,Y,color, performance = False):
		if not performance:
			if not Frame.isColor(color):
				return 0

			if not self.isPixel(X,Y):
				return 0

		Ioffset = self.getoffset(X,Y);
		self.R[Ioffset] = color[0]
		self.G[Ioffset] = color[1]
		self.B[Ioffset] = color[2]

		return 1

	def getOffset(self,X,Y):
		return (Y*self.width)+X-1;

	@staticmethod
	def isColor(color):
		if not 0 <= color[0] <= 255:
			return False
		if not 0 <= color[1] <= 255:
			return False
		if not 0 <= color[2] <= 255:
			return False
		return True
