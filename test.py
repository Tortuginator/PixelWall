import PixelWall as PW
import time
def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
	newframe.circle(5,5,(1,2),5,(0,254,0));
	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)
#a.addAnimationFile("0.bmp",1,0,1,43,16,StartFrame = 0,Loop = False);
#a.addAnimationFile("2.bmp",1,0,1,12,16,StartFrame = 45,Loop = False);
#a.addAnimationFile("3.bmp",1,0,1,54,16,StartFrame = 60,Loop = False);
#a.addAnimationFile("1.bmp",1,0,0,105,16,StartFrame = 120,Loop = True);
#a.addAnimationFile("1.bmp",1,0,16,105,16,StartFrame = 120,Loop = True);
print a.Animations
while True:
	a.pushFrame()
	time.sleep(0.1);
