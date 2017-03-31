import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame
import math
from PIL import Image, ImageDraw, ImageFilter

def RadialCircle(dFrame,CircleRadius,CirclePosition,CircleColor,StartOpacity = 1.0,EndOpacity = 0.0,OffDegrees = 0,offsetGradient = (0,0),CircleCutoff = 0,invert = False):
    def GetAngle(X,Y,cX,cY,MaxRadius,CurrentRadius):
        if CurrentRadius == 0:
            return 0
        relation = MaxRadius/float(CurrentRadius)
        angle = math.degrees(math.atan2(float(Y-cY)*relation, float(cX-X)*relation))
        return angle+90

    def CircularGradientMask(radius,height,width,center,startOpacity = 1,endOpacity = 0,offDeg = 0,cutoff = 0,invert = False):
        assert 0 < startOpacity <= 1,'invalid StartOpacity'
        assert 0 <= endOpacity < 1,'invalid EndOpacity'
        assert endOpacity < startOpacity,'invalid Opacity values'
        assert cutoff < radius,'invalid cutoff/radius combination'

        offDeg = offDeg%360
        baseOpacity = 255*float(endOpacity)
        diffOpacity = (1/float(360))*255*float(startOpacity-endOpacity)
        alpha_mask = Image.new('L', (width,height), 0)
        alpha_ly = alpha_mask.load()
        #alpha_mask_draw = ImageDraw.Draw(alpha_mask)
        transparency = 0
        for h in range(0,height):
            for w in range(0,width):
                factor = 0
                offHeight = 0
                RadDistance = (center[1]-h)**2 + (center[0]-w)**2
                RadDistance = math.sqrt(RadDistance)
                transparency = 0
                if RadDistance <= radius and RadDistance > cutoff:
                    degrees = GetAngle(w,h,center[0],center[1],radius,RadDistance)
                    degrees = (degrees+offDeg)%360
                    if invert:
                        degrees = 360-degrees
                    transparency = diffOpacity*degrees + baseOpacity
                alpha_ly[w,h] = (int(transparency))
        return alpha_mask

    #Normal Function
    CircleImage= Image.new('RGBA', (CircleRadius*2,CircleRadius*2), 0)
    CircleDraw = ImageDraw.Draw(CircleImage)
    CircleDraw.ellipse([(0, 0), (CircleRadius*2,CircleRadius*2)], fill = CircleColor)
    #Draw Mask
    CircleMask = CircularGradientMask(CircleRadius,CircleRadius*2,CircleRadius*2,(CircleRadius+offsetGradient[0],CircleRadius+offsetGradient[1]),StartOpacity,EndOpacity,OffDegrees,cutoff = CircleCutoff,invert = invert)
    #Paste Result
    dFrame.img.paste(CircleImage,box = (CirclePosition[0]-CircleRadius,CirclePosition[1]-CircleRadius),mask = CircleMask)

def SmoothRectangle(dFrame,position,color,height,width):
    assert type(position) == tuple,"position in the wrong format"
    assert len(position) == 2,"position not in the right length"

    assert type(color)== tuple,"color in the wrong format"
    assert len(color) == 3,"color has the length"

    assert type(height) == int  and type(width) == int,"wring height/width format"

    Xpos = int(position[0])
    Ypos = int(position[1])

    Xopacity = float(position[0]) - Xpos
    Yopacity = float(position[1]) - Ypos

    dFrame.imgdraw.rectangle((Xpos+width+1,Ypos,Xpos+width+1,Ypos+height),fill = (color[0],color[1],color[2],int(255*Xopacity)))
    dFrame.imgdraw.rectangle((Xpos,Ypos+height+1,Xpos+width,Ypos+height+1),fill = (color[0],color[1],color[2],int(255*Yopacity)))
    if Xopacity > 0 and Yopacity > 0:
        dFrame.imgdraw.point((Xpos+width+1,Ypos+height+1),(color[0],color[1],color[2],int(((Xopacity+Yopacity)/2)*255)))
    dFrame.imgdraw.rectangle((Xpos,Ypos,Xpos+width,Ypos+height),fill = (color[0],color[1],color[2],255))
