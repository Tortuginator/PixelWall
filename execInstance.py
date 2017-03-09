import PixelWall

def testRND(dFrame):
	p = PixelWall.RenderObjects.Rectangle.Rectangle(PixelWall.Core.Point(0,0),PixelWall.Core.Point(20,26),(100,99,100),1)
	c = PixelWall.RenderObjects.Circle.Circle(PixelWall.Core.Point(10,10),(200,200,200),5)
	dFrame.addObject(p);
	dFrame.addObject(c);
	return dFrame
F = PixelWall.Input.Function(testRND);
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM10",compression = "RFCA")
R = PixelWall.Engine(28,28,F,O)
#def __init__(self,fps,speedtype,speed,rFunc,startframe = 0,tourCount = 1,speedfactor = 1,tourLength = 0,infinity = False,smooth = False):
Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 30)
R.AnimationManagementSystem.addAimation(Ani);
R.baseFrequency = 2
R.fireUp();
