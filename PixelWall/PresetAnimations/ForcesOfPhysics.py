import sys
import random
import math
import operator
sys.path.append('.\PixelWall')
from PixelWall import Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class ForcesOfPhysics(PresetAnimations.AnimationInstance):
	def extendedInit(self):
		self.model = PH_environment()
		self.steps = 0

	def Render(self):
		if self.steps% 10 ==0:
			self.model.addParticle(PH_Particle(position = (int(random.uniform(0, 27)),int(random.uniform(0, 27))),mass = int(random.uniform(20, 50))*1000,color =(5,5,5),mergable = True,fixed = False))
			
		#if self.steps == 0:
		#	myP1 = PH_Particle(position = (5,10),acceleration = (0,0.1),mass = 200000,color = (255,0,0))
		#	myP2 = PH_Particle(position = (10,10),acceleration = (0,0.1),mass = 200000,color = (0,0,255))
		#	self.model.addParticle(myP1)
		#	self.model.addParticle(myP2)
			#self.model.addParticle(PH_Particle(position = (10,10),mass = 50000,color = (0,255,0),mergable = False,fixed = True))
			#self.model.addParticle(PH_Particle(position = (15,15),mass = 500000,color = (0,255,0),mergable = True,fixed = True))
			#self.model.addParticle(PH_Particle(position = (15,7),mass = 5000,color = (0,255,255),mergable = True,fixed = False))
		#else:
		self.model.simulate()
		points = self.model.dotList()
		self.steps +=1
		for i in points:
			if int(i[0][0]) < 0 or int(i[0][0]) > 27 or int(i[0][1]) <0 or int(i[0][1]) > 27:
				pass
			else:
				self.dFrame.pixel[int(i[0][0]),int(i[0][1])] = i[2]
class PH_ForceField():
	def __init__(self,mass = 1,position = (0,0),particle = None):
		self.particle = particle

	def apply(self,particle):
		if self.particle.ID == particle.ID:return
		distance = PH_ForceField.distance(self.particle.position,particle.position)
		ppdistance = self.particle.position-particle.position
		force = PH_ForceField.forceOnSphere(self.particle.position,self.particle.mass,particle.position,particle.mass,distance)
		scale = force/distance
		if not self.particle.fixed:
			self.particle.forces -=PH_FP([scale*force*ppdistance[0],scale*force*ppdistance[1]])
		if not particle.fixed:
			particle.forces += PH_FP([scale*force*ppdistance[0],scale*force*ppdistance[1]])

	@staticmethod
	def forceOnSphere(p1,m1,p2,m2,distance):
		return float("6.67e-11")*10*((m1*m2)/(distance**2))

	@staticmethod
	def distance(p1,p2):
		return PH_ForceField.hyp(p1-p2)

	@staticmethod
	def hyp(p):
		return math.sqrt((p[0]**2)+(p[1]**2))

class PH_Particle():
	def __init__(self,size = 1,position = (0,0),fixed = False,mass = 1,mergable = True,color = (255,255,255),acceleration = (0,0)):
		self.size = size
		self.position = PH_FP([float(position[0]),float(position[1])])
		self.fixed = fixed
		self.mass = mass
		self.forces = PH_FP([float(0),float(0)])
		self.intforces = PH_FP([float(0),float(0)])
		self.mergable = mergable
		self.color = color
		self.ID = random.uniform(1, 10)
		self.acceleration = PH_FP([float(acceleration[0]),float(acceleration[1])])
	def step(self,multiplicator = 0.1):
		self.acceleration = self.acceleration + (self.forces-self.intforces)
		if not self.fixed:
			self.position = self.position + self.acceleration*multiplicator
		self.intforces = self.forces
		self.forces = PH_FP([float(0),float(0)])

class PH_environment():
	def __init__(self):
		self.particles = []
		self.forceFields = []

	def addField(self,field):
		self.forceFields.append(field)

	def addParticle(self,particle):
		self.particles.append(particle)
		initField = PH_ForceField(particle = particle)
		self.addField(initField)

	def simulate(self):
		pMerge = []
		pForce = []
		for (x,y) in PH_environment.powset(self.forceFields,self.particles):
			if (x.particle.ID,y.ID) in pForce or (y.ID,x.particle.ID) in pForce: 
				continue
			if x.particle.ID == y.ID:continue
			x.apply(y)	
			pForce.append((x.particle.ID,y.ID))	#Save that we allready applied the force
			if x.particle.mergable and y.mergable:
				if PH_ForceField.distance(y.position,x.particle.position) <= 0.9:
					pMerge.append((x.particle,y))
		
		pDel = []
		for (x,y) in pMerge:
			pDel.append(x)
			y.color = ((x.color[0] + y.color[0]),(x.color[1] + y.color[1]),(x.color[2] + y.color[2]))
			y.acceleration = (y.acceleration*y.mass + x.acceleration*x.mass)/(x.mass+y.mass)
			y.forces = ((y.forces*y.mass) + (x.forces*x.mass))/(x.mass+y.mass)
			y.mass += x.mass
			y.size +=x.size
			y.fixed = True if y.fixed or x.fixed else False
		self.forceFields = [field for field in self.forceFields if not field.particle in pDel]
		self.particles = [item for item in self.particles if item not in pDel]
		for i in self.particles:
			i.step()
	@staticmethod
	def powset(a,b):
		r = []
		for i in a:
			for j in b:
				r.append((i,j))
		return r
	def dotList(self):
		rPoints = []
		for i in self.particles:
			rPoints.append((i.position,i.size,i.color))
		return rPoints

class PH_FP(tuple):
	def __add__(self, other):
		if len(self) != len(other):
			raise ValueError("tuple lengths don't match")
		return PH_FP(x + y for (x, y) in zip(self, other))
	def __int__(self):
		return tuple(int(x) for x in self)

	def __mul__(self,other):
		return PH_FP(x*other for x in self)

	def __sub__(self,other):
		return PH_FP(x - y for (x,y) in zip(self,other))

	def __div__(self,other):
		return PH_FP([float(x/float(other)) for x in self])