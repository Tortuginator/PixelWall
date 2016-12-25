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
a.addAnnimationTest(factor = 0.1);
#a.addAnimationPattern(colorRangeA = (0,0,0),colorRangeB= (255,255,255));
#a.addAnnimationCircle(15,10,20,(0,100,0),Loop = True,StartFrame = 0,colorGRAD = (0,0,0),factor = 1,length = 4)

print a.Animations

while True:
	a.pushFrame()
	time.sleep(1/30);
