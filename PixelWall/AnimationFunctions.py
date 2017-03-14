import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame
from PIL import Image,ImageDraw
def Circle2(AnimationInstance,iteration,opacity,dFrame):
    """
    Draws A Circle
    -The circle has a inner fade

    Parameters:
    -Color: [COLOR] The border Color
    -ColorGRAD: [COLOR] The color at the end of the inner fade
    -Length: length of the inner fade to ColorGRAD
    -Radius: [INT] The maximal circle radius
    """

    Color = (50,100,200)
    ColorGRAD = (255,0,0)
    Length = 5
    position = (14,14)
    iteration = float(iteration)*0.2
    #else
    Cindex = int(iteration)
    baseColor = [Color[0]-ColorGRAD[0],Color[1]-ColorGRAD[1],Color[2]-ColorGRAD[2]]


    for p in range(Cindex+1,0,-1):
        CurrentRadius = p;MaxRadius = Cindex;FadeIn = Length;

        if MaxRadius-FadeIn <= CurrentRadius:
            divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
        else:
            divRelation = 0

        if p > Cindex:
            divRad = Cindex
        else:
            divRad = p
        divColor = (int(divRelation*baseColor[0] + ColorGRAD[0]),int(divRelation*baseColor[1] + ColorGRAD[1]),int(divRelation*baseColor[2] + ColorGRAD[2]),255)
        dFrame.imgdraw.ellipse([(position[0]-CurrentRadius,position[1]-CurrentRadius),(position[0]+CurrentRadius,position[1]+CurrentRadius)],fill = divColor)

