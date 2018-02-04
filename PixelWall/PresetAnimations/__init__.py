
__all__ = ["Circle2","Matrix","Clock","Chill","GIF","GameOfLife","Spline","SnakeOnSpeed","BubbleField","ForcesOfPhysics"]

class AnimationInstance():
    def __init__(self,**args):
        self.dFrame = None
        self.iteration = 0
        self.args = args
        self.parent = None
        self.extendedInit()

    def setIteration(self,iteration):
        assert int(iteration) >= 0,"Iteration needs to be greater or same then 0"
        self.iteration = int(iteration)

    def Render(self):
        raise NotImplementedError("This function needs to be implemented")

    def extendedInit(self):
        pass

    def setPrevframe(self):
        pass

    def dynamicDuration(self):
        return False

    def setParent(self,parent):
        self.parent = parent
