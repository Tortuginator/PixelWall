#RelativeFrameCompressionAlgorithm
class RFCA():
    def __init__(self, LOD = 0):
        self.levelOfDetail(LOD);
        self.frame = None
        self.last = None
        self.LOD = 0
        self.counter = -1

    def getByteCode(self):
        #Type,SubframeType,Framenumber
        initSeq = [len(self.last[0])//255, len(self.last[0])%255, len(self.last[1])//255, len(self.last[1])%255, len(self.last[2])//255, len(self.last[2])%255]
        #return initSeq + self.last[0] + self.last[1] + self.last[2]
        return bytearray(initSeq) + bytearray(self.last[0]) + bytearray(self.last[1]) + bytearray(self.last[2])

    def levelOfDetail(self, LOD):
        if LOD < 0 and LOD > 10:
            self.LOD = 0
            return 0
        self.LOD = LOD

    def addFrame(self, newFrame):
        difference = [[], [], []]
        if self.initNewFrame(newFrame) is True:
            return
        for channel in range(0, len(self.frame)):
            lastPos = -1
            skippedPos = 0
            for p in range(0, len(self.frame[channel])):
                nowPos = p
                if abs(self.__allowedSymbol(newFrame[channel][p]) - self.frame[channel][p]) <= self.LOD:
                    skippedPos +=1
                else:
                    if lastPos == nowPos-1:
                        difference[channel].append(self.__allowedSymbol(newFrame[channel][p]))
                        lastPos = nowPos
                    else:
                        if skippedPos <= 2:
                            for r in range(0, skippedPos):
                                difference[channel].append(self.__allowedSymbol(newFrame[channel][r]))
                        elif skippedPos > 255:
                            for r in range(0, skippedPos//255):
                                difference[channel].append(1)
                                difference[channel].append(255)
                            difference[channel].append(1)
                            difference[channel].append(skippedPos%255)
                        else:
                            difference[channel].append(1)
                            difference[channel].append(skippedPos)
                        difference[channel].append(self.__allowedSymbol(newFrame[channel][p]))
                        skippedPos = 0;
        self.frame = newFrame
        self.counter +=1
        self.last = difference

    def initNewFrame(self, newFrame):
        if self.frame == None:
            self.frame = [[], [], []]
            for channel in range(0, len(newFrame)):
                for p in range(0, len(newFrame[channel])):
                    self.frame[channel].append(self.__allowedSymbol(newFrame[channel][p]))
            self.last = self.frame
            self.counter = 1
            self.frame = newFrame
            return True
        else:
            return False

    @staticmethod
    def __allowedSymbol(i):
        if i == 1:
            return 2
        if i == 3:
            return 4
        return i
