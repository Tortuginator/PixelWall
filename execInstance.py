import PixelWall
import PIL
def testRND(dFrame):
	#dFrame.imgdraw.ellipse((0,0,10,10), fill="red", outline = "blue")
	#dFrame.imgdraw.line([(0,0),(0,27)],fill = "red")
	#dFrame.imgdraw.rectangle((0,20,28,28),fill = "blue")
	return dFrame

F = PixelWall.Input.Function(testRND);
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM10",compression = "RAW")
R = PixelWall.Engine(28,28,F,O,fps = 10)
Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 200)
R.AnimationManagementSystem.addAimation(Ani);
R.fireUp();
