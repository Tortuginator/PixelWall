import socket,sys
import time
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

class socketNotInitialized(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "The socket was not initialized. I seems like you forgot that when you initialized the <TCPClient>. The socket can be initialized by calling \"reconnect()\""+ "\n" + repr(self.value)

class FrameFormat():
    def __init__(self):
        self.compression = None
        self.data = None
        self.objects = None

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
                        print "[!][Conv][LIN2RAW] found indicator byte at unintended position please check you indicator bytes"
                elif x <= locked:
                    pass
                    #to be ignored, because theese are the indicator and value bytes
                else:
                    new[cnt].append(i[x])

        len_old = len(data[0])+ len(data[1]) + len(data[2])
        len_new = len(new[0])+ len(new[1]) + len(new[2])
        print "[+][Conv][LIN2RAW] compression efficiency: ",100-int((float(len_old)/float(len_new))*100),"%"
        return new;

    @staticmethod
    def __convertRawToLin(data):
        indicator = 1
        new = [[],[],[]]
        cnt = -1
        for i in data:
            cnt +=1
            run = 0
            last = None
            for x in range(0,len(i)):
                if last == i[x]:
                    run += 1
                    #not over 255
                else:
                    if run == 3:#3
                        if x-3 >= 0:
                            new[cnt].append(i[x-3])
                    if run > 1 and run < 4:#3,2
                        if x-2 >= 0:
                            new[cnt].append(i[x-2])
                    if run > 0 and run < 4:#3,2,1
                        if x-1 >= 0:
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
            print "[+][TCPc]Connecting ",repr(self.ip),"@",repr(self.port)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.failcounter = 0
        except Exception,e :
            self.failcounter += 1
            self.__connect()
            print "[!][TCPc]Socket excption, trying to reconnect: ", repr(e)

    def reconnect(self,force = False):
        self.__connect(force);

    def resetReconnectAttemps(self):
        self.failcounter = 0
        return True

    def __prepareData(self,data):
        return data

    def output(self,data):
        data = self.__prepareData(data)
        if socket == None:
            raise socketNotInitialized;
        try:
            self.socket.send(data)
        except socket.timeout:
            print "[!][TCPc]Socket timeout",repr(self.ip),"@",repr(self.port)
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
        print "[+][TCPs] Starting..."
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip,self.port))
        self.instance = Thread(target = TCPServer.__srvThread, args = (self, ))
        self.instance.start();
        print "[+][TCPs] Started"

    @staticmethod
    def __srvThread(self):
        self.socket.listen(1)
        while True:
            connection, client_address = self.socket.accept()
            self.failcounter = 0;
            try:
                print "[+][TCPs] Client connected ", repr(client_address)
                while True:
                    data = connection.recv(self.buffer)
                    if len(data) == 0: break
                    self.__updateIncoming(data);
                    #connection.sendall(data)
                print "[+][TCPs] Client disconnected ", repr(client_address)
            finally:
                connection.close()
                print "[+][TCPs] Client disconnected ", repr(client_address)

    def __verify(self,data):
        return data;

    def __updateIncoming(self,data):
        isOK = self.__verify(data);
        if isOK is not False:
            self.data = isOK
            self.distinct = True
        else:
            print "[!][TCPs] Recived corrupt package data. Dumping Frame"

    def callData(self,force = False):
        if not self.distinct is True and force is False:
            return False
        #Check if server is still running
        if not self.instance.isAlive():
            if self.failcounter >= self.maxfails:
                raise failedToReconnect; #LOOK FOR SOMETHING BETTER
            self.__fireUp();
        return self.data

    def updateSinceLastCall(self):
        return self.distinct;


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
