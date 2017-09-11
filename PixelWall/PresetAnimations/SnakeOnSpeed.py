import sys
import random
import math
import datetime
sys.path.append('.\PixelWall')
from PixelWall import Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class SnakeOnSpeed(PresetAnimations.AnimationInstance):
	def extendedInit(self):
		self.LineStorage = []

	def Render(self):
		lineMax = 70
		length = 7
		randNR = 100
		colors = [(74,62,0),(75,13,38),(0,68,91),(8,70,54),(105,0,0),(78,112,57),(8,70,54)]
		#colors = [(42,100,97),(10,215,245),(40,15,217),(217,191,15),(245,20,20)]

		if "Colors" in self.args:
			colors = self.args["Colors"]

		if "length" in self.args:
			length = self.args["length"]

		if "DirectionChange" in self.args:
			randNR = self.args["DirectionChange"]

		if "LineLength" in self.args:
			lineMax = self.args["LineLength"]


		while len(self.LineStorage) < lineMax:
			startposX = random.randint(0,self.dFrame.img.size[0]-1)
			startposY = random.randint(0,self.dFrame.img.size[1]-1)
			colorID = random.randint(0,len(colors)-1)
			#colorID|pivot|Direction|counterSLC|cord
			coordindates = []
			for i in range(0,length):
				coordindates.append([startposX,startposY])
			direction = [random.randint(0,3)]
			self.LineStorage.append([colorID,0,direction,0,coordindates])
		#iterate
		for i in range(0,len(self.LineStorage)):
			self.LineStorage[i][3] +=1 #counter

			#Change Direction?
			rndCH = random.randint(0,randNR);
			if rndCH <= self.LineStorage[i][3]:
				self.LineStorage[i][3] = 0
				self.LineStorage[i][2] = random.randint(0,3)

			#Generate
			direction = self.LineStorage[i][2]
			dirVector = [0,0]
			if direction == 0:
				dirVector = [0,1]
			elif direction == 2:
				dirVector = [0,-1]
			elif direction == 3:
				dirVector = [-1,0]
			elif direction == 1:
				dirVector = [1,0]

			index = self.LineStorage[i][1]
			indexold = index
			index +=1;index = index % length
			self.LineStorage[i][4][index] = [(self.LineStorage[i][4][indexold][0]+dirVector[0])%self.dFrame.img.size[0],(self.LineStorage[i][4][indexold][1]+dirVector[1])%self.dFrame.img.size[1]]
			self.LineStorage[i][1] = index
		#Render
		for i in range(0,len(self.LineStorage)):
			locColor = colors[self.LineStorage[i][0]]
			for p in range(0,len(self.LineStorage[i][4])):
				self.dFrame.pixel[self.LineStorage[i][4][p][0],self.LineStorage[i][4][p][1]] =  locColor
