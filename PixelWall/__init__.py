from threading import Thread
import traceback
import Input
import Output
from Frame import Frame
from Parallel import TimeManager
import Core,Compression,Exceptions,Animations,Drawing,PresetAnimations,ParallelEngine
import Exceptions as Exceptions
from PresetAnimations import *
import PIL
__all__ = ["RFCA","Animations","Parallel","Frame","Output","Input","Core","Compression","Exceptions","Drawing","PresetAnimations","DBSC","ParallelEngine"]

class Engine():
    def __init__(self, XOutput, height = 32, width = 32,fps = 30, XInput = None):
        self.baseFrequency = fps
        self.frameHeight = height
        self.frameWidth = width
        self.brightness = float(1)
        self.Xinput = XInput
        self.Xoutput = XOutput
        self.lastFrame = None
        self.framenumber = 0
        self.AnimationManagementSystem = Animations.AnimationManager(self.baseFrequency)

    #def fireUp(self):
    #    self.TimeManagementSystem = Parallel.TimeManager()
    #    self.RenderTrigger = Parallel.TimeTrigger(self.baseFrequency, Engine.Render, self)
    #    self.TimeManagementSystem.triggers.append(self.RenderTrigger)
    #    self.TimeManagementSystem.fireUp()

    def fireUp(self):
        a = ParallelEngine.Manager(self.renderSubRout,self.Xoutput.output,fixargs = self);
        a.Renderfps = self.baseFrequency
        a.Launch()
    def __adjustBrightness(self):
        raise NotImplementedError

    def setBrightness(self, brightness):
        raise NotImplementedError

    def getBrightness(self):
        return self.brightness

    def Render(self):
        try:
            dFrame = Frame(self.frameHeight, self.frameWidth)
            dFrame.framenumber = self.framenumber
            self.framenumber +=1
            self.AnimationManagementSystem.Render(dFrame)
            self.Xinput.callData(dFrame)
            self.Xoutput.output(dFrame)
            self.lastFrame = dFrame
        except Exception,e:
            print e
            traceback.print_exc()
    @staticmethod
    def renderSubRout(self):
        self.framenumber +=1
        dFrame = Frame(self.frameHeight, self.frameWidth)
        dFrame.framenumber = self.framenumber
        self.AnimationManagementSystem.Render(dFrame)
        self.Xinput.callData(dFrame)
        self.lastFrame = dFrame
        return dFrame

