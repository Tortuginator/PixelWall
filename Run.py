import PixelWall as PW
import time
def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
	#newframe.circle(5,5,(1,2),5,(0,254,0));
	#newframe.drawCircle(0,8,5,(0,254,0));
	#newframe.circle(0,8,4,(0,200,0));
	#newframe.circle(0,8,3,(0,160,0));
	#newframe.writeText(0,10,"789",(255,255,255))
	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)
#a.addAnnimationTest();
#addAnimationPattern(self,Loop=True,Startframe = 1,factor = 1,colorRangeA=(0,0,0),colorRangeB=(255,255,255),RGBCorrelated = False):
a.addAnimationPattern(colorRangeA = (0,0,0),colorRangeB= (255,255,255));
#a.addAnnimationCircle(15,10,20,(0,100,0),Loop = True,StartFrame = 0,colorGRAD = (0,0,0),factor = 1,length = 4)
#a.addAnimationFile("0.bmp",1,0,1,43,16,StartFrame = 0,Loop = False);
#a.addAnimationFile("2.bmp",1,0,1,12,16,StartFrame = 45,Loop = False);
#a.addAnimationFile("3.bmp",1,0,1,54,16,StartFrame = 60,Loop = False);
#a.addAnimationFile("1.bmp",1,0,0,105,16,StartFrame = 120,Loop = True);
#a.addAnimationFile("1.bmp",1,0,16,105,16,StartFrame = 120,Loop = True);
print a.Animations

while True:
	a.pushFrame()
	time.sleep(1/30);
