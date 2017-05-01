import uuid
import PixelWall,WebDriver
startscreenPong = [
                [2,2,2,0,2,2,2,0,2,0,0,2,0,2,2,2],
                [2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,0],
                [2,2,2,0,2,0,2,0,2,0,2,2,0,2,0,2],
                [2,0,0,0,2,0,2,0,2,0,0,2,0,2,0,2],
                [2,0,0,0,2,2,2,0,2,0,0,2,0,2,2,2]
                ]
startscreenPlay = [
                    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,2,2,2,0,2,0,0,0,2,2,2,0,2,0,2,0,2],
                    [2,0,2,0,2,0,2,0,0,0,2,0,2,0,2,0,2,0,2],
                    [2,0,2,2,2,0,2,0,0,0,2,2,2,0,2,2,2,0,2],
                    [2,0,2,0,0,0,2,0,0,0,2,0,2,0,0,0,2,0,2],
                    [2,0,2,0,0,0,2,2,2,0,2,0,2,0,0,0,2,0,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
                ]

class Player():
    def __init__(self,name):
        self.name = name
        self.ID = str(uuid.uuid4())

    def getID(self):
        return self.ID

    def getPosition(self):
        return self.position

    def setPosition(self,position):
        return self.position


class GameControl():
    def __init__(self):
        self.players = None
        self.stats = None
        self.winTerms = GameControl.isWinner
        self.waiting = []

    def NewGame(self,player1,player2):
        self.players = (player1,player2)
        self.stats = (0,0)

    def registerToPlay(self,player):
        if player not in self.waiting:
            self.waiting.append(player)

    def getToPlay(self):
        if len(self.waiting) !=0:
            p = self.waiting[0]
            del self.waiting[0]
            return p
        else:
            return None

    @staticmethod
    def isWinner(stats):
        #return 0 - nothing happens, 1 player1, 2 player2 winns
        if stats[0] == 5:
            return 1
        elif stats[1] == 5:
            return 2
        return 0

    def isPlaying(self,player):
        if player in self.players:
            return True
        return False

    def givePoints(self,player,ammount):
        if self.isPlaying(player):
        if self.players[0] == player:
            self.stats = (self.stats[0]+ammount,self.stats[1])
        elif self.players[1] == player:
            self.stats = (self.stats[0],self.stats[1]+ammount)
        winstat = self.winTerms(self.stats)
        if winstat !=0:
            self.declareWinner(players[winstat-1])

    def getPoints(self):
        return self.stats

    def declareWinner(self,player):
        print "Winner",player, "with",self.stats

class Ball():
    def __init__(self):
        self.x = 0
        self.y = 0

class PingGame():
    def __init__(self,GameManager):
        self.GM = GameManager
        self.ball = Ball()
        self.ballDirX = -1
        self.ballDirY = -1

    def new(self):
        self.GM.NewGame(self.GM.getToPlay(),self.GM.getToPlay())

    def Render(self,dFrame):
        self.dFrame = dFrame

    def InitBall(self):
        #Initiate variable and set starting positions
        #any future changes made within rectangles
        self.ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2
        self.ball.x = WINDOWHEIGHT/2 - LINETHICKNESS/2
        self.GM.player[0].position = (dFrame.height - 5) /2
        self.GM.player[1].position = (dFrame.height - 5) /2

        #Keeps track of ball direction
        self.ballDirX = -1 ## -1 = left 1 = right
        self.ballDirY = -1 ## -1 = up 1 = down

    def paddleCollision(self):
        p0 = []
        p1 =
        for i in range(-2,2):
            p0.append(self.GM.players[0].position+i)
            p1.append(self.GM.players[1].position+i)

        if self.ballDirX == -1 and self.ball.y == 0 and self.ball.x in p0:
            return -1
        elif self.ballDirX == 1 and self.dFrame.width-1 == ball.y and self.ball.x in p1:
            return -1
        else: return 1
        #ballDirX * return

    def isCaughtByPlayer(self):
        if ball.x < 0:
            self.GM.givePoints(self.GM.player[1],1)
            self.InitBall()
        elif ball.x>= self.dFrame.width:
            self.GM.givePoints(self.GM.player[0],1)
            self.InitBall()
        return 0

    #P1 -- P2#





class APIcalls():
	def __init__(self,Engine):
		self.Engine = Engine
		self.calls =  {
			"/API/pong/control/up":self.controlUp,
            "/API/pong/control/down":self.controlDown,
            "/API/pong/player/new":self.newPlayer,
            "/API/pong/player/leave":self.delPlayer,
            "/API/pong/game/status":self.status,
            "/API/pong/game/new":self.newGame
			};


	def controlUp(self, details, cl):

		cl.send(json.dumps({"response":{"status":"success","message":"Matrix activated","key":"valid"}}),"application/json")

	def genChill(self, details, cl):
		self.Engine.AnimationManagementSystem.clear()

		testChill = PixelWall.PresetAnimations.Chill.Chill(ColorLower=(150,100,0) ,ColorHigher = (255,200,0))
		Ani = PixelWall.Animations.Animation(rFunc = testChill,startframe = 0,infinity = True)
		self.Engine.AnimationManagementSystem.addAimation(Ani)

		cl.send(json.dumps({"response":{"status":"success","message":"Chill activated","key":"valid"}}),"application/json")
