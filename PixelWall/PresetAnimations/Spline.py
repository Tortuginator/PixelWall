import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class Spline(PresetAnimations.AnimationInstance):
    @staticmethod
    def pythagoras(a,b,percision = True):
        if percision is True:
            a = float(a)
            b = float(b)
        return math.sqrt((a**2)+(b**2))

    def dynamicDuration(self):
        return True

    def extendedInit(self):
        self.object = None
        if "object" in self.args:
            self.object = self.args["object"]

        assert self.object != None,"please specify a object rendering function"

        self.speed = 1
        if "speed" in self.args:
            self.speed = self.args["speed"]

        self.StartPosition = (0,0)
        if "startPosition" in self.args:
            self.StartPosition = self.args["startPosition"]

        self.EndPosition = (0,0)
        if "endPosition" in self.args:
            self.EndPosition = self.args["endPosition"]

        self.STORstep = 0
        self.STORtotalstep = Spline.pythagoras(self.EndPosition[0]-self.StartPosition[0],self.EndPosition[1]-self.StartPosition[1],percision = True)
        self.STORdiff = (self.EndPosition[0]-self.StartPosition[0],self.EndPosition[1]-self.StartPosition[1])
        self.STORstepdiff = (float(self.STORdiff[0])/self.STORtotalstep,float(self.STORdiff[1])/self.STORtotalstep)
        print "approximate Duration",self.STORtotalstep
    def Render(self):
        #check
        if self.STORstep == 0:
            oldStep = 0
        else:
            oldStep = self.STORstep-1

        posNEW = self.StartPosition
        #posOLD = (posNEW[0]+self.STORstepdiff[0]*oldStep,posNEW[1]+self.STORstepdiff[1]*oldStep)
        posNEW = (posNEW[0]+self.STORstepdiff[0]*self.STORstep,posNEW[1]+self.STORstepdiff[1]*self.STORstep)
        self.STORstep +=self.speed
        #self.dFrame.imgdraw.point(posOLD,(255,255,255,128))
        self.dFrame.imgdraw.point(posNEW,(255,255,255,255))
        if self.STORstep > self.STORtotalstep:
            self.parent.toRemove = True
