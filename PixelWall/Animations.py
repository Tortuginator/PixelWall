import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions,Frame

class AnimationManager():
    def __init__(self,fps):
        self.Animations = []
        self.fps = fps

    def Render(self,dFrame):
        for i in self.Animations:
            if i.disabled is True:continue;
            currIter = i.getIteration(dFrame.framenumber,self.fps)
            print "Current Iteration" , currIter
            if i.last != currIter[0]:
                if i.last == None:
                    i.last = currIter[0]
                    i.prev = currIter[0]
                i.prev = i.last
                i.last = currIter[0]

            if i.smooth is True:
                i.Render(i.prev,1-currIter[1],dFrame)
                i.Render(currIter[0],currIter[1],dFrame)
            else:
                i.Render(currIter[0],100,dFrame)

    def addAimation(self,ani):
        self.Animations.append(ani)

class Animation(object):
    def __init__(self,rFunc,startframe = 0,tourCount = 0,tourLength = 0,infinity = False,args = {},smooth = False):
        if smooth not in [True,False]:
            return "Smooth must be of type bool"
        self.smooth = smooth
        self.tourLength = tourLength
        if infinity not in [True,False]:
            return "Infinity must be of type bool"
        self.infinity = infinity
        self.startframe = startframe
        self.last = None
        self.prev = None
        self.disabled = False
        self.tourCount = tourCount
        self.storage = []
        self.rFunc = rFunc
        if self.infinity is True and self.tourCount != 0:
            return "You can't say, that the Animation should run indefinetely and at the same time should terminate after x tours"
        #SET VARS

            #TODO implement real error
    def isDue(self,CurrentAbsoluteFrame,fps):
        if self.last != self.getIteration(CurrentAbsoluteFrame,fps) and self.disabled is not True:
            return True
        return False

    def getIteration(self,CurrentAbsoluteFrame,fps):
        if self.infinity is True:
            if self.tourLength == 0:
                return (CurrentAbsoluteFrame - self.startframe,100)
            else:
                return ((CurrentAbsoluteFrame - self.startframe)%(self.tourLength),100)
        elif self.infinity is False:
            if CurrentAbsoluteFrame > self.startframe+(self.tourLength * self.tourCount):
                self.disabled = True
                return (self.tourLength,100)

            p = CurrentAbsoluteFrame - self.startframe
            p = p%self.tourLength
            return (p,100)
        print "ERROR was not able to determine the iteration"

    def Render(self,iteration,opacity,dFrame,args = {}):
        self.rFunc(self,iteration,opacity,dFrame,arguments = args);
