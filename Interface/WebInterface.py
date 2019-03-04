from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class WebInterface(object):
    def __init__(self):
        self.WebsocketInstance = None
        self.__setup()

    def __setup(self):
        self.WebsocketInstance = SimpleWebSocketServer('',8000,WSServerClientInstance)
        self.WebsocketInstance.serveforever()

class WSServerClientInstance(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print self.data
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


if __name__ == "__main__":
    A = WebInterface()
    