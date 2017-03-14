from threading import Thread
import traceback
import Input
import Output
from Frame import Frame
from Format import FrameFormat
from Parallel import TimeManager
import Core,Compression,Exceptions,Animations,AnimationFunctions
import Exceptions as Exceptions
import PIL
__all__ = ["RFCA","AnimationFunctions","Animations","Parallel","Frame","Format","Output","Input","Core","Compression","Exceptions"]

class Engine():
    def __init__(self,height,width,Xinput,Xoutput,fps = 30):
        self.baseFrequency = fps
        self.frameHeight = height
        self.frameWidth = width
        self.brightness = float(1)
        self.Xinput = Xinput
        self.Xoutput = Xoutput
        self.lastFrame = None
        self.framenumber = 0
        self.AnimationManagementSystem = Animations.AnimationManager(self.baseFrequency)

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
            dFrame.framenumber = self.framenumber
            self.framenumber +=1
            updatedFrame = self.Xinput.updateSinceLastCall()
            if not updatedFrame:
                return
            self.Xinput.setArgs(dFrame)
            A = self.Xinput.callData()
            print "calling imput"
            if A is None:
                print "[!][PixelWall\init\Engine][Render] Some error Occured while Calling the Input data"
                return
            if A is False:
                return #skip if previously a error occured
            self.AnimationManagementSystem.Render(dFrame);
            self.Xoutput.output(A)
            self.lastFrame = A
        except Exception,e:
            print e
            traceback.print_exc()
