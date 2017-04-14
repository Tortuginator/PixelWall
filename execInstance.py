import PixelWall
import PIL
def testRND(dFrame):
	#dFrame.imgdraw.ellipse((0,0,10,10), fill="red", outline = "blue")
	#dFrame.imgdraw.line([(0,0),(0,27)],fill = "red")
	#dFrame.imgdraw.rectangle((0,20,28,28),fill = "blue")
	return dFrame

F = PixelWall.Input.Function(testRND)
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM6", compression = "LINEAR", loopback = False)
R = PixelWall.Engine(width = 28, height = 28, XInput = F, XOutput = O, fps = 5)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 200)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Chill,startframe = 0,infinity = True)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Matrix,startframe = 0,infinity = True)
testGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Circle3.gif",Position = (0,0))
Ani = PixelWall.Animations.Animation(rFunc = testGIF, startframe = 0, infinity = True, tourCount = 0)
R.AnimationManagementSystem.addAimation(Ani);
R.fireUp();
