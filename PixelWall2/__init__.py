import sys,time,traceback,threading
from .frame import Frame

def __init__(self,height,width,fps=0,draw = None):
    self.fps = fps
    self.height = height
    self.width = width
    self.fps = fps
    self._drawFunction = draw
    self._backgroundFunction = None
    self._outputFunction = None
    self._inputFunction = None
    self._updateMode = "timer"
    self.frame = Frame(self.width,self.height)

def run(self,drawFunction, outputFunction,inputFunction = None):
    self._drawFunction = _drawFunction
    self._outputFunction = outputFunction
    self._inputFunction = inputFunction
    if self._updateMode == "timer":
        self.runner = threading.Thread(target=lambda: every(float(1)/self.fps, self._callUpdateFrame()))
        self.runner.start()
    elif self._updateMode == "callback":
        print(" * Updatemode is set to callback. Awaiting callback")

def inputCallback(self,frame):
    self.frame = frame
    self._callUpdateFrame(skipInput = True)

def setFps(self,fps):
    self.fps = fps
    self._updateMode = "timer"

def setUpdateByCall(self):
    self.fps = -1
    self._updateMode = "callback"

def halt(self):
    pass

def _callUpdateFrame(self,skipInput = False):
    if self._inputFunction != None and not skipInput:
        frame = Frame(self.width,self.height)
        self._inputFunction()
        self.frame = frame
    frame = self.frame.pilObject
    if self._drawFunction != None:
        self._callDraw()
    if self._outputFunction == None:
        print(" ! WARNING: Output funtion not set")

@staticmethod
def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay
