import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter
"""EXAMPLE PATTERNS:
Pulsator-->  [[1,1,1,1,1,1,1,1],[1,0,1,1,1,1,0,1],[1,1,1,1,1,1,1,1]]
MegaPattern ->[[1,1,1],[1,0,1],[1,0,1],[0,0,0],[1,0,1],[1,0,1],[1,1,1]]
r-Pentomino --> [[0,1,1],[1,1,0],[0,1,0]]
"""


class GameOfLife(PresetAnimations.AnimationInstance):
    def extendedInit(self):
        self.color = (255,255,255)
        if "color" in self.args:
            self.color = self.args["color"]
        self.pattern = [[0,0,0],[0,1,0],[0,0,0]]
        if "pattern" in self.args:
            self.pattern = self.args["pattern"]
        self.position = (0,0)
        if "position" in self.args:
            self.position = self.args["position"]
        self.rules = GameOfLife.Rules
        if "rules" in self.args:
            self.rules = self.args["rules"]
        self.counter = 0
		
    def setPrevframe(self,prevframe):
        self.prevframe = prevframe

    def Render(self):
        if self.counter == 0:
            for r in range(0,len(self.pattern)):
                for i in range(0,len(self.pattern[r])):
                    if self.pattern[r][i] == 1:
                        self.dFrame.pixel[self.position[0]+i,self.position[1]+r] = self.color
            self.counter +=1
            self.prevframe = self.dFrame
            return

        width,height = self.dFrame.img.size
        for i in range(0,width):
            for r in range(0,height):
                input = [[0,0,0],[0,0,0],[0,0,0]]
                if  i-1 >= 0 and r-1 >= 0:input[0][0] = self.colorToLive(self.prevframe.pixel[i-1,r-1])
                if  i-1 >= 0:input[1][0] = self.colorToLive(self.prevframe.pixel[i-1,r])
                if  i-1 >= 0 and r+1 < height:input[2][0] = self.colorToLive(self.prevframe.pixel[i-1,r+1])

                if  r-1 >= 0:input[0][1] = self.colorToLive(self.prevframe.pixel[i,r-1])
                alive = self.colorToLive(self.prevframe.pixel[i,r])
                input[1][1] = 0
                if  r+1 < height:input[2][1] = self.colorToLive(self.prevframe.pixel[i,r+1])

                if  i+1 < width and r-1 >= 0:input[0][2] = self.colorToLive(self.prevframe.pixel[i+1,r-1])
                if  i+1 < width:input[1][2] = self.colorToLive(self.prevframe.pixel[i+1,r])
                if  i+1 < width and r+1 < height:input[2][2] = self.colorToLive(self.prevframe.pixel[i+1,r+1])

                if self.rules(input,alive) == 1:
                    self.dFrame.pixel[i,r] = self.color
        self.prevframe = self.dFrame
        self.counter +=1

    def colorToLive(self,color):
        #print color
        if color == self.color or color == tuple(list(self.color)+[255]):
            return 1
        else:
            return 0
    @staticmethod
    def Rules(input,isalive):
        count = GameOfLife.countlivingCells(input)
        if count == 2 and isalive == 1:
            return 1#LIVE
        elif count == 3:
            return 1#LIVE
        return 0
    @staticmethod
    def countlivingCells(input):
        c = 0
        for r in input:
            for i in r:
                if i == 1 or i == 255:
                    c+=1
        return c
