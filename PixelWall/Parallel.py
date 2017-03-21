import socket,sys,time,datetime
from threading import Thread
import Core

class TimeTrigger():
	def __init__(self, timesPerSecond, function, args):
		self.timesPerSecond = timesPerSecond
		self.function = function
		self.args = args
		self.__setVars()
		self.isSleeping = True
		self.next = datetime.datetime.now()

	def __setVars(self):
		self.msDelta = float(1)/float(self.timesPerSecond)

	def isDue(self):
		if self.next < datetime.datetime.now():
			return True
		return False

	def doExecute(self, args = None):
		if self.isDue() is False:return False;
		self.next = datetime.datetime.now() + datetime.timedelta(seconds = self.msDelta)
		if args != None:
			self.args = args
		self.isSleeping = False
		self.function(self.args)
		self.isSleeping = True
		return True

class TimeManager():
	def __init__(self):
		self.baseFrequency = 60
		self.instance = None
		self.triggers = []

	def fireUp(self):
		try:
			self.instance = Thread(target = TimeManager.__tmeThread, args = (self,))
			self.instance.start()
			print "[+][PixelWall\Parallel\TimeManager][fireUp] Management thread started"
		except Exception,e:
			print e

	def __tmeThread(self):
		try:
			innerStep = 0
			innerMicrosecondDelta = (float(1)/float(self.baseFrequency))
			while(True):
				time.sleep(innerMicrosecondDelta)
				if innerStep >= self.baseFrequency-1:
					innerStep = 0
					innerTiming = datetime.datetime.now()
				innerStep +=1
				for i in self.triggers:
					if i.isSleeping is True:
						try:
							i.doExecute()
						except Exception,e:
							print "[!][PixelWall\Parallel\TimeManager][__tmeThread] Exception occured for " + repr(i.function)  + " @iteration " + repr(innerStep)
							print repr(e)
		except Exception,e:
			print e
