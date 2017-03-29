sys.path.append('.\PixelWall')
from PixelWall import Core,Frame
import math
from PIL import Image, ImageDraw, ImageFilter

@staticmethod
def RadialCircle(dFrame,CircleRadius,CirclePosition,CircleColor,StartOpacity = 1.0,EndOpacity = 0.0,OffDegrees = 0,offsetGradient = (0,0),CircleCutoff = 0):
    def GetAngle(X,Y,cX,cY,MaxRadius,CurrentRadius):
        if CurrentRadius == 0:
            return 0
        relation = MaxRadius/float(CurrentRadius)
        angle = math.degrees(math.atan2(float(Y-cY)*relation, float(cX-X)*relation))
        return angle+90

    def CircularGradientMask(radius,height,width,center,startOpacity = 1,endOpacity = 0,offDeg = 0):
        assert 0 < startOpacity <= 1,'invalid StartOpacity'
        assert 0 <= endOpacity < 1,'invalid EndOpacity'
        assert endOpacity < startOpacity,'invalid Opacity values'

        offDeg = offDeg%360
        baseOpacity = 255*float(endOpacity)
        diffOpacity = (1/float(360))*255*float(startOpacity-endOpacity)
        alpha_mask = Image.new('L', (width,height), 0)
        alpha_mask_draw = ImageDraw.Draw(alpha_mask)
        transparency = 0
        for h in range(0,height):
            for w in range(0,width):
                factor = 0
                offHeight = 0
                RadDistance = (center[1]-h)**2 + (center[0]-w)**2
                RadDistance = math.sqrt(RadDistance)
                transparency = 0
                if RadDistance <= radius:
                    degrees = GetAngle(w,h,center[0],center[1],radius,RadDistance)
                    degrees = (degrees+offDeg)%360
                    transparency = diffOpacity*degrees + baseOpacity
                alpha_mask_draw.point((w,h),(int(transparency)))
        return alpha_mask

    #Normal Function
    CircleImage= Image.new('RGBA', (CircleRadius*2,CircleRadius*2), 0)
    CircleDraw = ImageDraw.Draw(CircleImage)
    CircleDraw.ellipse([(0, 0), (CircleRadius*2,CircleRadius*2)], fill = CircleColor)
    #Draw Mask
    CircleMask = CircularGradientMask(CircleRadius,CircleRadius*2,CircleRadius*2,(CircleRadius+offsetGradient[0],CircleRadius+offsetGradient[1]),StartOpacity,EndOpacity,OffDegrees)
    #Draw OffCircle
    CircleMaskDraw = ImageDraw.Draw(CircleMask)
    CircleDraw.ellipse([(CircleRadius-CircleCutoff, CircleRadius-CircleCutoff), (CircleRadius+CircleCutoff,CircleRadius+CircleCutoff)], fill = (0))
    #Paste Result
    dFrame.paste(CircleImage,box = (CirclePosition[0]-CircleRadius,CirclePosition[1]-CircleRadius),mask = CircleMask)
