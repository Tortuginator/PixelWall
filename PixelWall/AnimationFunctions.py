import sys
import random
sys.path.append('.\PixelWall')
from PixelWall import Core,Frame
from PIL import Image,ImageDraw,ImageFilter

ChillStorage = []
MatrixStorage = []
GifStorage = None
global GifStorage

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
    Length = 10
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

def Chill(AnimationInstance,iteration,opacity,dFrame):
    COSwave = [0,0,0,0,1,1,1,2,2,3,4,5,6,6,8,9,10,11,12,14,15,17,18,20,22,23,25,27,29,31,33,35,38,40,42,45,47,49,52,54,57,60,62,65,68,71,73,76,79,82,85,88,91,94,97,100,103,106,109,113,116,119,122,125,128,131,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177,180,183,186,189,191,194,197,199,202,204,207,209,212,214,216,218,221,223,225,227,229,231,232,234,236,238,239,241,242,243,245,246,247,248,249,250,251,252,252,253,253,254,254,255,255,255,255,255,255,255,255,254,254,253,253,252,252,251,250,249,248,247,246,245,243,242,241,239,238,236,234,232,231,229,227,225,223,221,218,216,214,212,209,207,204,202,199,197,194,191,189,186,183,180,177,174,171,168,165,162,159,156,153,150,147,144,141,138,135,131,128,125,122,119,116,113,109,106,103,100,97,94,91,88,85,82,79,76,73,71,68,65,62,60,57,54,52,49,47,45,42,40,38,35,33,31,29,27,25,23,22,20,18,17,15,14,12,11,10,9,8,6,6,5,4,3,2,2,1,1,1,0,0,0,0];
    Drops = 80;
    #img = Image.new("RGBA",(28,28),(0,0,0,0));
    #imgdraw = ImageDraw.Draw(img)
    while (len(ChillStorage) < Drops):
        #X,Y,Color(R,G,B),speed,pos
        ChillStorage.append([random.randint(0,27),random.randint(0,27),(random.randint(0,50),random.randint(100,255),random.randint(50,255)),random.randint(1,5),0])
    col = []
    for i in range(0,len(ChillStorage)):
        if ChillStorage[i][4] > 255:
            ChillStorage[i][4] = 255
        r = int(ChillStorage[i][2][0]*(float(COSwave[ChillStorage[i][4]])/255))
        g = int(ChillStorage[i][2][1]*(float(COSwave[ChillStorage[i][4]])/255))
        b = int(ChillStorage[i][2][2]*(float(COSwave[ChillStorage[i][4]])/255))
        divColor = (r,g,b,255)
        dFrame.imgdraw.point([ChillStorage[i][0],ChillStorage[i][1]],divColor)
        ChillStorage[i][4] += ChillStorage[i][3]
        if ChillStorage[i][4] >= 255:
            col.append(i)

    for r in range(0,len(col)):
        del ChillStorage[col[r]];

    dFrame.img = dFrame.img.filter(ImageFilter.GaussianBlur(radius = 5))
    dFrame.img = dFrame.img.filter(ImageFilter.SMOOTH_MORE)
    #dFrame.img = dFrame.img.filter(ImageFilter.BLUR)

def Matrix(AnimationInstance,iteration,opacity,dFrame):
    length = 10
    while len(MatrixStorage) < dFrame.img.size[0]: #width
        MatrixStorage.append(random.randint(0,dFrame.img.size[1]-1))

    for i in range(0,len(MatrixStorage)):
        tmpl = MatrixStorage[i] - length;
        if tmpl <= 0:
            tmpl = 0
        while tmpl < MatrixStorage[i]:
            tc = float(1/float(length))*(MatrixStorage[i]-tmpl)
            dFrame.imgdraw.point((i,tmpl),(0,int(200*(1-tc)),0))
            tmpl +=1
        MatrixStorage[i] +=1;
        if MatrixStorage[i] > (dFrame.img.size[1]+length+random.randint(0,5)): #height
            MatrixStorage[i] = 0

def GIF(AnimationInstance,iteration,opacity,dFrame):
    global GifStorage
    filename = "GIF\Fog.gif"
    position = (-2,-2)
    if GifStorage == None:
        GifStorage = Image.open(filename)
    try:
        dFrame.img.paste(GifStorage,position)
        GifStorage.seek(GifStorage.tell() + 1)
    except Exception,e:
        GifStorage.seek(0)
