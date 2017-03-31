import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions,Frame

class AnimationManager():
    def __init__(self, fps):
        self.Animations = []
        self.fps = fps

    def Render(self, dFrame):
        for i in self.Animations:
            if i.disabled is True: continue;
            currIter = i.getIteration(dFrame.framenumber, self.fps)
            print "Current Iteration" , currIter
            if i.last != currIter:
                if i.last == None:
                    i.last = currIter
                    i.prev = currIter
                i.prev = i.last
                i.last = currIter

            if i.smooth is True:
                #Enhance
                i.Render(currIter, dFrame)
            else:
                i.Render(currIter, dFrame)

    def addAimation(self,ani):
        self.Animations.append(ani)

class Animation(object):
    def __init__(self, rFunc, startframe = 0, tourCount = 0, tourLength = 0, infinity = False, smooth = False):
        if smooth not in [True, False]:
            return "Smooth must be of type bool"
        self.smooth = smooth
        self.tourLength = tourLength
        if infinity not in [True, False]:
            return "Infinity must be of type bool"
        self.infinity = infinity
        self.startframe = startframe
        self.last = None
        self.prev = None
        self.disabled = False
        self.tourCount = tourCount
        self.rFunc = rFunc
        if self.infinity is True and self.tourCount != 0:
            print "You can't say, that the Animation should run indefinetely and at the same time should terminate after x tours"

    def setInstance(self,instance):
        self.rFunc = instance

    def isDue(self, CurrentAbsoluteFrame, fps):
        if self.last != self.getIteration(CurrentAbsoluteFrame, fps) and self.disabled is not True:
            return True
        return False

    def getIteration(self, CurrentAbsoluteFrame, fps):
        if self.infinity is True:
            if self.tourLength == 0:
                return CurrentAbsoluteFrame - self.startframe
            else:
                return (CurrentAbsoluteFrame - self.startframe)%self.tourLength
        elif self.infinity is False:
            if CurrentAbsoluteFrame > self.startframe+(self.tourLength * self.tourCount):
                self.disabled = True
                return self.tourLength

            p = CurrentAbsoluteFrame - self.startframe
            p = p%self.tourLength
            return p
        print "ERROR was not able to determine the iteration"

    def Render(self,iteration,dFrame):
        self.rFunc.dFrame = dFrame
        self.rFunc.setIteration(iteration)
        self.rFunc.Render()
