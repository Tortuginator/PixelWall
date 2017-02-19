import PixelWall

def testRND(dFrame):
	p = PixelWall.RenderObjects.Rectangle.Rectangle(PixelWall.Core.Point(0,0),PixelWall.Core.Point(20,26),(100,99,100),1)
	c = PixelWall.RenderObjects.Circle.Circle(PixelWall.Core.Point(10,10),(200,200,200),5)
	dFrame.addObject(p);
	dFrame.addObject(c);
	return dFrame
F = PixelWall.Input.Function(testRND);
O = PixelWall.Output.BinaryFile()
#O = Serial(port = "COM10")
R = PixelWall.Engine(28,28,F,O)
R.baseFrequency = 2
R.fireUp();
