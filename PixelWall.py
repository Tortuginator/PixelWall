import time
import math
import random
from PIL import Image

class AnimationStates():
	inProgress = 0
	hasEnded = 1
	nextIteration = 2

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
		self.Animations = {} #All Animations are saved here
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
		newFrame = self.input(Frame(self.height,self.width),self.fps,self.frameCount,self.frameInSecond)#call new frame
		if self.brightness != 1:
			newFrame = self.__adjustBrightness(newFrame)

		newFrame = self.drawAnimation(newFrame);
		newFrame.output()
		self.frameTimes.append(time.time() - start_time)
		self.frameCount +=1
		self.frameInSecond +=1
		if self.frameInSecond > self.fps:
			self.frameInSecond = 1

		print "[RENDERENGINE] fct %s" % (time.time() - start_time)


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
			self.Halfframes = value;

	def setBrightness(self,brightness):
		if not 0 <= brightness <= 1:
			return 0
		self.brightness = brightness
		return 1

	def getBrightness(self):
		return self.brightness;

	def drawAnimation(self,dFrame):
		for i in self.Animations:
			i = self.Animations[i]
			if i["Type"] == "Custom":
				CurrentFrame = 0
				if self.frameCount >= i["StartFrame"]:
					CurrentFrame = self.frameCount-i["StartFrame"]
				else:
					continue #SKIP
				if i["Length"] == 0:
					if "Iteration" in i:
						Iteration = i["Iteration"]
						CurrentFrame = CurrentFrame -i["Coffset"]
					else:
						Iteration = -1
					CurrentFrame = float(CurrentFrame)*i["Factor"]
					print float(CurrentFrame)*i["Factor"]
				else:
					CurrentFrame = float(CurrentFrame)*i["Factor"]
					Iteration = CurrentFrame//i["Length"]
					CurrentFrame = float(CurrentFrame%i["Length"])+1
				print CurrentFrame
				if Iteration > i["Count"] and i["Count"] != 0:
					self.Animations.pop(i["Name"]);
					print "[RENDERENGINE] Animation closed " + i["Name"]
					continue
				dFrame,dStatus,self.Animations[i["Name"]]["Storage"]= i["Function"](dFrame,CurrentFrame,Iteration,i["Storage"],i["Parameters"])
				if dStatus == AnimationStates.hasEnded:
					self.Animations.pop(i["Name"])
					print "[RENDERENGINE] Animation closed " + i["Name"]
					continue
				elif dStatus == AnimationStates.nextIteration:
					print "Iteration registered"
					if i["Length"] == 0:
						if not "Iteration" in i:
							self.Animations[i["Name"]]["Iteration"] = 0
							self.Animations[i["Name"]]["Coffset"] = 0
						self.Animations[i["Name"]]["Iteration"] += 1
						self.Animations[i["Name"]]["Coffset"] += CurrentFrame*(1/i["Factor"])

			elif i["Type"] == "Image":
				if i["Loop"] is False and i["Frame"]["totalframes"] < pastFrames:
					continue
				for y in range(0,i["Frame"]["Height"]):
					for x in range(0,self.BitMapDB[i["Image"]["File"]]["width"]):
						localOffset = ((pastFrames%i["Frame"]["totalframes"])*i["Frame"]["Height"]*self.BitMapDB[i["Image"]["File"]]["width"])+(y*self.BitMapDB[i["Image"]["File"]]["width"])+x;
						content = self.BitMapDB[i["Image"]["File"]]["content"]
						if i["Transparency"] is True and content[0][localOffset] == 0 and content[1][localOffset] == 0 and content[2][localOffset] == 0:
							pass
						else:
							dFrame.setPixel(i["Position"]["X"]+x,i["Position"]["Y"]+y,(content[0][localOffset],content[1][localOffset],content[2][localOffset]))

		return dFrame

	#def addAnnimationTest(self,factor = 1,Loop = True,StartFrame = 0):
		#newA = {"Type":"TestA","Factor":factor,"Start":StartFrame,"Loop":Loop}


	#def addAnnimationCircle(self,X,Y,radius,color,Loop = True,StartFrame = 0,colorGRAD = (0,0,0),factor = 1,length = 1):
		#newA = {"Type":"Circle","Factor":factor,"Position":{"X":X,"Y":Y},"Radius":radius,"Color":color,"ColorGRAD":colorGRAD, "Start":StartFrame,"Loop":Loop,"Length":length}

	def __importAnimationFile(self,file):
		img_arrR = []
		img_arrG = []
		img_arrB = []
		rgb_im = Image.open(file)
		for y in range(0,rgb_im.size[1]):
			for x in range(0,rgb_im.size[0]):
				b = rgb_im.getpixel((x,y));
				img_arrR.append(b[0])
				img_arrG.append(b[1])
				img_arrB.append(b[2])
		self.BitMapDB[file] = {"height":rgb_im.size[1],"width":rgb_im.size[0],"content":[img_arrR,img_arrG,img_arrB]};

	def addAnimationImage(self,file,factor,X,Y,ImageFrames,height,StartFrame = 0,Loop = False,Static = True,Transparency = True):
		if not 0 < factor <= 1:return 0;
		if StartFrame == 0: StartFrame = self.frameCount;
		if not Static in [True,False]:return 0
		if not Loop in [True,False]:return 0
		if not Transparency in [True,False]: return 0;

		NewA = {"Type":"File","Factor":factor,"Position":{"X":X,"Y":Y},"Image":{"File":file},"Transparency":Transparency,"Frame":{"Height":height,"totalframes":ImageFrames},"Start":StartFrame,"Loop":Loop,"Static":Static};
		if not NewA["Image"]["File"] in self.BitMapDB or NewA["Static"] == False:
			self.__importAnimationFile(file)
		if not (self.BitMapDB[file]["height"]%NewA["Frame"]["Height"]) == 0:
			return 0
		self.Animations.append(NewA);
		return 1

	def addAnimationCustom(self,Name = "Unknown",Count = 0,Parameters = {},StartFrame = 1,Length = 0,Function = None,Factor = 1,Storage = None):
		if Count == 0:
			Loop = True;
		else:
			Loop = False;
		if not Count >= 0:return 0
		if not int(Count) == Count:return 0
		if not StartFrame >= 0:return 0
		if not int(StartFrame) == StartFrame:return 0
		if not Length >= 0:return 0
		if not int(Length) == Length:return 0
		if Function == None:return 0
		if not Factor > 0:return 0
		if Name == "Unknown":return 0

		newA = {"Type":"Custom","Name":Name,"Loop":Loop,"Count":Count,"Parameters":Parameters,"StartFrame": StartFrame,"Length":Length,"Function":Function,"Factor":Factor,"Storage":Storage}
		if not Name in self.Animations:
			self.Animations[Name] = newA;
		else:
			print "[ERROR] Name allready exists in self.Animations"
			return 0
		return 1



	#def addAnimationPattern(self,Loop=True,StartFrame = 1,factor = 1,colorRangeA=(0,0,0),colorRangeB=(255,255,255),RGBCorrelated = False):
		#newA = {"Type":"Pattern","Factor":factor,"Start":StartFrame,"Loop":Loop,"ColorA":colorRangeA,"ColorB":colorRangeB,"RGBcorr":RGBCorrelated}

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

	def drawCircle(self, x0, y0, radius, colour):
		if Frame.isColor(colour) is False:return 0;
		colour = Frame.isColor(colour);
		#if Frame.isColor(fillColor) is False:return 0;
		if radius <= 0:	return 0;

		#Adjust the location

		f = 1 - radius
		ddf_x = 1
		ddf_y = -2 * radius
		x = 0
		y = radius
		self.setPixel(x0, y0 + radius, colour,merge = True)
		self.setPixel(x0, y0 - radius, colour,merge = True)
		self.setPixel(x0 + radius, y0, colour,merge = True)
		self.setPixel(x0 - radius, y0, colour,merge = True)
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			self.setPixel(x0 + x, y0 + y, colour,merge = True)
			self.setPixel(x0 - x, y0 + y, colour,merge = True)
			self.setPixel(x0 + x, y0 - y, colour,merge = True)
			self.setPixel(x0 - x, y0 - y, colour,merge = True)
			self.setPixel(x0 + y, y0 + x, colour,merge = True)
			self.setPixel(x0 - y, y0 + x, colour,merge = True)
			self.setPixel(x0 + y, y0 - x, colour,merge = True)
			self.setPixel(x0 - y, y0 - x, colour,merge = True)

	def drawRectangle(self,Xa,Xb,Ya,Yb,color,opacity = 1):
		#if not self.isPixel(Xa,Ya):return 0;
		#if not self.isPixel(Xb,Yb):return 0;

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
			if not self.isPixel(Xa,Ya+p):continue;
			Ioffset = self.getOffset(Xa,Ya+p)
			for i in range(0,Xoffset):
				self.R[Ioffset+i] = int(color[0]*opacity)
				self.G[Ioffset+i] = int(color[1]*opacity)
				self.B[Ioffset+i] = int(color[2]*opacity)

		return 1

	def __setPixel(self,X,Y,color):#WARNING, no checks will be performed
		return self.setPixel(X,Y,color,True)

	def setPixel(self,X,Y,color, performance = False,merge = False):
		if not performance:
			if not self.isPixel(X,Y):
				return 0
			if not Frame.isColor(color):
				return 0

		if not X >= 0 or not Y >= 0:
			return 0

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

	def output(self):
		byR = bytearray(self.R)
		byG = bytearray(self.G)
		byB = bytearray(self.B)

		with open("frame.bin", "wb") as f:
			f.write(byR + byG + byB)

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

	def writeText(self,X,Y,text,color):
		if not Frame.isColor(color):return 0;
		if not self.isPixel(X,Y):return 0;
		spaces = {"!":1,"|":1,":":1,".":1}
		chars = {	"0":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,0)],
					"1":[(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,4),(0,3)],
					"2":[(0,0),(1,0),(2,0),(0,1),(1,2),(2,3),(2,4),(1,5),(0,4)],
					"3":[(0,0),(1,0),(2,1),(1,2),(2,3),(1,4),(0,4)],
					"4":[(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4),(0,5),(2,3),(2,4)],
					"5":[(0,1),(1,0),(2,1),(1,3),(0,3),(0,4),(0,5),(1,5),(2,5),(2,2)],
					"6":[(0,1),(0,3),(1,0),(2,1),(1,2),(0,4),(1,5),(2,5),(0,2)],
					"7":[(0,0),(0,1),(1,2),(1,3),(2,4),(0,5),(1,5),(2,5)],
					"8":[(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(0,3),(2,3),(0,4),(1,4),(2,4)],
					"9":[(2,0),(2,1),(2,2),(2,3),(2,4),(1,4),(0,4),(0,3),(0,2),(1,2)],

					"!":[(0,0),(0,2),(0,3),(0,4),(0,5)],
					"a":[(0,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(1,5),(0,5),(0,4),(0,3),(0,2),(0,1),(1,2)],
					"b":[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(2,0),(1,2),(2,2),(2,1)],
					"c":[(0,0),(0,1),(0,2),(1,0),(2,0),(1,2),(2,2)],
					"d":[(0,0),(1,0),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(0,1),(0,2),(1,2)],

					"-":[(0,2),(1,2),(2,2)],
					"_":[(0,0),(1,0),(2,0)],
					":":[(0,1),(0,3)],
					".":[(0,0)],
					"|":[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)],
					"+":[(1,1),(1,2),(1,3),(0,2),(2,2)]}
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
