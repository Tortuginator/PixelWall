import sys
import random
import math
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame,Drawing,AnimationInstance
from PIL import Image, ImageDraw, ImageFilter

class Clock(AnimationInstance):
    def _Render(self):
        """
        Displays the current Systemtime as a Clock on the screen using circular clockwise gradients.
        args:
            -Colors:
                -ColorHours The Color of the Hour pointer
                -ColorMinutes The color of the minutes pointer
                -ColorSeconds The color of the seconds pointer
            -Radi:
                -HoursRad The Additional radius of the Hours circle
                -SecondsRad ""
                -MinutesRad ""
            -Interpolate Interpolates the minutes and hour pointers, so that they don't do a sudden movement
            -CenterPosition The Center of the Clock aka. Circles
        """
        ColorSeconds = (0,0,200)
        ColorMinutes = (0,200,0)
        ColorHours = (200,0,0)
        CenterPosition = None
        HoursRad = 10
        MinutesRad = 10
        SecondsRad = 10
        Interpolate = True

        if "ColorHours" in self.args:
            assert type(self.args["ColorHours"]) == tuple,"The ColorHours value needs to be a tuple"
            assert len(self.args["ColorHours"]) == 3,"The ColorHours value needs to of length 3"
            ColorHours = argumetns["ColorHours"]

        if "ColorMinutes" in argumets:
            assert type(self.args["ColorMinutes"]) == tuple,"The ColorMinutes value needs to be a tuple"
            assert len(self.args["ColorMinutes"]) == 3,"The ColorMinutes value needs to of length 3"
            ColorMinutes = self.args["ColorMinuts"]

        if "ColorSeconds" in self.args:
            assert type(self.args["ColorSeconds"]) == tuple,"The ColorSeconds value needs to be a tuple"
            assert len(self.args["ColorSeconds"]) == 3,"The ColorSeconds value needs to of length 3"
            ColorSeconds = self.args["ColorSeconds"]

        if "Interpoate" in self.args:
            assert type(self.args["interpolate"]) == bool,"The Interpolate value needs to be of type boolean"
            Interpoate = self.args["Interpolate"]

        if "CenterPosition" in self.args:
            assert type(self.args["CenterPosition"]) == tuple,"CenterPosition must be a tuple"
            assert len(self.args["CenterPosition"]) == 2,"CenterPosition must be of length 2"
            CenterPosition = self.args["CenterPosition"]

        if "SecondsRad" in self.args:
            SecondsRad = int(self.args["SecondsRad"])

        if "MinutesRad" in self.args:
            MinutesRad = int(self.args["MinutesRad"])

        if "HoursRad" in self.args:
            HoursRad = int(self.args["HoursRad"])

        assert CenterPosition is not None, "CenterPosition variable must be set and can not be empty"
        assert SecondsRad > 0,"The SecondsRad value needs to be greater than 0"
        assert SecondsRad < MinutesRad < HoursRad,"The Radi of the different units: Hours,Minutes,Seconds are not in the correct 'Smaller than' order"

        locTime = time.localtime(time.time())
        if Interpoate is True:
            seconds = locTime[5]*float(360/60)
            minutes = locTime[4]*float(360/60)+((1/float(60))*locTime[5])*float(360/60)
            hours = (locTime[3]%12)*float(360/12) + (1/float(60))*(locTime[4])*float(360/12)
        else:
            seconds = locTime[5]*float(360/60)
            minutes = locTime[4]*float(360/60)
            hours = (locTime[3]%12)*float(360/12)

        assert 0 <= seconds <= 360,"seconds do not match 360 pattern"
        assert 0 <= minutes <= 360,"minutes do not match 360 pattern"
        assert 0 <= hours <= 360,"hours do not match 360 pattern"

        Drawing.RadialCircle(self.dFrame.img, HoursRad+MinutesRad+SecondsRad, CenterPosition, ColorHours, 1.0, 0.0, OffDegrees = hours, CircleCutoff = SecondsRad + MinutesRad-1, invert = True)
        Drawing.RadialCircle(self.dFrame.img, MinutesRad+SecondsRad, CenterPosition, ColorMinuts, 1.0, 0.0, OffDegrees = minutes, CircleCutoff = SecondsRad-1, invert = True)
        Drawing.RadialCircle(self.dFrame.img, SecondsRad, CenterPosition, ColorSeconds, 1.0, 0.0, OffDegrees = seconds, invert = True)
