import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing

from PIL import Image, ImageDraw, ImageFilter

class Teleport(AnimationInstance):
    def extendedInit(self):
        self.positons = []

    def Render(self):
        number = 10
        width = self.dFrame.size[0]
        height = self.dFrame.size[1]

        while len(self.positions) < number:
            ###[startpositionX,startpositionY,endpositionX,endpositionY,size,speed,colorA,colorB,position]
            self.positions.append([self.random,0])
