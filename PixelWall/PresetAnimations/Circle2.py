import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing,AnimationInstance
from PIL import Image, ImageDraw, ImageFilter

class Circle2(AnimationInstance):
    def _Render(self):
        """
        Draws A Circle
        -The circle has a inner fade

        Parameters:
        -Color: [COLOR] The border Color
        -ColorGRAD: [COLOR] The color at the end of the inner fade
        -Length: [INT] length of the inner fade from Color to ColorGRAD
        -Radius: [INT] The maximal circle radius
        -Speed: [FLOAT] the speedadjustment. Normal 0.2
        """
        ##Default self.dFrame
        Color = (50, 100, 200)
        ColorGRAD = (255, 0, 0)
        Length = 10
        position = (14, 14)
        Speed = 0.2
        #Set self.dFrame
        if "ColorFill" in self.args:
            ColorGRAD = self.args["ColorFill"]
        if "ColorBorder" in self.args:
            Color = self.args["ColorBorder"]
        if "Position" in self.args:
            position = self.args["position"]
        if "Length" in self.args:
            Length = self.args["Length"]
        if "Speed" in self.args:
            Speed = self.args["Speed"]


        iteration = float(self.iteration)*Speed
        #else
        Cindex = int(iteration)
        baseColor = [Color[0]-ColorGRAD[0], Color[1]-ColorGRAD[1], Color[2]-ColorGRAD[2]]


        for p in range(Cindex+1, 0, -1):
            CurrentRadius = p;MaxRadius = Cindex;FadeIn = Length;

            if MaxRadius-FadeIn <= CurrentRadius:
                divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
            else:
                divRelation = 0

            if p > Cindex:
                divRad = Cindex
            else:
                divRad = p
            divColor = (int(divRelation*baseColor[0] + ColorGRAD[0]), int(divRelation*baseColor[1] + ColorGRAD[1]), int(divRelation*baseColor[2] + ColorGRAD[2]), 255)
            self.dFrame.imgdraw.ellipse([(position[0]-CurrentRadius, position[1]-CurrentRadius), (position[0]+CurrentRadius,position[1]+CurrentRadius)], fill = divColor)
