import time
import math
import PIL
class RenderEngine():
	def __init__(self,height,width,Hz):
		self.brightness = 1;
		self.height = height;
		self.fps = 20;
		self.width = width;
		self.frequency = Hz;
		self.input = "";
		self.frameCount = 0
		self.frameInSecond = 0
		self.RenderInstances = []
		self.framePreset = Frame(self.height,self.width)
		self.frameTimes = [] #for Statistics
		self.Animations = [] #All Animations are saved here
		self.BitMapDB = {} #A temporary library of BMP maps

	def setFramePreset(self,NewPreset):
		if NewPreset.instanceOf(Frame):
			self.framePreset = NewPreset
			return 1
		return 0

	def getFramePreset(self):
		return self.framePreset

	def pushFrame(self):
		start_time = time.time()
		newFrame = self.input(self.framePreset,self.fps,self.frameCount,self.frameInSecond)#call new frame

		if self.brightness != 1:
			newFrame = self.__adjustBrightness(newFrame)

		newFrame.output()
		self.frameTimes.append(time.time() - start_time)
		self.frameCount +=1
		self.frameInSecond +=1
		if self.frameInSecond > self.fps:
			self.frameInSecond = 1

		print "--- %s seconds ---" % (time.time() - start_time)


	def __adjustBrightness(self,newFrame):
		for i in range(0,newFrame.PixelCount-1):
			newFrame.R[i] = int(newFrame.R[i]*self.brightness)
			newFrame.G[i] = int(newFrame.G[i]*self.brightness)
			newFrame.B[i] = int(newFrame.B[i]*self.brightness)
		return newFrame

	def setInputRenderer(self,InputName):
		self.input = InputName
		return 1

	def getInputRenderer():
		return self.Input;

	def setFPS(self,FPS):
		self.fps = FPS;

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
		self.R = [0 for i in range(0,self.PixelCount)]
		self.G = [0 for i in range(0,self.PixelCount)]
		self.B = [0 for i in range(0,self.PixelCount)]

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
		else:
			Yoffset -=1;

		Xoffset = Xb-Xa
		if Xoffset >=0:
			Xoffset += 1;
		else:
			Xoffset -= 1;

		for p in range(0,Yoffset):
			Ioffset = self.getOffset(Xa,Ya+p)
			for i in range(0,Xoffset):
				self.R[Ioffset+i] = color[0]
				self.G[Ioffset+i] = color[1]
				self.B[Ioffset+i] = color[2]

		return 1

	def __setPixel(self,X,Y,color):#WARNING, no checks will be performed
		return self.setPixel(X,Y,color,True)

	def setPixel(self,X,Y,color, performance = False):
		if not performance:
			if not self.isPixel(X,Y):
				return 0
			if not Frame.isColor(color):
				return 0


		Ioffset = self.getOffset(X,Y);
		self.R[Ioffset] = color[0]
		self.G[Ioffset] = color[1]
		self.B[Ioffset] = color[2]

		return 1

	def output(self):
		byR = bytearray(self.R)
		byG = bytearray(self.G)
		byB = bytearray(self.B)

		with open("frame.bin", "wb") as f:
			f.write(byR + byG + byB)

	@staticmethod
	def isColor(color):
		if not 0 <= color[0] <= 255:
			return False
		if not 0 <= color[1] <= 255:
			return False
		if not 0 <= color[2] <= 255:
			return False
		return True

	def writeText(self,X,Y,text,color):
		if not Frame.isColor(color):return 0;
		if not self.isPixel(X,Y):return 0;
		spaces = {"!":1}
		chars = {	"0":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,0)],
					"1":[(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,4),(0,3)],
					"2":[(0,0),(1,0),(2,0),(0,1),(1,2),(2,3),(2,4),(1,5),(0,4)],
					"3":[(0,0),(1,0),(2,1),(1,2),(2,4),(2,3),(1,5),(0,5)],
					"4":[(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4),(0,5),(2,3),(2,4)],
					"5":[(0,1),(1,0),(2,1),(1,3),(0,3),(0,4),(0,5),(1,5),(2,5),(2,2)],
					"6":[(0,1),(0,3),(1,0),(2,1),(1,2),(0,4),(1,5),(2,5),(0,2)],
					"7":[(0,0),(0,1),(1,2),(1,3),(2,4),(0,5),(1,5),(2,5)],

					"!":[(0,0),(0,2),(0,3),(0,4),(0,5)],
					"a":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,2)],
					"b":[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(2,0),(1,2),(2,2),(2,1)],
					"c":[(0,0),(0,1),(0,2),(1,0),(2,0),(1,2),(2,2)],
					"d":[(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(0,1),(0,2),(1,2)]}
		given = list(text)
		pos = 0;
		for i in text:
			if i in chars:
				for p in chars[i]:
					self.setPixel(pos+p[0],Y-p[1],color)
			if i in spaces:
				pos +=1+spaces[i]
			else:
				pos +=4;
		return 1
	def __shouldDrawSubFrame(self,startframe,factor):
		diffFrameCount = self.totalframes-startframe
		FramesSkipped = diffFrameCount%(1/factor)
		if FramesSkipped == 0:
			return True
		return False

	def drawAnimation(self,dFrame):
		r = 0
		for i in self.Animations:
			if not self.__shouldDrawSubFrame(i["Start"],i["Factor"]):
				continue
			pastFrames = (self.totalframes - i["Start"])//(1/i["Factor"]);
			if i["Loop"] is False and i["Frames"]["totalframes"] < pastFrames:
				self.Animations.pop(r);
				return 0
			if i["Type"] == "File":
				for y in range(0,i["Frames"]["Height"]):
					for x in range(0,self.BitMapDB[i["File"]["width"]]):
						localFrameOffset = (self.totalframes - i["Start"])//(1/i["Factor"])
						localFrameOffset = localFrameOffset%i["Frames"]["totalframes"]
						localOffset = (localOffset*i["Frames"]["Height"]*i["Frames"]["Width"])+(y*self.BitMapDB[i["File"]["width"]])+x;
						content = self.BitMapDB[i["File"]]["content"]
						if i["Black"] is False:
							if content[0][localFrameOffset] == 0 and content[1][localFrameOffset] == 0 and content[2][localFrameOffset] == 0:
								continue
						dFrame.setPixel(i["Positon"]["X"]+x,i["Positon"]["Y"]-y,(content[0][localFrameOffset],content[1][localFrameOffset],content[2][localFrameOffset]))

			r += 1;
	def __importAnimationFile(self,file):
		img_arrR = []
		img_arrG = []
		img_arrB = []
		img = PIL.Image.open(file)
		rgb_im = img.convert('RGB')

		for y in range(0,rgb_im.size[0]):
			for x in range(0,rgb_im.size[1]):
				b = im_rgb[x,y];
				img_arrR.append(b[0])
				img_arrG.append(b[1])
				img_arrB.append(b[2])
		self.BitMapDB[file] = {"height":rgb_im.size[1],"width":rgb_im.size[0],"content":[g_arrR,g_arrG,g_arrB]};

	def addAnimationFile(self,file,factor,X,Y,totalframes,height):
		if not 0 < factor <= 1:return 0;
		NewA = {"Type":"File","Factor":factor,"Position":{"X":X,"Y":Y},"Image":{"File":file,"showBlack":False},"Frames":{"Height":height,"CurrentFrame":0,"totalframes":totalframes},"Start":self.totalframes,"Loop":False,"Static":True};
		if not NewA["Image"]["File"] in self.BitMapDB or NewA["Static"] == False:
			self.__importAnimationFile(file)
		if not (self.BitMapDB[file]["height"]%NewA["Frame"]["Height"]) == 0:
			return 0
		self.Animations[len(self.Animations)] = NewA
		return 1
