import time
import math
import random
from PIL import Image
class FrameObjects():
	def __init__(self):
		pass
	def clear(self):
		pass
	def Add(self,type,parameters={}):
		pass

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
		self.Storage = {}

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

	def __shouldDrawSubFrame(self,startframe,factor):
		if startframe >= self.frameCount:return False;
		diffFrameCount = self.frameCount-startframe
		FramesSkipped = diffFrameCount%(1/factor)
		if FramesSkipped == 0:
			return True
		return False

	def drawAnimation(self,dFrame):
		r = 0
		for i in self.Animations:
			if not self.__shouldDrawSubFrame(i["Start"],i["Factor"]):
				continue
			pastFrames = int((self.frameCount - i["Start"])//(1/i["Factor"]));

			if i["Type"] == "File":
				if i["Loop"] is False and i["Frame"]["totalframes"] < pastFrames:
					self.Animations.pop(r);
					return dFrame
				#print pastFrames%i["Frame"]["totalframes"]
				for y in range(0,i["Frame"]["Height"]):
					for x in range(0,self.BitMapDB[i["Image"]["File"]]["width"]):
						localOffset = ((pastFrames%i["Frame"]["totalframes"])*i["Frame"]["Height"]*self.BitMapDB[i["Image"]["File"]]["width"])+(y*self.BitMapDB[i["Image"]["File"]]["width"])+x;
						content = self.BitMapDB[i["Image"]["File"]]["content"]
						if i["Transparency"] is True and content[0][localOffset] == 0 and content[1][localOffset] == 0 and content[2][localOffset] == 0:
							pass
						else:
							dFrame.setPixel(i["Position"]["X"]+x,i["Position"]["Y"]+y,(content[0][localOffset],content[1][localOffset],content[2][localOffset]))

			elif i["Type"] == "TestA":
				totalduration = 80
				CurrentIndex = (pastFrames%totalduration)+1

				if CurrentIndex <= 5:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,p*2,p*2,(255,0,0))
				elif CurrentIndex <= 10:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,p*2,p*2,(0,255,0))
				elif CurrentIndex <= 15:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,p*2,p*2,(0,0,255))
				elif CurrentIndex <= 20:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,(p*2)+1,(p*2)+1,(255,0,0))
				elif CurrentIndex <= 25:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,(p*2)+1,(p*2)+1,(0,255,0))
				elif CurrentIndex <= 30:
					for p in range(0,(self.height//2)+1):
						dFrame.drawRectangle(0,self.width-1,(p*2)+1,(p*2)+1,(0,0,255))
				elif CurrentIndex <= 60:
					CurrentIndex =CurrentIndex-30
					dFrame.drawRectangle(0,CurrentIndex,0,self.height-1,(255,255,255))
				elif CurrentIndex <=80:
					CurrentIndex =CurrentIndex-60
					dFrame.drawRectangle(0,self.width,0,self.height,((255/20)*CurrentIndex,(255/20)*CurrentIndex,(255/20)*CurrentIndex))

			elif i["Type"] == "Circle":
				Cindex = pastFrames%(i["Radius"])
				Cindex = Cindex+1
				baseColor = [i["Color"][0] - i["ColorGRAD"][0],i["Color"][1] - i["ColorGRAD"][1],i["Color"][2] - i["ColorGRAD"][2]]

				for p in range(0,Cindex+1):
					CurrentRadius = p;MaxRadius = Cindex;FadeIn = i["Length"];

					if MaxRadius-FadeIn <= CurrentRadius:
						divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
					else:
						divRelation = 0

					if p > Cindex:
						divRad = Cindex
					else:
						divRad = p
					divColor = (divRelation*baseColor[0] + i["ColorGRAD"][0],divRelation*baseColor[1] + i["ColorGRAD"][1],divRelation*baseColor[2] + i["ColorGRAD"][2])
					dFrame.drawCircle(i["Position"]["X"],i["Position"]["Y"],divRad,divColor)

				#def drawCircle(self, x0, y0, radius, colour):
			elif i["Type"] == "Pattern":
				Cindex = pastFrames-i["Start"]
				if not "RND_PATT" in self.Storage:
					self.Storage["RND_PATT"] = [];
					tmLength = self.width*self.height
					for p in range(0,tmLength+1):
						self.Storage["RND_PATT"].append(random.randint(0,255))

				tmLength = self.width*self.height
				for p in range(0,tmLength+1):
					x0 = p%self.width
					y0 = p//self.width
					c0r = (i["ColorA"][0] - i["ColorB"][0])*(-1)
					c0g = (i["ColorA"][1] - i["ColorB"][1])*(-1)
					c0b = (i["ColorA"][2] - i["ColorB"][2])*(-1)
					p0 = math.cos(self.Storage["RND_PATT"][p]*float(Cindex*0.0001))
					if p0 < 0:
						p0 = p0*(-1)
					c0 = (int(i["ColorA"][0] + c0r*p0),int(i["ColorA"][1] + c0g*p0),int(i["ColorA"][2] + c0b*p0))
					dFrame.setPixel(x0,y0,c0)
		r += 1;
		return dFrame

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

	def addAnimationFile(self,file,factor,X,Y,ImageFrames,height,StartFrame = 0,Loop = False,Static = True,Transparency = True):
		if not 0 < factor <= 1:return 0;
		if StartFrame == 0: StartFrame = self.frameCount;
		if not Static in [True,False]:return 0
		if not Loop in [True,False]:return 0
		if not Transparency in [True,False]: return 0;
		if not StartFrame%1 == 0:return 0;#Even number

		NewA = {"Type":"File","Factor":factor,"Position":{"X":X,"Y":Y},"Image":{"File":file},"Transparency":Transparency,"Frame":{"Height":height,"totalframes":ImageFrames},"Start":StartFrame,"Loop":Loop,"Static":Static};
		if not NewA["Image"]["File"] in self.BitMapDB or NewA["Static"] == False:
			self.__importAnimationFile(file)
		if not (self.BitMapDB[file]["height"]%NewA["Frame"]["Height"]) == 0:
			return 0
		self.Animations.append(NewA);
		return 1

	def addAnnimationTest(self,factor = 1,Loop = True,StartFrame = 0):
		if not Loop in [True,False]:return 0
		if not factor > 0:return 0
		if not StartFrame >= 0:return 0
		if not StartFrame%1 == 0:return 0;#Even number

		newA = {"Type":"TestA","Factor":factor,"Start":StartFrame,"Loop":Loop}

		self.Animations.append(newA);
		return 1

	def addAnnimationCircle(self,X,Y,radius,color,Loop = True,StartFrame = 0,colorGRAD = (0,0,0),factor = 1,length = 1):
		if not radius >= 0:return 0;
		if not factor > 0:return 0;
		if not radius%1 == 0:return 0;#Even number
		if not Loop in [True,False]: return 0;
		if not Frame.isColor(color):return 0;
		if not StartFrame >= 0:return 0;
		if not StartFrame%1 == 0:return 0;#Even number
		if not Frame.isColor(colorGRAD):return 0;

		newA = {"Type":"Circle","Factor":factor,"Position":{"X":X,"Y":Y},"Radius":radius,"Color":color,"ColorGRAD":colorGRAD, "Start":StartFrame,"Loop":Loop,"Length":length}

		self.Animations.append(newA);
		return 1
	def addAnnimationCustom(self,Loop=False,StartFrame = 1,duration = 1,function = None,factor = 1):
		print "NOT IMPLEMENTED"
		pass

	def addAnimationPattern(self,Loop=True,StartFrame = 1,factor = 1,colorRangeA=(0,0,0),colorRangeB=(255,255,255),RGBCorrelated = False):
		if not Loop in [True,False]:return 0
		if not StartFrame >= 0:return 0
		if not StartFrame%1 == 0:return 0;#Even number
		if not factor > 0:return 0
		if not Frame.isColor(colorRangeA):return 0
		if not Frame.isColor(colorRangeB):return 0
		if not RGBCorrelated in [True,False]:return 0

		newA = {"Type":"Pattern","Factor":factor,"Start":StartFrame,"Loop":Loop,"ColorA":colorRangeA,"ColorB":colorRangeB,"RGBcorr":RGBCorrelated}
		self.Animations.append(newA);
		return 1

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
		self.setPixel(x0, y0 + radius, colour)
		self.setPixel(x0, y0 - radius, colour)
		self.setPixel(x0 + radius, y0, colour)
		self.setPixel(x0 - radius, y0, colour)
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			self.setPixel(x0 + x, y0 + y, colour)
			self.setPixel(x0 - x, y0 + y, colour)
			self.setPixel(x0 + x, y0 - y, colour)
			self.setPixel(x0 - x, y0 - y, colour)
			self.setPixel(x0 + y, y0 + x, colour)
			self.setPixel(x0 - y, y0 + x, colour)
			self.setPixel(x0 + y, y0 - x, colour)
			self.setPixel(x0 - y, y0 - x, colour)

	def drawRectangle(self,Xa,Xb,Ya,Yb,color):
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

		if not X >= 0 or not Y >= 0:
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
