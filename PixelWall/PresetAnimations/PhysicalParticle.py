import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class ParticleSimulation(PresetAnimations.AnimationInstance):
	def extendedInit(self):
		self.ParticleStorage = []
		self.particlenumber = 0

	def Coloring(self,distances,mode):
		if mode == 0:#Neares point to color
			maxDist = self.maxDist
			mdist = maxDist
			mcolor = (0,0,0)
			for i in distances:
				if mdist >= i[1]:
					mcolor,mdist = i
			return mcolor

		elif mode == 1:#FUckup
			sumDist = 0
			maxDist = self.maxDist
			sumColor = (0,0,0)
			for i in distances:
				strength = maxDist - i[1]
				sumDist += strength
				sumColor = (sumColor[0]+i[0][0]*strength,sumColor[1]+i[0][1]*strength,sumColor[2]+i[0][2]*strength)
			return (int(sumColor[0]/sumDist),int(sumColor[1]/sumDist),int(sumColor[2]/sumDist))

		elif mode == 2:#Quatratic Approximation
			dlen = len(distances)
			distances.sort(key=lambda x: x[1],reverse = True)
			color = (0,0,0)

			if dlen >=4:
				dlow = dlen-4
			else:
				dlow = 0

			for i in range(dlow,dlen):
				color = ((2**i)*distances[i][0][0]+color[0],(2**i)*distances[i][0][1]+color[1],(2**i)*distances[i][0][2]+color[2])
			return (color[0]/(2**dlen),color[1]/(2**dlen),color[2]/(2**dlen))

	def Render(self):

		##
		self.maxDist = math.sqrt((self.dFrame.img.size[0]+1)**2 + (self.dFrame.img.size[1]+1)**2)
		ColorLower = (200, 70, 70)
		ColorHigher = (255, 200, 160)

		while len(self.DotStorage) < 10:
			#ID,Color,Mass[KG],Vector,Position,Calculations
			rndcolor = (random.randint(ColorLower[0], ColorHigher[0]), random.randint(ColorLower[1], ColorHigher[1]), random.randint(ColorLower[2], ColorHigher[2]))
			particle = [self.particlenumber,rndcolor,random.randint(100,1000),(0,0),(0,0),[]]
			self.particlenumber+=1
			#Color;Direction;PosX;PosY;LifetimeLeft;strength;random

			item = [rndcolor,(random.randint(-1, 1),random.randint(-1, 1)),random.randint(0, self.dFrame.img.size[0]-1), random.randint(0, self.dFrame.img.size[1]-1),0,1.0,0]
			self.DotStorage.append(item)
		NewPoints = []
		for i in range(0,len(self.DotStorage)):
			Dot = self.DotStorage[i]
			#undate dot position
			RandomFactor = (random.randint(-10, 10)*0.1*Dot[6],random.randint(-10, 10)*0.1*Dot[6])
			Dot[2] = Dot[2] + (RandomFactor[0]+Dot[1][0]*0.1)*(0.5)
			Dot[3] = Dot[3] + (RandomFactor[1]+Dot[1][1]*0.1)*(0.5)
			#Check if Dot is out of bounds
			if Dot[2] <= 0:
				Dot[2] = 0
				Dot[1] = (Dot[1][0]*-1,Dot[1][1])
			elif Dot[2] >= self.dFrame.img.size[0]-1:
				Dot[2] = self.dFrame.img.size[0]-1
				Dot[1] = (Dot[1][0]*-1,Dot[1][1])

			if Dot[3] <= 0:
				Dot[3] = 0
				Dot[1] = (Dot[1][0],Dot[1][1]*-1)
			elif Dot[3] >= self.dFrame.img.size[1]-1:
				Dot[3] = self.dFrame.img.size[1]-1
				Dot[1] = (Dot[1][0],Dot[1][1]*-1)

		#iteratePixels
		for X in range(0,self.dFrame.img.size[0]):
			for Y in range(0,self.dFrame.img.size[1]):
				Distances = []
				for Dot in self.DotStorage:
					#Color,Distance
					Distances.append([Dot[0],int(math.sqrt(int((X-Dot[2])**2 + (Y-Dot[3])**2)))])
				#Color the pixel
				self.dFrame.pixel[X,Y] = self.Coloring(Distances,0)
		self.dFrame.img = self.dFrame.img.filter(ImageFilter.SMOOTH_MORE)
