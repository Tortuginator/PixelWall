from __init__ import FrameFunction
import Core,Exceptions
class Rectangle(FrameFunction):
	def __init__(self,startPoint,endPoint,color,opacity):
		if not isinstance(startPoint,Core.Point):
			raise Exceptions.unexpectedType(type = "Core.Point",variable ="startPoint")
		if not isinstance(endPoint,Core.Point):
			raise Exceptions.unexpectedType(type = "Core.Point",variable = "endPoint")
		self.color = color
		self.startPoint = startPoint
		self.endPoint = endPoint
		self.opacity = opacity

	def Render(self,dFrame):
		if not Frame.isColor(self.color):return 0;
		Yoffset = self.endPoint.y - self.startPoint.y
		if Yoffset >= 0:
			Yoffset +=1;
		else:
			Yoffset -=1;

		Xoffset = self.endPoint.x - self.startPoint.x
		if Xoffset >=0:
			Xoffset += 1;
		else:
			Xoffset -= 1;

		for p in range(0,Yoffset):
			if not dFrame.isPixel(self.startPoint.x,self.startPoint.y+p):continue;
			Ioffset = dFrame.getOffset(self.startPoint.x,self.startPoint.y+p)
			for i in range(0,Xoffset):
				dFrame.R[Ioffset+i] = int(self.color[0]*self.opacity)
				dFrame.G[Ioffset+i] = int(self.color[1]*self.opacity)
				dFrame.B[Ioffset+i] = int(self.color[2]*self.opacity)

		def Object(self):
			return (self.startPoint,self.endPoint,self.color,self.opacity)
