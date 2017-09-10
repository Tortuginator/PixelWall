import sys
sys.path.append('.\PixelWall')
from PixelWall import Frame

class AnimationManager():
    def __init__(self, fps):
        self.Animations = []
        self.fps = fps
        self.removeList = []
    def Render(self, dFrame):
        for r in range(0,len(self.Animations)):
            i = self.Animations[r]
            if i.disabled is True: continue;
            if i.toRemove is True: self.removeList.append(r);continue;
            currIter = i.getIteration(dFrame.framenumber, self.fps)
            if currIter < 0:continue;
            if i.debug:print "[-] Current Iteration for ",i.rFunc, "@",currIter;
            if i.last != currIter:
                if i.last == None:
                    i.last = currIter
                    i.prev = currIter
                i.prev = i.last
                i.last = currIter

                i.Render(currIter, dFrame)

        for i in self.removeList:
            del self.Animations[i]
        del self.removeList[:]

    def addAimation(self,ani):
        self.Animations.append(ani)

    def clear(self):
        del self.Animations[:]

class Animation(object):
    def __init__(self, rFunc, startframe = 0, tourCount = 0, tourLength = 0, infinity = False, smooth = False,debug = False,dynamicDuration = False):
        assert type(infinity) == bool,"The argument 'infinity' needs to be of type bool"
        assert type(smooth) == bool,"The argument 'smooth' needs to be of type bool"
        assert type(debug) == bool,"The argument 'debug' needs to be of type bool"
        assert startframe >= 0,"The argument 'startframe' can't be below 0"
        assert tourLength >= 0, "The argument 'tourLength' can't be below 0"
        assert tourCount >= 0, "The argument 'tourCount' can't be below 0"

        self.smooth = smooth
        self.tourLength = tourLength
        self.infinity = infinity
        self.startframe = startframe
        self.debug = debug
        self.last = None
        self.prev = None
        self.disabled = False
        self.toRemove = False
        self.tourCount = tourCount
        self.rFunc = rFunc
        self.dynamic = dynamicDuration
        if self.infinity is True and self.tourCount != 0 and not dynamicDuration is True:
            print "You can't say, that the Animation should run indefinetely and at the same time should terminate after x tours"

        if dynamicDuration is True:
            self.tourCount = 0
            self.infinity = True
            self.tourLength = 1

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
        self.rFunc.setParent(self)
        self.rFunc.setIteration(iteration)
        self.rFunc.Render()
