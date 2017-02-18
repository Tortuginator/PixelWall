from threading import Thread

import Input
import Output
from Frame import Frame
from Format import FrameFormat
from Parallel import TimeManager
import Core,Compression,Exceptions
from PixelWall.RenderObjects import *

__all__ = ["Parallel","Frame","Format","Output","Input","Core","Compression","Exception","RenderObjects"]

class Engine():
    def __init__(self,height,width,Xinput,Xoutput):
        self.baseFrequency = 30
        self.frameHeight = height
        self.frameWidth = width
        self.brightness = float(1)
        self.Xinput = Xinput
        self.Xoutput = Xoutput
        self.lastFrame = None

    def fireUp(self):
        self.TimeManagementSystem = Parallel.TimeManager()
        self.RenderTrigger = Parallel.TimeTrigger(self.baseFrequency, Engine.Render, self)
        self.TimeManagementSystem.triggers.append(self.RenderTrigger)
        self.TimeManagementSystem.fireUp()

    def __adjustBrightness(self):
        raise NotImplementedError

    def setBrightness(self,brightness):
        raise NotImplementedError

    def getBrightness(self):
        return self.brightness

    def Render(self):
        try:
            dFrame = Frame(self.frameHeight, self.frameWidth)
            updatedFrame = self.Xinput.updateSinceLastCall()
            if not updatedFrame:
                return
            self.Xinput.setArgs(dFrame)
            A = self.Xinput.callData()
            if A is None:
                print "[!][PixelWall\init\Engine][Render] Some error Occured while Calling the Input data"
                return
            if A is False:
                return #skip if previously a error occured

            self.Xoutput.output(A)
            self.lastFrame = A
        except Exception,e:
            print e
