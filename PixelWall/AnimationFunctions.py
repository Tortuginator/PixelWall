import sys
sys.path.append('.\PixelWall')
from PixelWall import Core,RenderObjects,Frame

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

    Color = (100,200,100)
    ColorGRAD = (0,255,0)
    Length = 5
    position = Core.Point(15,15)

    #else
    Cindex = int(iteration)
    baseColor = [Color[0]-ColorGRAD[0],Color[1]-ColorGRAD[1],Color[2]-ColorGRAD[2]]

    for p in range(0,Cindex+1):
        CurrentRadius = p;MaxRadius = Cindex;FadeIn = Length;

        if MaxRadius-FadeIn <= CurrentRadius:
            divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
        else:
            divRelation = 0

        if p > Cindex:
            divRad = Cindex
        else:
            divRad = p
        divColor = (divRelation*Color[0] + ColorGRAD[0],divRelation*Color[1] + ColorGRAD[1],divRelation*Color[2] + ColorGRAD[2])
        #def __init__(self,centerPoint,color,radius,fill = False,fillcolor = 0,opacity = 1):
        dFrame.addObject(RenderObjects.Circle.Circle(position,divColor,divRad,opacity = opacity))
