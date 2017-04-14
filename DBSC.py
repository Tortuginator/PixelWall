class DBSC:
    global modi,shift
    modi = [2,4,8,16,32,64,128]
    shift = [1,2,3,4,5,6,7]
    def __init__(self,data):
        #'{0:b}'.format(42)
        self.data = data
        self.IA = [] #Indent
        self.DA = [] #Data
        self.SA = [] #Second

    def CalculateMode(self,shiftI = 0):

        tmp = [0,0,0,0,0,0,0]
        for i in self.data:
			for m in range(0,len(modi)):
				if i < (modi[m]+shiftI)%256:tmp[m] +=1;
        minM = 0
        minV = 10000000
        for i in range(0,len(tmp)):
            r = self.length(i,len(self.data),tmp[i])
            if r > 0:
                if r < minV:
                    minM = i
                    minV = r
        p = minV+3
        print "Expecting:",minM,"as mode and Length:",minV/8,minV,"Realistic:",p/8
        return minM

    @staticmethod
    def FindSmallestArea(array):
        tmpSmall = [0,0,0,0,0,0,0]
        tmpShift = [0,0,0,0,0,0,0]
        for i in range(0,len(modi)):
            innertmp = []
            for r in range(0,256):
                c = (r+modi[i]) % 256
                if r != 0:
                    #if not array[c] <= array[r-1]:#if the most outest position is smaller then the most inner position of the previous ind
                    v = DBSC.SumArrayArea(r,modi[i],array)
                    if tmpSmall[i] < v:
                        tmpSmall[i] = v
                        tmpShift[i] = r
                else:
                    v = DBSC.SumArrayArea(r,modi[i],array)
                    tmpSmall[i] = v
                    tmpShift[i] = r
        return tmpSmall,tmpShift

    @staticmethod
    def SumArrayArea(start,length,array):
        integral = 0
        for i in range(start,start+length):
            p = i % 256
            integral += array[p]
        return integral

    def CalculateShiftMode(self):
        tmp = []
        total = len(self.data)
        for i in range(0,256):
            tmp.append(0)

        #Get Number of occurances
        diff = 0
        for i in self.data:
            tmp[i] +=1
            diff+=i
        print "AvgDiff:",diff/len(self.data)
        r = DBSC.FindSmallestArea(tmp)
        print r
        minI = 0
        minM = 0
        minV = 0
        for i in range(0,len(r[0])):
            c = self.length(i,len(self.data),r[0][i])
            if minV == 0:
                minV = c
                minI = i
                minM = modi[i]
            elif minV > c:
                minV = c
                minI = i
                minM = modi[i]
        return minV,minV/8,minI

    @staticmethod
    def length(bitlength,length,counter):
        bitlength +=1
        return length + bitlength*counter + 8*(length-counter)

    def Compress(self):
        #'{0:b}'.format(42)
        mode = self.CalculateMode()
        print "Automode",mode,"at@",modi[mode]
        count = 0
        for i in self.data:
            if i > modi[mode]:
                self.IA.append(1)#additional
                self.DA.append(i)
            else:
                self.DA.append(i)
                self.IA.append(0)
                count +=1

        bitmode = '{0:b}'.format(mode)
        while len(bitmode) < 3:
            bitmode +="0"+bitmode

        restmp = bitmode
        res = []
        for i in range(0,len(self.IA)):
            t = '{0:b}'.format(self.DA[i])
            if self.IA[i] == 0:
                if len(t) < mode+1:
                    while len(t) < mode+1:
                        t = "0" + t
                x = "0"
                restmp = restmp + t + x
            else:
                if len(t) < 8:
                    while len(t) < 8:
                        t = "0" + t
                x = "1"
                restmp = restmp + t[0:mode+1] + x + t[mode+1:8]
            r = len(restmp)
            if r >= 8:
                res.append(int(restmp[0:8], 2))
                restmp = restmp[8:len(restmp)]
        if restmp != "":
            while len(restmp) > 8:
                res.append(int(restmp[0:8], 2))
                restmp = restmp[8:len(restmp)]
            #do end
            v = int(restmp,2)
            res.append(v)
        return res
