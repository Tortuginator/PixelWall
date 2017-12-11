import PixelWall
from PIL import Image,ImageFont
font = ImageFont.truetype("Silkscreen.ttf",size = 8)
def filteri(dFrame):
	#dFrame.imgdraw.text((0,14),"Hello",font=font,fill=(255,255,255,0))
	#print "adding text"
	pass

F = PixelWall.Input.Function(filteri)
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM6", compression = "RFCA", loopback = False)
R = PixelWall.Engine(width = 28, height = 28, XInput = F, XOutput = O, fps = 55)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 0)
#testChill = PixelWall.PresetAnimations.Chill.Chill(ColorLower=(20,0,200),ColorHigher = (100,50,255))
#Ani = PixelWall.Animations.Animation(rFunc = testChill,startframe = 0,infinity = True)
#testMatrix = PixelWall.PresetAnimations.Matrix.Matrix(Length = 10,Color = (0,200,0))
#Ani = PixelWall.Animations.Animation(rFunc = testMatrix,startframe = 0,infinity = True)
testGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Lines.gif",Position = (-2,-2))
Ani = PixelWall.Animations.Animation(rFunc = testGIF, startframe = 0, infinity = True, tourCount = 0)
#testSnake = PixelWall.PresetAnimations.SnakeOnSpeed.SnakeOnSpeed()
#Ani = PixelWall.Animations.Animation(rFunc = testSnake, startframe = 0, infinity = True, tourCount = 0)
#testGoF = PixelWall.PresetAnimations.GameOfLife.GameOfLife(position = (10,10),pattern = [[1,1,1,1,1,1,1,1],[1,0,1,1,1,1,0,1],[1,1,1,1,1,1,1,1]])
#Ani = PixelWall.Animations.Animation(rFunc = testGoF, startframe = 0, infinity = True, tourCount = 0)
#testSPL = PixelWall.PresetAnimations.Spline.Spline(object = 0,speed = 1,startPosition = (0,0),endPosition = (20,20))
#Ani = PixelWall.Animations.Animation(rFunc = testSPL, startframe = 0, infinity = True, tourCount = 0)
#testSPLDelay = PixelWall.PresetAnimations.Spline.Spline(object = 0,speed = 0.5,startPosition = (20,20),endPosition = (10,13))
#AniDelay = PixelWall.Animations.Animation(rFunc = testSPLDelay, startframe = 29, infinity = True, tourCount = 0)
Ani.debug = False
R.AnimationManagementSystem.addAimation(Ani);
#R.AnimationManagementSystem.addAimation(AniDelay);
R.fireUp();
