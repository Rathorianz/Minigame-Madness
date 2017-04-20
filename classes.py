import math
import pygame
class Grid:

    def __init__(self, screen, initx = 7, inity = 6, initwidth = 50):
        RED = (255, 0, 0)
        self.color = RED
        self.matrix = [[0 for x in range(initx)]for x in range(inity)]
        self.initx = initx
        self.inity = inity
        self.initwidth = initwidth
        self.screen = screen
        self.xOffset = 0
        self.yOffset = 75
        self.boardYOffset = self.yOffset + 25
        self.gridLineWidth = 1
        self.MovingPiecePosition = (self.initx//2)+1
        self.currentMovingPiece = 0

        self.pieces = []
        for i in range (self.initx * self.inity):
            if (i%2==0):
                self.pieces.append(Piece('C',self.initwidth))
            else:
                self.pieces.append(Piece('U',self.initwidth))
        #self.drawgrid()
        self.startGame()

    def GetXLocation(self):
        returnValue = self.xOffset+ (self.gridLineWidth*(self.MovingPiecePosition) +(self.initwidth * self.MovingPiecePosition))
        return returnValue

    def GetXGridLocation(self,x):
        returnValue = self.xOffset+ (self.gridLineWidth*(x) +(self.initwidth * x))
        return returnValue

    def GetYGridLocation(self,y):
        returnValue = self.boardYOffset+(self.gridLineWidth*(self.inity - y) +(self.initwidth * (self.inity - y)))
        return returnValue

    def startGame(self):
        self.screen.fill(self.color)
        self.currentMovingPiece = 0
        self.continueGame()

    def continueGame(self):
        self.pieces[self.currentMovingPiece].drawMoving(self.screen, self.yOffset ,self.GetXLocation())

    def MoveMovingPiece(self,direction):
        # L for left,  R for right and D for down.
        if (self.validateMove(direction) == True):

            if (direction == 'L' or direction == 'R'):
                self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())

                if (direction == 'L'):
                    self.MovingPiecePosition-=1
                if (direction == 'R'):
                    self.MovingPiecePosition+=1
                self.pieces[self.currentMovingPiece].drawMoving(self.screen, self.yOffset ,self.GetXLocation())

            if (direction == 'D'):
                if (self.checkNewAvailableSquare(self.MovingPiecePosition) != -1):

                    self.pieces[self.currentMovingPiece].y=self.checkNewAvailableSquare(self.MovingPiecePosition)
                    self.pieces[self.currentMovingPiece].x=self.MovingPiecePosition

                    if (self.currentMovingPiece < (self.initx * self.inity) - 1):
                        self.currentMovingPiece += 1
                        self.continueGame()
                        self.drawgrid()
                    else:
                        self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())
                        self.drawgrid()
                        print ("game over!!! no one won")
                    #self.didUserWin()
                    #self.ComputerMove()
                    #self.moveAndDrop()
                else:
                    print("no move")


    def checkNewAvailableSquare(self,x):
        ColumnLocation = 0
        for i in range (self.initx * self.inity):
            if (self.pieces[i].x == x):
                if (self.pieces[i].y >=ColumnLocation):
                    if (self.pieces[i].y < self.inity-1):
                        ColumnLocation = self.pieces[i].y+1
                    else:
                        ColumnLocation = -1
        return ColumnLocation


    def validateMove(self, direction):
        if (direction == 'L'):
            if (self.MovingPiecePosition <=1):
                return False
        if (direction == 'R'):
            if (self.MovingPiecePosition >=self.initx):
                return False
        if (direction == 'D'):
            return True
        return True

    def placepiece(self): #work on this check if you can put the piece there return location of the piece to the controller
        print("initialing pieces")

    def drawpieces(self):
        for i in range (self.initx * self.inity):
            #self.pieces[i].x =
            if (self.pieces[i].x != -1 and self.pieces[i].y != -1):
                self.pieces[i].drawObject(self.screen,self.GetXGridLocation(self.pieces[i].x),self.GetYGridLocation(self.pieces[i].y))

    def drawgrid(self):
        WHITE = (255, 255, 255)

        rect_x = self.xOffset
        rect_y = self.yOffset

        for r in range (self.initx):
            rect_x += self.initwidth + self.gridLineWidth
            rect_y = self.yOffset
            for c in range (self.inity):
                rect_y += self.initwidth + self.gridLineWidth
                pygame.draw.rect(self.screen, WHITE, [rect_x, rect_y, self.initwidth, self.initwidth])
        self.drawpieces()



    #def check(self): #work on this to return if the user won lost or draw
#algorithm to check if 4 in a row
class Piece:
    def __init__(self, playertype,diameter, x=-1, y=-1):
        self.x = x
        self.y = y
        GREEN = (0,255 , 0)
        BLUE = (0, 0, 255)
        RED = (255,0,0)
        self.backColor = RED
        if (playertype == "C"):
            self.color = GREEN
        else:
            self.color = BLUE
        self.diameter = diameter -2

    def drawObject(self,screen,rect_x,rect_y):

        if (self.x != -1 and self.y != -1):
            pygame.draw.circle(screen, self.color, [rect_x+self.diameter//2, rect_y],(self.diameter-10)//2)

    def setPieceCoordinate(self,x,y):
        self.x = x
        self.y = y

    def drawMoving(self,screen,rectY,rectX):
        pygame.draw.circle(screen, self.color, [rectX+self.diameter//2, rectY] ,((self.diameter-10)//2))

    def RemoveMe(self,screen,rectY,rectX):
        pygame.draw.circle(screen, self.backColor, [rectX+self.diameter//2, rectY] ,((self.diameter-10)//2))

    def move(self, dire):
        if(dire == 'a'):   #NTS restriction i.e. self.x-1 <= abs(3)
            self.x - 1
        elif(dire == 's'): #NTS goes down till there is a piece below or bottom of grid....while loop
            self.y
        elif(dire == 'd'): #NTS restriction i.e. self.x+1 <= abs(3)
            self.x + 1
