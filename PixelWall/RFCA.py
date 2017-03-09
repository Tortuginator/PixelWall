#RelativeFrameCompressionAlgorithm
class RFCA():
    def __init__(self,LOD = 0):
        self.levelOfDetail(LOD);
        self.frame = None
        self.last = None
        self.LOD = 0
        self.counter = -1

    def getByteCode(self):
        #Type,SubframeType,Framenumber
        initSeq = [3,0,self.counter%255,len(self.last[0])//255,len(self.last[0])%255,len(self.last[1])//255,len(self.last[1])%255,len(self.last[2])//255,len(self.last[2])%255]
        return initSeq + self.last[0] + self.last[1] + self.last[2]
        return bytearray(initSeq) + bytearray(self.last[0]) + bytearray(self.last[1]) + bytearray(self.last[2])

    def levelOfDetail(self,LOD):
        if LOD < 0 and LOD > 10:
            self.LOD = 0
            return 0
        self.LOD = LOD

    def addFrame2(self,newFrame):
        difference = [[],[],[]]
        if self.initNewFrame() is True:
            return

        for channel in range(0,len(self.frame)):
            for p in range(0,len(self.frame[channel])):
                lastP = -1
                if abs(self.__allowedSymbol(newFrame[channel][p]) - self.frame[channel][p]) <= self.LOD:
                    #no difference
                    pass
                else:
                    if lastP == p-1:
                        difference[channel].append(self.__allowedSymbol(newFrame[channel][p]))
                        lastP = p
                    else:
                        skipped = p - (lastP+1)
                        if skipped <= 2:
                            for r in range(lastP+1,p):
                                difference[channel].append(self.__allowedSymbol(newFrame[channel][r]))
                        else if skipped > 255:
                            for r in range(0,skipped//255):
                                difference[channel].append(1)
                                difference[channel].append(255)
                            difference[channel].append(1)
                            difference[channel].append(skipped%255)
                        else:
                            difference[channel].append(1)
                            difference[channel].append(skipped)
                        difference[channel].append(self.__allowedSymbol(newFrame[channel][p]))
        self.frame = newFrame
        self.counter +=1
        self.last = compact
    def initNewFrame(self,newFrame):
        if self.frame == None:
            self.frame = [[],[],[]]
            for channel in range(0,len(newFrame)):
                for p in range(0,len(newFrame[channel])):
                    self.frame[channel].append(self.__allowedSymbol(newFrame[channel][p]))
            self.last = self.frame
            self.counter = 1
            self.frame = newFrame
            return True
        else:
            return False

    def addFrame(self,newFrame):
        difference = [[],[],[]]
        difference[0] = [(-1) for i in range(0,len(newFrame[0]))]
        difference[1] = [(-1) for i in range(0,len(newFrame[0]))]
        difference[2] = [(-1) for i in range(0,len(newFrame[0]))]
        if self.frame == None:
            self.frame = [[],[],[]]
            for channel in range(0,len(newFrame)):
                for p in range(0,len(newFrame[channel])):
                    self.frame[channel].append(self.__allowedSymbol(newFrame[channel][p]))
            self.last = self.frame
            self.counter = 1
            self.frame = newFrame
            return
        for channel in range(0,len(self.frame)):
            for p in range(0,len(self.frame[channel])):
                if abs(newFrame[channel][p] - self.frame[channel][p]) <= self.LOD:
                    difference[channel][p] = -1
                else:
                    difference[channel][p] = newFrame[channel][p]
        #Remove the unused differences from the frames
        compact = [[],[],[]]
        skipped = 0
        for channel in range(0,len(difference)):
            for p in range(0,len(difference[channel])):
                if difference[channel][p] == -1:
                    skipped +=1
                else:
                    if skipped == 0:
                        compact[channel].append(self.__allowedSymbol(difference[channel][p]))
                    elif skipped <= 3:
                        for i in range(0,skipped+1):
                            compact[channel].append(self.__allowedSymbol(newFrame[channel][p-1-skipped+i]))
                        compact[channel].append(self.__allowedSymbol(difference[channel][p]))
                    else:
                        for r in range(0,(skipped-3)//255):
                            compact[channel].append(1)
                            compact[channel].append(255)
                        compact[channel].append(1)
                        compact[channel].append((skipped-3)%255)
                        compact[channel].append(self.__allowedSymbol(difference[channel][p]))
                        skipped = 0
            for r in range(0,(skipped-3)//255):
                compact[channel].append(1)
                compact[channel].append(255)
            compact[channel].append(1)
            compact[channel].append((skipped-3)%255)
            skipped = 0
        #Compression
        self.frame = newFrame
        self.counter +=1
        self.last = compact

    @staticmethod
    def __allowedSymbol(i):
        if i == 1:
            return 2
        if i == 3:
            return 4
        return i
