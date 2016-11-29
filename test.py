import PixelWall as PW

def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
	newframe.setPixel(0,20,[200,200,200],True)
	newframe.setRectangle(5,10,5,10,[150,150,150]);
	newframe.setRectangle(6,9,6,9,[255,0,0]);
	newframe.setRectangle(2,3,3,9,[200,101,2]);
	newframe.writeText(0,19,"01!24",[255,0,0])
	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)

a.pushFrame()