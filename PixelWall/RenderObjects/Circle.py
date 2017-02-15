from __init__ import FrameFunction

class Circle(FrameFunction):
	def __init__(self,centerPoint,color,radius,fill = False,fillcolor = 0,opacity = 1):
		self.centerPoint = centerPoint
		self.color = color
		self.radius = radius
		self.fill = fill
		self.fillcolor = fillcolor
		self.opacity = opacity

	def Render(self,dFrame):
		x0 = self.centerPoint[0]
		y0 = self.centerPoint[1]
		if dFrame.isColor(self.color) is False:return 0;
		colour = Frame.isColor(self.color);
		#if Frame.isColor(fillColor) is False:return 0;
		if self.radius <= 0:	return 0;

		#Adjust the location

		f = 1 - self.radius
		ddf_x = 1
		ddf_y = -2 * self.radius
		x = 0
		y = self.radius
		self.setPixel((x0, y0 + self.radius), colour,merge = True,ignore = True)
		self.setPixel((x0, y0 - self.radius), colour,merge = True,ignore = True)
		self.setPixel((x0 + self.radius, y0), colour,merge = True,ignore = True)
		self.setPixel((x0 - self.radius, y0), colour,merge = True,ignore = True)
		while x < y:
			if f >= 0:
				y -= 1
				ddf_y += 2
				f += ddf_y
			x += 1
			ddf_x += 2
			f += ddf_x
			self.setPixel((x0 + x, y0 + y), colour,merge = True,ignore = True)
			self.setPixel((x0 - x, y0 + y), colour,merge = True,ignore = True)
			self.setPixel((x0 + x, y0 - y), colour,merge = True,ignore = True)
			self.setPixel((x0 - x, y0 - y), colour,merge = True,ignore = True)
			self.setPixel((x0 + y, y0 + x), colour,merge = True,ignore = True)
			self.setPixel((x0 - y, y0 + x), colour,merge = True,ignore = True)
			self.setPixel((x0 + y, y0 - x), colour,merge = True,ignore = True)
			self.setPixel((x0 - y, y0 - x), colour,merge = True,ignore = True)

	def Object(self):
		return (self,centerPoint,color,radius)
