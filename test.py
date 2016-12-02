import PixelWall as PW

def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
	newframe.setPixel(0,20,[200,200,200],True)
	
	
	
	newframe.setRectangle(5,10,5,10,[150,150,150]);

	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)
a.addAnimationFile("0.bmp",1,0,1,43,16);
for i in range(0,30):
	a.pushFrame()
