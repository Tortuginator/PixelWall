from threading import Thread
import traceback
from Frame import Frame
import Input,Output,Animations,Drawing,PresetAnimations,ParallelEngine
from PresetAnimations import *
import PIL
__all__ = ["RFCA","Animations","Parallel","Frame","Output","Input","Drawing","PresetAnimations","DBSC","ParallelEngine"]

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

    def fireUp(self):
        a = ParallelEngine.Manager(self.renderSubRout,self.Xoutput.sendImage,fixargs = self);
        a.Renderfps = self.baseFrequency
        a.Launch()

    @staticmethod
    def renderSubRout(self):
        self.framenumber +=1
        dFrame = Frame(self.frameHeight, self.frameWidth)
        dFrame.framenumber = self.framenumber
        self.AnimationManagementSystem.Render(dFrame)
        self.Xinput.callData(dFrame)
        self.lastFrame = dFrame
        return dFrame

