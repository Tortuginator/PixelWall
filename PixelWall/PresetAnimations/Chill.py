import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class Chill(PresetAnimations.AnimationInstance):
	def extendedInit(self):
		self.ChillStorage = []

	def Render(self):
		"""
		Chill is a Animation, which draws random points of random color on a random location of the Canvas
		This Canvas will the be blurred using the GaussianBlur Algorithm
		Each point has a own "speed", meaning each point at a speed of 1 exists 255 frames long and a point with the speed of 2 exists UP|! 255/2 frames long
		The Speed is randomly assigned. The Amount of Pixels, which exist on a canvas Simultaniously is determined by the value "Points"
		The fade-in/out is determined by the Coswave in the intervall 0 to 2PI
		"""

		#Set Defaults
		ColorLower = (100, 100, 100)
		ColorHigher = (255, 255, 255)
		Drops = 80
		SpeedMin = 0.05
		SpeedMax = 2.0
		#Get args
		if "ColorLower" in self.args:
			ColorLower = self.args["ColorLower"]
		if "ColorHigher" in self.args:
			ColorHigher = self.args["ColorHigher"]

		if "Points" in self.args:
			Drops = self.args["Points"]

		if "SpeedMax" in self.args:
			SpeedMax = self.args["SpeedMax"]
		if "SpeedMin" in self.args:
			SpeedMin = self.args["SpeedMin"]

		#check
		if ColorLower[0] > ColorHigher[0] or ColorLower[1] > ColorHigher[1] or ColorLower[2] > ColorHigher[2]:
			return
			#raise FAILED TO DETERMINE THE MINA AND MAX COLOR
		if SpeedMax < SpeedMin:
			return
			#Raise Error of invalid Speedargs

		#precalculated COS wave
		COSwave = [0,0,0,0,1,1,1,2,2,3,4,5,6,6,8,9,10,11,12,14,15,17,18,20,22,23,25,27,29,31,33,35,38,40,42,45,47,49,52,54,57,60,62,65,68,71,73,76,79,82,85,88,91,94,97,100,103,106,109,113,116,119,122,125,128,131,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177,180,183,186,189,191,194,197,199,202,204,207,209,212,214,216,218,221,223,225,227,229,231,232,234,236,238,239,241,242,243,245,246,247,248,249,250,251,252,252,253,253,254,254,255,255,255,255,255,255,255,255,254,254,253,253,252,252,251,250,249,248,247,246,245,243,242,241,239,238,236,234,232,231,229,227,225,223,221,218,216,214,212,209,207,204,202,199,197,194,191,189,186,183,180,177,174,171,168,165,162,159,156,153,150,147,144,141,138,135,131,128,125,122,119,116,113,109,106,103,100,97,94,91,88,85,82,79,76,73,71,68,65,62,60,57,54,52,49,47,45,42,40,38,35,33,31,29,27,25,23,22,20,18,17,15,14,12,11,10,9,8,6,6,5,4,3,2,2,1,1,1,0,0,0,0];
		Drops = 80;
		while (len(self.ChillStorage) < Drops):
			self.ChillStorage.append([random.randint(0, self.dFrame.img.size[0]), random.randint(0, self.dFrame.img.size[1]), (random.randint(ColorLower[0], ColorHigher[0]), random.randint(ColorLower[1], ColorHigher[1]), random.randint(ColorLower[2], ColorHigher[2])), random.uniform(SpeedMin, SpeedMax), 0])
		col = []
		for i in range(0, len(self.ChillStorage)):
			if self.ChillStorage[i][4] > 255:
				self.ChillStorage[i][4] = 255
			r = int(self.ChillStorage[i][2][0]*(float(COSwave[int(self.ChillStorage[i][4])])/255))
			g = int(self.ChillStorage[i][2][1]*(float(COSwave[int(self.ChillStorage[i][4])])/255))
			b = int(self.ChillStorage[i][2][2]*(float(COSwave[int(self.ChillStorage[i][4])])/255))
			divColor = (r,g,b,255)
			self.dFrame.imgdraw.point([self.ChillStorage[i][0], self.ChillStorage[i][1]], divColor)
			self.ChillStorage[i][4] += self.ChillStorage[i][3]
			if self.ChillStorage[i][4] >= 255:
				col.append(i)

		for r in range(0, len(col)):
			del self.ChillStorage[col[r]];

		self.dFrame.img = self.dFrame.img.filter(ImageFilter.GaussianBlur(radius = 2))#To prevent the "ignoring" of the borders by 2 px, when only using the SMOOTH_MORE filter
		self.dFrame.img = self.dFrame.img.filter(ImageFilter.SMOOTH_MORE)
		self.dFrame.img = self.dFrame.img.filter(ImageFilter.GaussianBlur(radius = 2))
