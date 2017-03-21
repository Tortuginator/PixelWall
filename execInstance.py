import PixelWall
import PIL
def testRND(dFrame):
	#dFrame.imgdraw.ellipse((0,0,10,10), fill="red", outline = "blue")
	#dFrame.imgdraw.line([(0,0),(0,27)],fill = "red")
	#dFrame.imgdraw.rectangle((0,20,28,28),fill = "blue")
	return dFrame

F = PixelWall.Input.Function(testRND)
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM6",compression = "RFCA")
R = PixelWall.Engine(28,28,F,O,fps = 5)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 200)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Chill,startframe = 0,infinity = True)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Matrix,startframe = 0,infinity = True)
Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.GIF,startframe = 0,infinity = True,args = {"File":"GIF\Boxes.gif"})
R.AnimationManagementSystem.addAimation(Ani);
R.fireUp();
