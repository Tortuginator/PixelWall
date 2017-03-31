import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing,PresetAnimations
from PIL import Image, ImageDraw, ImageFilter

class GIF(PresetAnimations.AnimationInstance):
    def extendedInit(self):
        self.file = None

    def Render(self):
        """
        Renders a GIF animation Frame by Frame. In case, the GIF animations "look weird" make sure that they dont use "transparent" layers or colors.
        self.args:
            -File the filename of the giffile
            -Position the top-left corner's position
        """

        filename = None
        position = None

        if "File" in self.args:
            filename = self.args["File"]

        if "Position" in self.args:
            assert type(self.args["Position"]) == tuple,"The position value needs to have the type tuple"
            assert len(self.args["Position"]) == 2,"The position value needs to have the length 2"
            position = self.args["Position"]

        assert filename != None,"The filename value needs to be set"
        assert position != None,"The position value needs to be set"
        if self.file == None:
            self.file = Image.open(filename)
        try:
            self.dFrame.img.paste(self.file, position)
            self.file.seek(self.file.tell() + 1)
        except Exception,e:
            self.file.seek(0)
