#RelativeFrameCompressionAlgorithm
class RFCA():
    def __init__(self):
        self.frame = None
        self.last = None
        self.counter = -1
        self.correctseqential = True # this enables the Algorithm to include a sequence in each frame increasing with each iteration to prevent faulty pixels
        self.sequentiallength = 20
        self.sequentialposition = 0

    def getByteCode(self):
        initSeq = [len(self.last[1])//255, len(self.last[1])%255, len(self.last[2])//255, len(self.last[2])%255, len(self.last[0])//255, len(self.last[0])%255]
        return bytearray(initSeq) + bytearray(self.last[1]) + bytearray(self.last[2]) + bytearray(self.last[0])

    def FrameDiff(self,BaseFrame,SecondFrame):
        return [self.ChannelDiff(BaseFrame[0],SecondFrame[0]),self.ChannelDiff(BaseFrame[1],SecondFrame[1]),self.ChannelDiff(BaseFrame[2],SecondFrame[2])]

    def ChannelDiff(self,BaseChannel,SecondChannel):
        #under the assumption, that booth Channels have the same configuration
        assert len(BaseChannel) == len(SecondChannel),"Booth Channels don't have the same length"
        difference = []
        for i in range(0,len(BaseChannel)):
            difference.append(SecondChannel[i] - BaseChannel[i]);
        return difference

    @staticmethod
    def __skipSequence(counter):
        result = []
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
        for i in range(index - length,index+1):
            result.append(RFCA.__allowedSymbol(SecondFrame[channel][i]));
        return result

    def computeSequences(self,BaseFrame,SecondFrame):
        result = [[],[],[]]
        difference = self.FrameDiff(BaseFrame,SecondFrame)

        for c in range(0,len(SecondFrame)):
            Skip = 0
            for i in range(0,len(BaseFrame[c])):
                if i < (self.sequentialposition+1)*self.sequentiallength and i >= self.sequentialposition*self.sequentiallength and self.correctseqential:
                    difference[c][i] = 100;#Fake difference

                if difference[c][i] == 0:
                    Skip +=1
                elif Skip == 0 and difference[c][i] != 0:
                    result[c].append(RFCA.__allowedSymbol(SecondFrame[c][i]))
                elif Skip > 0 and Skip <= 2 and difference[c][i] != 0:
                    result[c] += RFCA.__recoverShortSkips(BaseFrame = BaseFrame,SecondFrame = SecondFrame,length = Skip,channel = c, index = i)
                    Skip = 0

                elif Skip > 2 and difference[c][i] != 0:
                    result[c] += RFCA.__skipSequence(counter = Skip)
                    Skip = 0
                    result[c].append(RFCA.__allowedSymbol(SecondFrame[c][i]))

        if self.correctseqential:
            self.sequentialposition +=1;
            if self.sequentiallength*self.sequentialposition > len(BaseFrame[0]):
                self.sequentialposition = 0
        return result

    def addFrame(self,newFrame):
        if self.initNewFrame(newFrame) is True:
            return
        self.last = self.computeSequences(self.frame,newFrame)
        self.counter +=1
        self.frame = newFrame

    def setLastFrame(self,newFrame):
        self.frame = newFrame

    def initNewFrame(self, newFrame):
        if self.frame == None:
            self.frame = [[0]*len(newFrame[0]),[0]*len(newFrame[0]),[0]*len(newFrame[0])]
            self.last = self.computeSequences(self.frame,newFrame)
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
