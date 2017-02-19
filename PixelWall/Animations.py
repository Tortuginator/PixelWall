import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions,Frame

class AnimationManager():
    def __init__(self,fps):
        self.Animations = []
        self.fps = fps
    def Render(self,dFrame):
        for i in self.Animations:
            if self.disabled is True:continue;
            currIter = i.getIteration(dFrame.framenumber,self.fps)
            if i.last != currIter[0]:
                if i.last == None:
                    i.last = currIter[0]
                    i.prev = currIter[0]
                i.prev = i.last
                i.last = currIter[0]

            if self.smooth is True:
                i.Render(i.prev,1-currIter[1],dFrame)
                i.Render(currIter[0],currIter[1],dFrame)
            else:
                i.Render(currIter[0],100,dFrame)

    def addAimation(self,ani):
        if not isinstance(ani,Animation):
            raise Exceptions.unexpectedType(variable = "ani",type="PixelWall.Animations.Animation")
        self.Animation.append(ani)


class AnimationSpeed():
    framebased = 1
    timebased = 2

class Animation(Object):
    def __init__(self,fps,speedtype,speed,startframe = 0,tourCount = 1,speedfactor = 1,tourLength = 0,infinity = False,smooth = False):
        if smooth not in [True,False]:
            return "Smooth must be of type bool"
        self.smooth = smooth
        self.tourLength = tourLength
        self.speedtype = speedtype
        if int(speed) < 1:return "ERROR";
        self.speed = int(speed)
        if self.infinity not in [True,False]:
            return "Infinity must be of type bool"
        self.infinity = infinity
        self.startframe = startframe
        self.last = None
        self.prev = None
        self.disabled = False
        if self.speedfactor =< 0:
            return "The speedfactor cant be negative or 0"
        self.speedfactor = float(speedfactor)
        if self.infinity is True and self.tourCount != 0:
            return "You can't say, that the Animation should run indefinetely and at the same time should terminate after x tours"
        #SET VARS
        if self.speedtype == 1:
            self.tps = float(fps)/self.speed # tps => TimesPerSecond
        elif self.speedtype == 2:
            self.tps = float(self.speed)/fps
        else:
            return "ERROR"
        self.tps = self.tps*(1/self.speedfactor)
            #TODO implement real error

    def isDue(self,CurrentAbsoluteFrame,fps):
        if self.last != self.getIteration(CurrentAbsoluteFrame,fps) and self.disabled is not True:
            return True
        return False
        """if self.nextDEL == True:
            return False
        if self.CurrenAbsoluteFrame < self.startframe:
            return False
        if last == None:
            return True
        tmpl = self.last + self.tps
        if self.tourLength != 0 and self.infinity == False:
            if self.speedtype == 1
                if (self.startframe + self.tourLength*self.tourCount) < tmpl):
                    self.disabled = True
                    return True
            elif self.speedtype == 2:
                if (self.startframe + self.tourLength*(self.tourCount*fps)) < tmpl):
                    self.disabled = True
                    return True
        if CurrentAbsoluteFrame >= tmpl:
            return True
        return False"""
    def getIteration(self,CurrentAbsoluteFrame,fps):
        if self.infinity is True:
            return ((CurrentAbsoluteFrame - self.startframe)//self.tps,int(float((CurrentAbsoluteFrame - self.startframe)%self.tps)/self.tps)*100)
        elif self.infinity is False:
            if self.speedtype == 1:
                if CurrentAbsoluteFrame > self.startframe+(self.tourLength * self.tourCount)
                    self.disabled = True
                    return (self.tourLength,100)
            elif self.speedtype == 2:
                if CurrentAbsoluteFrame > self.startframe+(self.tourLength*fps * self.tourCount
                    self.disabled = True
                    return (self.tourLength,100)

                p = CurrentAbsoluteFrame - self.startframe
                if self.speedtype == 2:
                    p = t%(self.tourLength*fps)#The tourLength is there in seconds
                elif self.speedtype == 1:
                    p = t%self.tourLength
                t = p//self.tps
                return (t,int(float(p%self.tps)/self.tps)*100)
        return "ERROR was not able to determine the iteration"
    def Render(self,iteration,opacity,dFrame):
        raise NotImplementedError
