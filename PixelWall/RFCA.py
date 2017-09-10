#RelativeFrameCompressionAlgorithm
class RFCA():
    def __init__(self):
        self.frame = None
        self.last = None
        self.counter = -1

    def getByteCode(self):
        #Type,SubframeType,Framenumber
        initSeq = [len(self.last[0])//255, len(self.last[0])%255, len(self.last[1])//255, len(self.last[1])%255, len(self.last[2])//255, len(self.last[2])%255]
        #return initSeq + self.last[0] + self.last[1] + self.last[2]
        return bytearray(initSeq) + bytearray(self.last[0]) + bytearray(self.last[1]) + bytearray(self.last[2])

    @staticmethod
    def __FrameDiff(BaseFrame,SecondFrame):
        return [RFCA.__ChannelDiff(BaseFrame[0],SecondFrame[0]),RFCA.__ChannelDiff(BaseFrame[1],SecondFrame[1]),RFCA.__ChannelDiff(BaseFrame[2],SecondFrame[2])]
    @staticmethod
    def __ChannelDiff(BaseChannel,SecondChannel):
        #under the assumption, that booth Channels have the same configuration
        assert len(BaseChannel) == len(SecondChannel),"Booth Channels don't have the same length"
        difference = []
        for i in range(0,len(BaseChannel)):
            difference.append(SecondChannel[i] - BaseChannel[i]);
        return difference

    @staticmethod
    def __skipSequence(counter):
        result = []
        if counter > 255:
            for r in range(0, counter//255):result +=[1,255];
        result.append(1)
        result.append(counter%255)
        return result

    @staticmethod
    def __recoverShortSkips(BaseFrame,SecondFrame,length,channel,index):
        assert len(SecondFrame[0]) >= length,"Frame in wrong format"
        assert length <= index, "Wrong Length or index parameter"
        assert 0 <= channel < 3,"wrong channel parameter"

        result = []
        for i in range(index - length,index):
            result.append(RFCA.__allowedSymbol(SecondFrame[channel][i]));
        return result

    @staticmethod
    def computeSequences(BaseFrame,SecondFrame):
        result = [[],[],[]]
        difference = RFCA.__FrameDiff(BaseFrame,SecondFrame)

        for c in range(0,len(SecondFrame)):
            Skip = 0
            for i in range(0,len(BaseFrame[c])):
                if difference[c][i] == 0:
                    Skip +=1
                elif Skip == 0 and difference[c][i] != 0:
                    result[c].append(RFCA.__allowedSymbol(SecondFrame[c][i]))

                elif Skip > 0 and Skip <= 2:
                    result[c] += RFCA.__recoverShortSkips(BaseFrame = BaseFrame,SecondFrame = SecondFrame,length = Skip,channel = c, index = i)
                    Skip = 0
                    result[c].append(RFCA.__allowedSymbol(SecondFrame[c][i]))

                elif Skip > 2:
                    result[c] += RFCA.__skipSequence(counter = Skip)
                    Skip = 0
                    result[c].append(RFCA.__allowedSymbol(SecondFrame[c][i]))
        return result

    def addFrame(self,newFrame):
        if self.initNewFrame(newFrame) is True:
            return
        self.last =  RFCA.computeSequences(self.frame,newFrame)
        self.counter +=1
        self.frame = newFrame

    def setLastFrame(self,newFrame):
        self.frame = newFrame

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
