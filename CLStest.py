import socket,sys
class UndefinedOutputType(Exception):
    def __init__(self, value = None):
        self.value = value

    def __str__(self):
        return "Output object was not assigned any type of <class>Output!"+ "\n" + repr(self.value)

class Output():
    def __init__(self):
        self.type = None
        self.compression = False
        self.fps = 30

    def setCompression(self,compression):
        if not type(compression) is boolean:
            return False
        self.compression = compression
        return True

    def setFPS(self,fps):
        fps = int(fps)
        if fps <= 0:
            return False
        self.fps = fps
        return True

    def output(self):
        raise UndefinedOutputType(self.output);
        #Since not implemented here

class TCPClient(Output):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def reconnect(self):
        return "reconnecting..."
        pass

    def output(self):
        print "I am outputting now"
        #Connect


if __name__ == "__main__":

    foo = TCPClient("172.0.0.1",3346);
    print foo.output()
    print foo.reconnect()
