import socket, sys, time, datetime
from threading import Thread
import sys
import RFCA
sys.path.append('.\PixelWall')


current_milli_time = lambda: int(round(time.time() * 1000))

class Manager():
	def __init__(self, RenderInput, SendOutput, fixargs = None):
		self.RenderIn = RenderInput
		self.SendOut = SendOutput
		self.fixargs = fixargs
		#prop
		self.Renderfps = 1
		self.OutputThread = None
		self.NextEmit = None
		self.RenderRoulette = RoundRender(RenderInput,fixargs)

	def Launch(self):
		self.NextEmit = current_milli_time()
		if self.OutputThread is None:
			self.OutputThread = Thread(target = Manager._Emitter, args = (self, ))
			self.OutputThread.start()
	
	def Restart(self):
		if self.OutputThread is not None:
			self.OutputThread.stop()
			self.OutputThread.start()

	def _Emitter(self):
		while True:
			if self.NextEmit > current_milli_time():
				msDelta = self.NextEmit-current_milli_time()
				time.sleep(float(msDelta)/1000);
				#print "WAITING"
			#EmitterRoutine
			#print "wait " + str(int(1000/float(self.Renderfps)))
			self.NextEmit = current_milli_time() + int(1000/float(self.Renderfps))
			data = self.RenderRoulette.get(self.fixargs)
			#print "[MAIN]" + str(current_milli_time())
			self.SendOut(data)


class RoundRender():
	def __init__(self,RenderInput,fixargs):
		self.max = 3
		self.cur = 0
		self.storage = []
		self.idx = 0
		self.RenderInput = RenderInput
		self.RFCA = RFCA.RFCA();

		for i in range(0,self.max):
			self.storage.append(None)
			self.newRun(i,fixargs)

	def newRun(self,index,args):
		index = index % self.max
		#print "[RenderRoulette] NEW " + str(index) + "|" + str(current_milli_time())
		self.storage[index] = RenderUnit(self.RenderInput)
		self.storage[index].hook = Thread(target = RenderUnit.Run, args = (self.storage[index],args ))
		self.storage[index].hook.start()

	def newCompress(self,index):
		index = index % self.max
		if self.storage[index].isComputing and not self.storage[index].RenderExecuted :
			print "Waiting for Renderer"
			while self.storage[index].isComputing == True :
				time.sleep(0.002)
		if self.storage[index].RenderExecuted:
			self.storage[index].Chook = Thread(target = RenderUnit.Compress, args = (self.storage[index],self.RFCA ))
			self.storage[index].Chook.start()

	def get(self,args):
		#print "[RenderRoulette] GET " + str(self.idx) + "|" + str(current_milli_time())
		result = None
		while self.storage[self.idx].isComputing == True:
			time.sleep(0.001)
		if self.storage[self.idx].compressed == True:
			result = self.storage[self.idx].compressedresult
		elif self.storage[self.idx].isFaulty == True:
			result = None
		#print "Calc Time: " + str(self.storage[self.idx].time) +"ms"
		#start new Instance
		self.newRun(self.idx,args)
		#update index
		self.idx = (self.idx +1)%self.max
		self.newCompress(self.idx)
		return result

class RenderUnit():
	def __init__(self,func):
		self.isFaulty = False
		self.isComplete = False
		self.isComputing = None
		self.func = func
		self.hook = None
		self.result = None
		self.time = 0
		self.compressed = False
		self.compressedresult = None
		self.RenderExecuted = False
		self.Chook = None

	def Run(self,args):
		self.isComputing = True
		self.time = current_milli_time()
		try:
			#print "[RenderRoulette] RND " + str(current_milli_time())
			self.result = self.func(args)
			self.isComplete = True
		except Exception,e:
			print e
			self.isFaulty = True
		self.isComputing = False
		self.time = current_milli_time()-self.time
		self.RenderExecuted = True

	def Compress(self,instance):
		if self.isComputing == False:
			if self.isFaulty == True:
				self.compressed = None
				return
			if self.result == None:
				return
		try:
			self.isComputing = True
			#print "[RenderRoulette] CMP " + str(current_milli_time())
			instance.addFrame(self.result.getColorArr())
			self.compressedresult = instance.getByteCode()
			self.isComputing = False
			self.compressed = True
		except Exception,e:
			print "[Compress]ERROR: " + str(e)
			self.isFaulty = True

