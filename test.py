import PixelWall as PW
import time
def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
<<<<<<< HEAD
	newframe.setPixel(0,20,[200,200,200],True)
	newframe.setCircle(10,10,6);


	#newframe.setRectangle(5,10,5,10,[150,150,150]);
	#newframe.setRectangle(6,9,6,9,[255,0,0]);
	#newframe.setRectangle(2,3,3,9,[200,101,2]);
	#newframe.writeText(0,19,"aabb",[255,0,0])
=======
>>>>>>> origin/master
	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)
a.addAnimationFile("0.bmp",1,0,1,43,16,StartFrame = 0,Loop = False);
a.addAnimationFile("2.bmp",1,0,1,12,16,StartFrame = 45,Loop = False);
a.addAnimationFile("3.bmp",1,0,1,54,16,StartFrame = 60,Loop = False);
a.addAnimationFile("1.bmp",1,0,0,105,16,StartFrame = 120,Loop = True);
a.addAnimationFile("1.bmp",1,0,16,105,16,StartFrame = 120,Loop = True);
print a.Animations
while True:
	a.pushFrame()
	time.sleep(0.1);

<<<<<<< HEAD
a.pushFrame()
=======
>>>>>>> origin/master
