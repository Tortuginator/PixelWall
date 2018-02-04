import PixelWall
from PIL import Image,ImageFont
font = ImageFont.truetype("Silkscreen.ttf",size = 7)
from datetime import datetime
from time import gmtime, strftime
global counter
counter = 0
def filteri(dFrame):
	#Jodel = Image.open('Jodel.jpg').convert('RGBA')
	#dFrame.img = Image.alpha_composite(dFrame.img,Jodel)
	pass
F = PixelWall.Input.Function(filteri)
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.SimpleSerial(port = "COM6", compression = "RFCA", loopback = False)
R = PixelWall.Engine(width = 28, height = 28, XInput = F, XOutput = O, fps = 60)
#testChill = PixelWall.PresetAnimations.Chill.Chill(ColorLower=(0,100,150),ColorHigher = (20,190,255))
#Ani = PixelWall.Animations.Animation(rFunc = testChill,startframe = 0,infinity = True)

#testMatrix = PixelWall.PresetAnimations.Matrix.Matrix(Length = 15,Color = (0,150,0))
#Ani = PixelWall.Animations.Animation(rFunc = testMatrix,startframe = 0,infinity = True)

testGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Ball1.gif",Position = (-2,-2))
Ani = PixelWall.Animations.Animation(rFunc = testGIF, startframe = 0, infinity = True, tourCount = 0)

testPhysics = PixelWall.PresetAnimations.ForcesOfPhysics.ForcesOfPhysics()
Ani = PixelWall.Animations.Animation(rFunc = testPhysics,startframe = 0,infinity = True,tourCount = 0)
#testSnake = PixelWall.PresetAnimations.SnakeOnSpeed.SnakeOnSpeed()
#Ani = PixelWall.Animations.Animation(rFunc = testSnake, startframe = 0, infinity = True, tourCount = 0)

#testGoF = PixelWall.PresetAnimations.GameOfLife.GameOfLife(position = (10,10),pattern = [[1,1,1,1,1,1,1,1],[1,0,1,1,1,1,0,1],[1,1,1,1,1,1,1,1]])
#Ani = PixelWall.Animations.Animation(rFunc = testGoF, startframe = 0, infinity = True, tourCount = 0)
#Ani.debug = False
R.AnimationManagementSystem.addAimation(Ani);
#R.AnimationManagementSystem.addAimation(AniDelay);
R.fireUp();
