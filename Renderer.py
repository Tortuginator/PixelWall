import socket,sys
import time,datetime
from threading import Thread

class CompressionType():
    No = 0
    Linear = 1
    Object = 2

    @staticmethod
    def isCompression(compression):
        if compression in [0,1,2]:
            return True
        return False

class failedToReconnect(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "The socket tried 3 times in a row to connect to the server without success"+ "\n" + repr(self.value)

class wrongObject(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "It seems like a other object was expected: "+ "\n" + repr(self.value)

class InvalidCompression(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "It seems like the Compression given was not recognized "+ "\n" + repr(self.value)

class socketNotInitialized(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "The socket was not initialized. I seems like you forgot that when you initialized the <TCPClient>. The socket can be initialized by calling \"reconnect()\""+ "\n" + repr(self.value)

class PrintRegister():
    def __init__(self):
        self.currentlyPrinting = False
        self.instance = None
        self.register = []
        self.__fireUp();

    def __fireUp(self):
        self.instance = Thread(target = PrintRegister.__print, args = (self, ))
        self.instance.start();

    def __print(self):
        for i in self.register:
            print i
        #reset
        self.register = []


    def doPrint(self,out):
        if not self.instance.isAlive:
            self.__fireUp();
        self.register.append(out);
global PNR
PNR = PrintRegister();
class UtilPrint():
    @staticmethod
    def compose(sign,parent,function,message):
        PNR.doPrint("[" + sign + "][" +parent+ "][" +function + "] " + message)

class FrameFormat():
    def __init__(self,data = None,compression = None,objects = None):
        if compression == None:
            self.compression = None
        else:
            if CompressionType.isCompression(compression) :
                self.compression = compression
            else:
                raise InvalidCompression;

        self.data = data
        self.objects = objects

    def fromTransport(self,data):
        #Convert:
        data = bytearray(data);
        Ldat = len(data);
        #Structure:
        #[Compression (0,1,2)][EXTRA+6]
        if int(data[0]) in [CompressionType.No,CompressionType.Linear]:
            #[Lengtha1][lengtha2][Lengthb1][lengthb2][lengthc1][lengthc2]
            #totalLength = 255*Lengthxa[0-255] + Lengthxb[0-255]|| MAX: 65280bytes length*3 + 7
            totalLengthR = int(ldat[1]) * 255 + int(ldat[2])
            totalLengthG = int(ldat[3]) * 255 + int(ldat[4])
            totalLengthB = int(ldat[5]) * 255 + int(ldat[6])
            if Ldat != (totalLengthR + totalLengthG + totalLengthB+7):
                UtilPrint.compose("!",self.__class__,__name__,"failed to decode. The lengths do not match. The packet will be ignored.")
                return False
            newdata = [[],[],[]]
            newdata[0] = data[8:8+totalLengthR]
            newdata[1] = data[totalLengthR+8+1:totalLengthG+8+totalLengthR]
            newdata[2] = data[totalLengthG+8+totalLengthR+1:totalLengthG+8+totalLengthR+totalLengthB]
            self.data = newdata
            self.compression = int(data[0])
            return True
        elif int(data[0]) == CompressionType.Object:
            raise NotImplementedError;
        return False

    def toTransport(self,forceRaw = False):
        if self.compression == CompressionType.No:
            if not forceRaw:
                self.compression == CompressionType.Linear
                self.data = FrameFormat.__convertRawToLin(self.data)
            else:
                lenR = len(self.data[0])
                lenG = len(self.data[1])
                lenB = len(self.data[2])
                if lenG != lenR != lenB:
                    UtilPrint.compose("!",self.__class__,__name__,"the lenghts of the color arrays do not match in RAW mode!")
                header = bytearray([0,lenR//255,lenR%255,lenG//255,lenG%255,lenB//255,lenB%255])
                if type(self.data[0]) == list:
                    R = bytearray(self.data[0])

                if type(self.data[1]) == list:
                    G = bytearray(self.data[1])

                if type(self.data[2]) == list:
                    B = bytearray(self.data[2])
                return (header + R + G + B)

        if self.compression == CompressionType.Linear:
            lenR = len(self.data[0])
            lenG = len(self.data[1])
            lenB = len(self.data[2])
            header = bytearray([1,lenR//255,lenR%255,lenG//255,lenG%255,lenB//255,lenB%255])
            if type(self.data[0]) == list:
                R = bytearray(self.data[0])

            if type(self.data[1]) == list:
                G = bytearray(self.data[1])

            if type(self.data[2]) == list:
                B = bytearray(self.data[2])
            return (header + R + G + B)

    def toRaw(self):
        if self.compression == 0:
            return self.data
        elif self.compression == 1:
            return FrameFormat.__convertLinToRaw(self.data)
        elif self.compression == 2:
            return None #not posible
        return None

    def toLinear(self):
        if self.compression == 0:
            return FrameFormat.__convertRawToLin(self.data);
        elif self.compression == 1:
            return self.data
        elif self.compression == 2:
            return None #not possible
        return None

    def toObject(self):
        if self.compression == 0:
            return None#Rendered
        elif self.compression == 1:
            return None#Rendered to LIN
        elif self.compression == 2:
            return self.data;
        return None

    @staticmethod
    def __convertLinToRaw(data):
        indicator = 1;
        new = [[],[],[]]
        cnt = -1
        for i in data:
            locked = None
            cnt +=1
            for x in range(0,len(i)):
                if i[x] == indicator:
                    if x + 2 <= len(i):
                        #[Indicator][Value][Count]
                        for r in range(0,i[x+2]+1):
                            new[cnt].append(i[x+1])#new value
                        locked = x+2;
                    else:
                        UtilPrint.compose("!","UDN",__name__,"found indicator byte at unintended position please check you indicator bytes")
                elif x <= locked:
                    pass
                    #to be ignored, because theese are the indicator and value bytes
                else:
                    new[cnt].append(i[x])

        len_old = len(data[0])+ len(data[1]) + len(data[2])
        len_new = len(new[0])+ len(new[1]) + len(new[2])
        UtilPrint.compose("+","UDN",__name__,"compression efficiency: " + repr(100-int((float(len_old)/float(len_new))*100)) + "%")
        return new;

    @staticmethod
    def __convertRawToLin(data):
        indicator = 1;replacement = 2;new = [[],[],[]];
        for cnt in range(0,len(data)):
            i = data[cnt];run = 0;last = None
            for x in range(0,len(i)):
                if last == i[x]:
                    run += 1
                    #not over 255
                else:
                    if run == 3:#3
                        if x-3 >= 0:
                            if i[x-1] == indicator:
                                new[cnt].append(replacement)
                            else:
                                new[cnt].append(i[x-3])
                    if run > 1 and run < 4:#3,2
                        if x-2 >= 0:
                            if i[x-2] == indicator:
                                new[cnt].append(replacement)
                            else:
                                new[cnt].append(i[x-2])
                    if run > 0 and run < 4:#3,2,1
                        if x-1 >= 0:
                            if i[x-1] == indicator:
                                new[cnt].append(replacement)
                            else:
                                new[cnt].append(i[x-1])
                    #new[i].append(x[i])
                    #[Indicator][Value][Count]
                    if run > 3:
                        new[cnt].append(indicator)
                        new[cnt].append(last)
                        new[cnt].append(run-1)
                    last = i[x]
                    run = 1
            if x == len(i)-1:
                if i[x] == indicator:
                    new[cnt].append(replacement)
                else:
                    new[cnt].append(i[x])
        return new

    def setData(self,data,compression):
        self.data = data
        self.compression = compression

class Output():
    def __init__(self):
        self.type = None
        self.compression = False
        self.fps = 30
        self.supportedCompression = [None]

    def setCompression(self,compression):
        if not type(compression) is bool:
            return False
        self.compression = compression
        return True

    def setFPS(self,fps):
        fps = int(fps)
        if fps <= 0:
            return False
        self.fps = fps
        return True

    #ABSTRACT
    def output(self,data):
        raise NotImplementedError;


class BinaryFile(Output):
    def __init__(self, filename = "output.bin", path = ""):
        self.filename = filename
        self.filepath = path
        self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]

    def __preparedata(self, data):
        return data

    def output(self,data):
        data = self.__prepareData(data);
        with open(path + filename, "wb") as f:
			f.write(data)


class TCPClient(Output):
    def __init__(self,ip,port,connectOnInit = True):
        self.ip = ip
        self.port = port
        self.failcounter = 0;
        self.failmax = 3;
        self.socket = None
        self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]

        if connectOnInit:
            self.__connect();

    def __connect(self,force = False):
        if (self.failcounter >= self.failmax) and not force:
            raise failedToReconnect;
        try:
            UtilPrint.compose("+",self.__class__,__name__,"[+][TCPc]Connecting ",repr(self.ip),"@",repr(self.port))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.failcounter = 0
        except Exception,e :
            self.failcounter += 1
            self.__connect()
            UtilPrint.compose("+",self.__class__,__name__,"[!][TCPc]Socket excption, trying to reconnect: ", repr(e))

    def reconnect(self,force = False):
        self.__connect(force);

    def resetReconnectAttemps(self):
        self.failcounter = 0
        return True

    def __prepareData(self,data):
        return data.toTransport();

    def output(self,data):
        data = self.__prepareData(data)
        if socket == None:
            raise socketNotInitialized;
        try:
            self.socket.send(data)
        except socket.timeout:
            UtilPrint.compose("!",self.__class__,__name__,"Socket timeout",repr(self.ip),"@",repr(self.port))
            self.reconnect();
        #Connect
    def close(self):
        self.socket.close();

class Input():
    def __init__(self):
        self.fps = 30
        self.data = None
        self.distinct = None
        self.supportedCompression = [None]

    def setFPS(self,fps):
        fps = int(fps)
        if fps <= 0:
            return False
        self.fps = fps
        return True

    def callData(self):
        raise NotImplementedError;

    def updateSinceLastCall(self):
        raise NotImplementedError;

class PyGame(Input):
    def __init__(self,pyGameobj):
        self.PYobj = pyGameobj
        self.supportedCompression = [CompressionType.No,CompressionType.Linear]

    def callData(self):
        raise NotImplementedError

    def updateSinceLastCall(self):
        raise NotImplementedError

class Function(Input):
    def __init__(self,function):
        self.function = function
        self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]

    def callData(self,args):
        return self.function(args);

    def updateSinceLastCall(self):
        return True;
        #Allways true, because it should be called each time when it gets called from the engine

class TCPServer(Input):
    def __init__(self,ip = '',port = 4000):
        self.ip = ip;
        self.port = port;
        self.instance = None
        self.socket = None
        self.buffer = 1024*500
        self.distinct = None
        self.failcounter = 0
        self.maxfails = 3
        self.supportedCompression = [CompressionType.No,CompressionType.Linear,CompressionType.Object]
        self.__fireUp();

    def setBuffer(self,buffer):
        if buffer != int(buffer) or not buffer > 0:
            return False

        self.buffer = buffer
        return True

    def __fireUp(self):
        self.failcounter += 1
        UtilPrint.compose("+",self.__class__,__name__,"Starting...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip,self.port))
        self.instance = Thread(target = TCPServer.__srvThread, args = (self, ))
        self.instance.start();
        UtilPrint.compose("+",self.__class__,__name__,"Started")

    @staticmethod
    def __srvThread(self):
        self.socket.listen(1)
        while True:
            connection, client_address = self.socket.accept()
            self.failcounter = 0;
            try:
                UtilPrint.compose("+",self.__class__,__name__,"Client connected " + repr(client_address))
                while True:
                    data = connection.recv(self.buffer)
                    if len(data) == 0: break
                    self.__updateIncoming(data);
                    #connection.sendall(data)
                UtilPrint.compose("+",self.__class__,__name__,"Client disconnected " + repr(client_address))
            finally:
                connection.close()
                UtilPrint.compose("+",self.__class__,__name__,"Client disconnected "+ repr(client_address))

    def __verify(self,data):
        return FrameFormat.fromTransport(data);

    def __updateIncoming(self,data):
        isOK = self.__verify(data);
        if isOK is not False:
            self.data = isOK
            self.distinct = True
        else:
            UtilPrint.compose("!",self.__class__,__name__,"Recived corrupt package data. Dumping Frame")

    def callData(self,force = False):
        if not self.distinct is True and force is False:
            return False
        self.distinct = False;
        #Check if server is still running
        if not self.instance.isAlive():
            if self.failcounter >= self.maxfails:
                raise failedToReconnect; #LOOK FOR SOMETHING BETTER
            self.__fireUp();
        return self.data

    def updateSinceLastCall(self):
        return self.distinct;

class TimeTrigger():
    def __init__(self,timesPerSecond,function,args):
        self.timesPerSecond = timesPerSecond
        self.function = function
        self.args = args
        self.__setVars();
        self.iteration = 0
        self.isSleeping = True

    def __setVars(self):
        self.msDelta = int((1/float(timesPerSecond))*1000000)

    def isDue(self,time):
        if not((self.iteration * self.msDelta) < time):
            return False
        else:
            return True

    def doExecute(self, args = None):
        if self.isDue is False:return False;
        if args != None:
            self.args = args

        self.iteration +=1;
        self.isSleeping = False
        self.function(self.args);
        self.isSleeping = True

        if self.timesPerSecond-1 <= self.iteration:
            self.reset();

    def reset(self):
        self.iteration = 0

class TimeManager():
        def __init__(self):
            self.baseFrequency = 120
            self.instance = None
            self.triggers = []

        def __fireUp(self):
            for i in self.triggers:
                if i is not type(TimeTrigger):
                    raise wrongObject("Expecting TimeTrigger")


        def __tmeThread(self,triggers):
            innerTiming = datetime.datetime.now()
            innerStep = 0
            innerMicrosecondDelta = int(float(1/float(self.baseFrequency))*1000000)
            while(True):
                if not(innerStep*innerMicrosecondDelta <= ((datetime.datetime.now() - innerTiming).microseconds)):
                    time.sleep(0.001)
                    continue
                if innerStep >= self.baseFrequency-1:
                    innerStep = 0
                    innerTiming = datetime.datetime.now()
                innerStep +=1

                for i in triggers:
                    if i.isSleeping is True:
                        try:
                            i.doExecute()
                        except Exception,e:
                            UtilPrint.compose("!",self.__class__,__name__,"Exception occured for " + repr(i.function)  + " @iteration " + repr(innerStep))
                            UtilPrint.compose("!",self.__class__,__name__,repr(e))

        def __tmeExec(self,function,args):
            pass




if __name__ == "__main__":
    a = FrameFormat()
    i = [[112,12,32,32,32,32,32,32,2],[112,12,32,32,32,2,32,32,2],[112,12,32,32,32,32,32,32,2]]
    i = [[0,2,2,2,2,2,2,2,2,2,2,0],[0,2,2,2,2,2,2,2,2,2,2,0],[0,2,2,2,2,2,2,2,2,2,2,0]]
    print i
    a.setData(i,CompressionType.No)
    print a.toLinear();
    b = FrameFormat();
    b.setData(a.toLinear(),1);
    print b.toRaw();

class Pixel():
    def __init__(X,Y):
        self.X = X
        self.Y = Y

class Engine():
    def __init__(self,height,width):
        self.baseFrequency = 30
        self.frameHeight = height
        self.frameWidth = width
        self.brightness = float(1)
