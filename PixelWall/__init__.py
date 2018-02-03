from threading import Thread
import traceback,time
from Frame import Frame
import Input,Output,Animations,Drawing,PresetAnimations,ParallelEngine
from PresetAnimations import *
import PIL
__all__ = ["RFCA","Animations","Parallel","Frame","Output","Input","Drawing","PresetAnimations","DBSC","ParallelEngine"]

current_milli_time = lambda: int(round(time.time() * 1000))

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
        #a = ParallelEngine.Manager(self.renderSubRout,self.Xoutput.sendImage,fixargs = self);
        #a.Renderfps = self.baseFrequency
        #a.Launch()
        self.Watchdog = Thread(target = Engine.__Watchdog, args = (self,))
        self.Watchdog.start()

    def __Watchdog(self):
        self.RFCA = RFCA.RFCA();
        freqency = int(1000/float(self.baseFrequency))
        timeInterval = current_milli_time() + freqency
        while 1:
            internalFrame = Engine.renderSubRout(self)
            fakeFrame = internalFrame.getColorArr()
            r,g,b = fakeFrame
            fakeFrame = [r,g,b]
            self.RFCA.addFrame(fakeFrame)
            preparedFrame = self.RFCA.getByteCode()
            while(current_milli_time() < timeInterval):
                pass
            timeInterval = current_milli_time() + freqency
            self.Xoutput.sendImage(preparedFrame)

    @staticmethod
    def renderSubRout(self):
        self.framenumber +=1
        dFrame = Frame(self.frameHeight, self.frameWidth)
        dFrame.framenumber = self.framenumber
        self.AnimationManagementSystem.Render(dFrame)
        self.Xinput.callData(dFrame)
        self.lastFrame = dFrame
        return dFrame
