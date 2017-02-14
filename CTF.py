#CompactTransportFormat
class CompactTransportFormat():
    def __init__(self):
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
            return 0
        self.LOD = LOD

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
                            compact[channel].append(self.__allowedSymbol(newframe[channel][p-1-skipped+i]))
                        compact[channel].append(self.__allowedSymbol(difference[channel][p]))
                    else:
                        compact[channel].append(1)
                        compact[channel].append(skipped-3)
                        compact[channel].append(self.__allowedSymbol(difference[channel][p]))

                        skipped = 0
            compact[channel].append(1)
            compact[channel].append(skipped-3)
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


if __name__ == "__main__":
    testCTF = CompactTransportFormat();
    testCTF.addFrame([[0,5,2,226,224,165,1,1,1,1,5,4],[0,5,2,226,224,165,1,1,1,1,5,4],[0,5,2,226,224,165,1,1,1,1,5,4]])
    print testCTF.getByteCode()
    testCTF.addFrame([[0,5,2,226,224,165,1,1,1,1,5,4],[0,5,2,226,224,165,1,1,1,1,5,4],[0,5,2,226,224,165,1,1,1,1,5,4]])
    print testCTF.getByteCode()
