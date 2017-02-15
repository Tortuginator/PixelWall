import socket,sys,time,datetime
from threading import Thread
import Core

class TimeTrigger():
	def __init__(self,timesPerSecond,function,args):
		self.timesPerSecond = timesPerSecond
		self.function = function
		self.args = args
		self.__setVars();
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
		self.function(self.args);
		self.isSleeping = True
		return True

class TimeManager():
	def __init__(self):
		self.baseFrequency = 120
		self.instance = None
		self.triggers = []

	def fireUp(self):
		self.instance = Thread(target = TimeManager.__tmeThread, args = (self,self.triggers))

	def __tmeThread(self,triggers):
		innerStep = 0
		innerMicrosecondDelta = (int(float(1)/float(self.baseFrequency))*100000)
		while(True):
			if innerStep*innerMicrosecondDelta > current_milli_time():
				time.sleep(0.001)
				continue
			if innerStep >= self.baseFrequency-1:
				innerStep = 0
				innerTiming = datetime.datetime.now()
			innerStep +=1
			for i in triggers:
				if i.isSleeping is True:
					try:
						i.doExecute()
					except Exception,e:
						Core.UtilPrint.compose("!",self.__class__,__name__,"Exception occured for " + repr(i.function)  + " @iteration " + repr(innerStep))
						Core.UtilPrint.compose("!",self.__class__,__name__,repr(e))

		def __tmeExec(self,function,args):
			pass
