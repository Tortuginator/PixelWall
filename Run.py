import PixelWall as PW
import time
import PresetAnimations as PA
def myFrameGenerator(newframe,fps,frameCount,frameInSecond):
	#newframe.circle(5,5,(1,2),5,(0,254,0));
	#newframe.drawCircle(0,8,5,(0,254,0));
	#newframe.circle(0,8,4,(0,200,0));
	#newframe.circle(0,8,3,(0,160,0));
	#newframe.writeText(0,10,"789",(255,255,255))
	return newframe


a = PW.RenderEngine(21,33,30)
a.setInputRenderer(myFrameGenerator)
#a.addAnimationCustom(Name="Test",StartFrame = 0,Length = 90,Factor = 0.01,Function = PA.Presets.Test)
a.addAnimationCustom(Name = "Circle2a",StartFrame=0,Count = 0,Length = 10,Factor = 0.001,Function = PA.Presets.Circle2,Parameters = {"Color":(255,0,0),"ColorGRAD":(0,0,0),"Length":5,"X":10,"Y":10,"FadeOut":10})
a.addAnimationCustom(Name = "Circle2b",StartFrame=0,Count = 0,Length = 10,Factor = 0.001,Function = PA.Presets.Circle2,Parameters = {"Color":(0,255,0),"ColorGRAD":(0,0,0),"Length":5,"X":20,"Y":10,"FadeOut":10})

while True:
	a.pushFrame()
	time.sleep(1/30);
