import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class Matrix(PresetAnimations.AnimationInstance):
    def extendedInit(self):
        self.matrix = []

    def Render(self):
        """
        Shows the "typical hacker matrix". Basically Green Lines Vertically running down the screen, while fading out at the end
        arguments:
            -Color sets the color of the matrixeffect
            -Length sets the length of the stripes
        """
        length = 10
        Color = (0, 200, 0)

        if "Length" in self.args:
            assert int(self.args["Length"]) > 0,"Length must be greater than 0"
            length = int(self.args["Length"])

        if "Color" in self.args:
            assert type(self.args["Color"]) is tuple, "Color needs to be type of tuple"
            assert len(self.args["Color"]) == 3, "Color needs to be of length 3"
            Color = self.args["Color"]

        while len(self.matrix) < self.dFrame.img.size[0]: #width
            self.matrix.append(random.randint(0, self.dFrame.img.size[1]-1))

        for i in range(0, len(self.matrix)):
            tmpl = self.matrix[i] - length;
            if tmpl <= 0:
                tmpl = 0
            while tmpl < self.matrix[i]:
                tc = float(1/float(length))*(self.matrix[i]-tmpl)
                self.dFrame.imgdraw.point((i, tmpl),(Color[0], int(Color[1]*(1-tc)), Color[2]))
                tmpl +=1
            self.matrix[i] +=1;
            if self.matrix[i] > (self.dFrame.img.size[1]+length+random.randint(0, 5)): #height
                self.matrix[i] = 0
