import PixelWall
from PIL import Image,ImageFont
font = ImageFont.truetype("Silkscreen.ttf",size = 8)
def filteri(dFrame):

F = PixelWall.Input.Function(testRND)
#O = PixelWall.Output.BinaryFile()
O = PixelWall.Output.Serial(port = "COM6", compression = "RFCA", loopback = False)
R = PixelWall.Engine(width = 28, height = 28, XInput = F, XOutput = O, fps = 90)
#Ani = PixelWall.Animations.Animation(rFunc = PixelWall.AnimationFunctions.Circle2,startframe = 0,infinity = True,tourLength = 200)
#testChill = PixelWall.PresetAnimations.Chill.Chill(ColorLower=(150,100,0),ColorHigher = (255,200,0))
#Ani = PixelWall.Animations.Animation(rFunc = testChill,startframe = 0,infinity = True)
#testMatrix = PixelWall.PresetAnimations.Matrix.Matrix(Length = 10,Color = (0,200,0))
#Ani = PixelWall.Animations.Animation(rFunc = testMatrix,startframe = 0,infinity = True)
testGIF = PixelWall.PresetAnimations.GIF.GIF(File = "GIF\Boxes.gif",Position = (-2,-2))
Ani = PixelWall.Animations.Animation(rFunc = testGIF, startframe = 0, infinity = True, tourCount = 0)
R.AnimationManagementSystem.addAimation(Ani);
R.fireUp();
