import PixelWall

def testRND(dFrame):
	#p = PixelWall.RenderObjects.Rectangle.Rectangle(PixelWall.Core.Point(0,0),PixelWall.Core.Point(20,20),(100,100,100),1)
	c = PixelWall.RenderObjects.Circle.Circle(PixelWall.Core.Point(10,10),(200,200,100),10)
	#dFrame.addObject(p);
	dFrame.addObject(c);
	dFrame.setPixel(PixelWall.Core.Point(27,27),(100,20,250))
	return dFrame
F = PixelWall.Input.Function(testRND);
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM10",compression = "RFCA")
R = PixelWall.Engine(28,28,F,O)
Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 30)
R.AnimationManagementSystem.addAimation(Ani);
R.baseFrequency = 10
R.fireUp();
