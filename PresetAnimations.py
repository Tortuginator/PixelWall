import PixelWall as PW
import math,random
class Presets():
    @staticmethod
    def Rectangle1(dFrame,CurrentIndex,Iteration,Storage,Parameters):
        """
        Draws a moving Rectangle
        Parameters:
        -Length: [INT] the length of the fade
        -Xsize: [INT] width of the Rectangle
        -Ysize: [INT] hieght of the Rectangle
        -Xstart: [INT] the start X coordinate
        -Ystart: [INT] the start Y coordinate
        -Xtarget: [INT] the X coordinate of the target
        -Ytarget: [INT] the Y coordinate of the target
        -Color: [COLOR] the Rectangle colors
        -FadeColorEnd: [COLOR] the Color at the end of the Fade
        -FadeColorStart: [COLOR] the Color at the beginning of the Fade
        """

    @staticmethod
    def Test(dFrame,CurrentIndex,Iteration,Storage,Parameters):
        """
        Draws a Testpattern to check if all colors and pixels are displayed corretly and the correct screensize was detected
        -has no parameters
        -runs as infinite loop
        """
        status = PW.AnimationStates.inProgress
        if CurrentIndex <= 5:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,p*2,p*2,(255,0,0))
        elif CurrentIndex <= 10:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,p*2,p*2,(0,255,0))
        elif CurrentIndex <= 15:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,p*2,p*2,(0,0,255))
        elif CurrentIndex <= 20:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,(p*2)+1,(p*2)+1,(255,0,0))
        elif CurrentIndex <= 25:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,(p*2)+1,(p*2)+1,(0,255,0))
        elif CurrentIndex <= 30:
            for p in range(0,(dFrame.height//2)+1):
                dFrame.drawRectangle(0,dFrame.width-1,(p*2)+1,(p*2)+1,(0,0,255))
        elif CurrentIndex <= 60:
            CurrentIndex =CurrentIndex-30
            dFrame.drawRectangle(0,CurrentIndex,0,dFrame.height-1,(255,255,255))
        elif CurrentIndex <=80:
            CurrentIndex =CurrentIndex-60
            dFrame.drawRectangle(0,dFrame.width,0,dFrame.height,((255/20)*CurrentIndex,(255/20)*CurrentIndex,(255/20)*CurrentIndex))
        elif CurrentIndex <=90:
            dFrame.setPixel(0,0,(255,255,255))
            dFrame.setPixel(0,dFrame.height-1,(255,255,255))
            dFrame.setPixel(dFrame.width-1,dFrame.height-1,(255,255,255))
            dFrame.setPixel(dFrame.width-1,0,(255,255,255))

        return (dFrame,status,Storage)

    @staticmethod
    def Circle1(dFrame,CurrentIndex,Iteration,Storage,Parameters):
        """
        Draws A Circle
        -The circle has a inner fade

        Parameters:
        -Color: [COLOR] The border Color
        -ColorGRAD: [COLOR] The color at the end of the inner fade
        -Length: length of the inner fade to ColorGRAD
        -Radius: [INT] The maximal circle radius
        """
        status = PW.AnimationStates.inProgress
        Cindex = CurrentIndex
        baseColor = [Parameters["Color"][0] - Parameters["ColorGRAD"][0],Parameters["Color"][1] - Parameters["ColorGRAD"][1],Parameters["Color"][2] - Parameters["ColorGRAD"][2]]

        for p in range(0,Cindex+1):
            CurrentRadius = p;MaxRadius = Cindex;FadeIn = Parameters["Length"];

            if MaxRadius-FadeIn <= CurrentRadius:
                divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
            else:
                divRelation = 0

            if p > Cindex:
                divRad = Cindex
            else:
                divRad = p
            divColor = (divRelation*baseColor[0] + Parameters["ColorGRAD"][0],divRelation*baseColor[1] + Parameters["ColorGRAD"][1],divRelation*baseColor[2] + Parameters["ColorGRAD"][2])
            dFrame.drawCircle(Parameters["X"],Parameters["Y"],divRad,divColor)
        return (dFrame,status,None)

    @staticmethod
    def Circle2(dFrame,CurrentIndex,Iteration,Storage,Parameters):
        """

        Draws A Circle
        -The circle fades it Opacity to 0 linear to the total_radius
        -The circle has a inner fade

        Parameters:
        -FadeOut: [INT] Radius+1, when the circle has opacity 0
        -Color: [COLOR] The border Color
        -ColorGRAD: [COLOR] The color at the end of the inner fade
        -Length:[INT] length of the inner fade to ColorGRAD
        -Radius: [INT] maximal radius of the circle
        """
        status = PW.AnimationStates.inProgress
        Cindex = CurrentIndex
        baseColor = [Parameters["Color"][0] - Parameters["ColorGRAD"][0],Parameters["Color"][1] - Parameters["ColorGRAD"][1],Parameters["Color"][2] - Parameters["ColorGRAD"][2]]
        divOpacity = float(Parameters["FadeOut"]-CurrentIndex+1)/float(Parameters["FadeOut"])
        if divOpacity > 1:divOpacity =1;
        for p in range(0,Cindex+1):
            CurrentRadius = p;MaxRadius = Cindex;FadeIn = Parameters["Length"];

            if MaxRadius-FadeIn <= CurrentRadius:
                divRelation = float(CurrentRadius-MaxRadius+FadeIn)/float(FadeIn)
            else:
                divRelation = 0

            if p > Cindex:
                divRad = Cindex
            else:
                divRad = p
            divColor = (divRelation*baseColor[0] + Parameters["ColorGRAD"][0],divRelation*baseColor[1] + Parameters["ColorGRAD"][1],divRelation*baseColor[2] + Parameters["ColorGRAD"][2])
            divColor = (int(divColor[0]*divOpacity),int(divColor[1]*divOpacity),int(divColor[2]*divOpacity))
            dFrame.drawCircle(Parameters["X"],Parameters["Y"],divRad,divColor)
        return (dFrame,status,None)

    @staticmethod
    def Pattern1(dFrame,Cindex,Iteration,Storage,Parameters):
        """
        Draws a random pattern of pixels using the COS Function
        The pixels have no relation to each other
        Parameters:
        -ColorA: [COLOR] The mimimum color
        -COlorB: [COLOR] The maxiumum color
        """
        status = PW.AnimationStates.inProgress
        if Storage is None:
            Storage = []
            tmLength = dFrame.width*dFrame.height
            for p in range(0,tmLength+1):
                Storage.append(random.randint(0,255))

        tmLength = dFrame.height*dFrame.width
        for p in range(0,tmLength+1):
            x0 = p%dFrame.width
            y0 = p//dFrame.width
            c0r = (Parameters["ColorA"][0] - Parameters["ColorB"][0])*(-1)
            c0g = (Parameters["ColorA"][1] - Parameters["ColorB"][1])*(-1)
            c0b = (Parameters["ColorA"][2] - Parameters["ColorB"][2])*(-1)
            p0 = math.cos(Storage[p]*float(Cindex*0.0001))
            if p0 < 0:p0 = p0*(-1)
            c0 = (int(Parameters["ColorA"][0] + c0r*p0),int(Parameters["ColorA"][1] + c0g*p0),int(Parameters["ColorA"][2] + c0b*p0))
            dFrame.setPixel(x0,y0,c0)
        return (dFrame,status,Storage)
