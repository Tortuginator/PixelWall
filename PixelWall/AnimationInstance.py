import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions,Frame

class AnimationInstance():
    def __init__(self,dFrame,**args):
        self.dFrame = dFrame
        self.iteration = 0
        self.running = True
        self.args = args
        self.extendedInit()

    def setIteration(self,iteration):
        assert int(iteration) >= 0,"Iteration needs to be greater or same then 0"
        self.iteration = int(iteration)

    def start(self):
        self.runing = True

    def stop(self):
        self.running = False

    def _Render(self,**kwargs):
        raise NotImplementedError("This function needs to be implemented")

    def next(self,**kwargs):
        if self.running:
            self._Render(kwargs)

    def extendedInit(self):
        pass
