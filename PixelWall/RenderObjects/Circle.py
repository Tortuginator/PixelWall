from __init__ import FrameFunction
import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Exceptions,Frame
class Circle(FrameFunction):
	def __init__(self,centerPoint,color,radius,fill = False,fillcolor = 0,opacity = 1):
		self.centerPoint = centerPoint
		self.color = color
		self.radius = radius
		self.fill = fill
		self.fillcolor = fillcolor
		self.opacity = opacity
		if not isinstance(centerPoint,Core.Point):
			raise Exceptions.unexpectedType(variable = "centerPoint",type="Core.Point")

	def Render(self,dFrame):
		x0 = self.centerPoint.x
		y0 = self.centerPoint.y
		if Frame.isColor(self.color) is False:return 0;
		colour = Frame.isColor(self.color);
		#if Frame.isColor(fillColor) is False:return 0;
		if self.radius <= 0:	return 0;

		#Adjust the location

		f = 1 - self.radius
		ddf_x = 1
		ddf_y = -2 * self.radius
		x = 0
		y = self.radius
		dFrame.setPixel(Core.Point(x0, y0 + self.radius), colour,merge = True)
		dFrame.setPixel(Core.Point(x0, y0 - self.radius), colour,merge = True)
		dFrame.setPixel(Core.Point(x0 + self.radius, y0), colour,merge = True)
		dFrame.setPixel(Core.Point(x0 - self.radius, y0), colour,merge = True)
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			dFrame.setPixel(Core.Point(x0 + x, y0 + y), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 - x, y0 + y), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 + x, y0 - y), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 - x, y0 - y), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 + y, y0 + x), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 - y, y0 + x), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 + y, y0 - x), colour,merge = True)
			dFrame.setPixel(Core.Point(x0 - y, y0 - x), colour,merge = True)
		return dFrame