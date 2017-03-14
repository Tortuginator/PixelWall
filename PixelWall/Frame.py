import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions
from PIL import Image,ImageDraw
class Frame():
	def __init__(self,height,width):
		self.framenumber = 0
		self.height = height;
		self.width = width;
		self.PixelCount = height*width
		self.FunctionStorage = []
		self.img = Image.new("RGBA",(self.height,self.width),(0,0,0,0));
		self.imgdraw = ImageDraw.Draw(self.img)

	def getColorArr(self):
		R = [];
		G = []
		B = []
		for i in list(self.img.getdata()):
			R.append(i[0])
			G.append(i[1])
			B.append(i[2])
		return [R,G,B]
