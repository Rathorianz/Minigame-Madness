import math
import pygame
class Grid:

    def __init__(self, screen, startingplayer = 'C', initx = 7, inity = 6, initwidth = 75):
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        self.color = BLUE
        self.matrix = [[0 for x in range(initx)]for x in range(inity)]
        self.initx = initx
        self.inity = inity
        self.initwidth = initwidth
        self.screen = screen
        self.xOffset = 0
        self.yOffset = 75
        self.boardYOffset = self.yOffset + 40
        self.gridLineWidth = 1
        self.MovingPiecePosition = (self.initx//2)+1
        self.currentMovingPiece = 0
        self.currentPlayer = 0
        self.startingplayer = startingplayer
        if (self.startingplayer == 'C'):
            self.secondplayer = 'U'
        else:
            self.secondplayer = 'C'

        self.pieces = []
        for i in range (self.initx * self.inity):
            if (i%2==0):
                self.pieces.append(Piece(self.startingplayer,self.initwidth))
            else:
                self.pieces.append(Piece(self.secondplayer,self.initwidth))
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
                    self.didPlayerWin()
                    #self.canIwin()
                        #if yes
                            #self.ComputerMove()
                        #else
                            #self.canplayerwin()

                    #self.moveAndDrop()
                else:
                    print("no move")

    def didPlayerWin(self):
        if(self.didPlayerWinHorizontally() == True or self.didPlayerWinVertically() == True or self.didPlayerWinDiagonally() == True):
            print("won")

    def getPieceGivenXY(self,x,y):
        for i in range (self.initx * self.inity):
            if (self.pieces[i].x == x and self.pieces[i].y == y):
                return self.pieces[i]
        return ""

    def didPlayerWinHorizontally(self):
        for i in range (self.inity):
            for j in range (self.initx - 2):
                piece1 = self.getPieceGivenXY(j, i)
                piece2 = self.getPieceGivenXY(j + 1, i)
                piece3 = self.getPieceGivenXY(j + 2, i)
                piece4 = self.getPieceGivenXY(j + 3, i)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    return True
        return False

    def didPlayerWinVertically(self):
        for i in range (self.initx + 1):
            for j in range (self.inity - 3):
                piece1 = self.getPieceGivenXY(i, j)
                piece2 = self.getPieceGivenXY(i, j + 1)
                piece3 = self.getPieceGivenXY(i, j + 2)
                piece4 = self.getPieceGivenXY(i, j + 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    return True
        return False

    def checkforwinning(self,piece1, piece2, piece3, piece4):
        if (piece1 != "" and  piece2 != "" and  piece3 != "" and piece4 != "" and piece1.color == piece2.color == piece3.color == piece4.color):
            return True
        else:
            return False

    def didPlayerWinDiagonally(self):
        for i in range (self.inity - 2):
            for j in range (self.initx - 2):
                piece1 = self.getPieceGivenXY(j, i)
                piece2 = self.getPieceGivenXY(j + 1, i + 1)
                piece3 = self.getPieceGivenXY(j + 2, i + 2)
                piece4 = self.getPieceGivenXY(j + 3, i + 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    return True

        for i in range (self.initx - 2):
            for j in range (self.inity, 2, -1):
                piece1 = self.getPieceGivenXY(i, j)
                piece2 = self.getPieceGivenXY(i + 1, j - 1)
                piece3 = self.getPieceGivenXY(i + 2, j - 2)
                piece4 = self.getPieceGivenXY(i + 3, j - 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    return True

        return False

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
        YELLOW = (255,255,0)
        self.backColor = BLUE
        if (playertype == "C"):
            self.color = YELLOW
        else:
            self.color = RED
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

class screens:
    def __init__(self, fonttype, screen):
        self.button1xloc = 125
        self.button2xloc = 425
        self.buttonyloc = 450
        self.buttonlength = 100
        self.buttonwidth = 50
        self.fonttype = fonttype
        self.screen = screen
        self.labelxloc = 125
        self.label1yloc = 200
        self.label2yloc = 300
        self.xmiddlelocation = (self.button1xloc + self.button2xloc) / 2

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def screenmaking(self,label1, label2, screencolor, fontcolor, fontcolortxt, button1label, button2label, value):
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        BLACK=(0,0,0)

        end_it = False
        while (end_it==False):
            self.screen.fill(screencolor)
            myfont = pygame.font.SysFont(self.fonttype, 40)
            nlabel = myfont.render(label1, 1, fontcolor)
            hlabel = myfont.render(label2, 2, fontcolor)
            end_it = self.button(fontcolortxt, button1label, button2label, value)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    end_it=True
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.blit(nlabel,(self.labelxloc,self.label1yloc))
            self.screen.blit(hlabel,(self.labelxloc,self.label2yloc))
            pygame.display.flip()

    def button(self, fontcolortxt, button1label, button2label, value):
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        BLACK=(0,0,0)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (value == 'no'):
            if (self.xmiddlelocation + self.buttonlength > mouse[0] > self.xmiddlelocation and self.buttonyloc + self.buttonwidth > mouse[1] > self.buttonyloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.xmiddlelocation, self.buttonyloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return(True)
            else:
                pygame.draw.rect(self.screen, RED, (self.xmiddlelocation, self.buttonyloc,self.buttonlength,self.buttonwidth))
            smallfont=pygame.font.SysFont(self.fonttype, 20)
            textSurf, textRect = self.text_objects(button1label, smallfont, fontcolortxt)
            textRect.center = ( ((self.xmiddlelocation)+(self.buttonlength/2))) , (self.buttonyloc+(self.buttonwidth/2))
            self.screen.blit(textSurf, textRect)
        if (value == 'yes'):
            if (self.button1xloc + self.buttonlength > mouse[0] > self.button1xloc and self.buttonyloc + self.buttonwidth > mouse[1] > self.buttonyloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button1xloc, self.buttonyloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return(False)
            else:
                pygame.draw.rect(self.screen, RED, (self.button1xloc, self.buttonyloc,self.buttonlength,self.buttonwidth))
            smallfont=pygame.font.SysFont(self.fonttype, 20)
            textSurf, textRect = self.text_objects(button1label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button1xloc)+(self.buttonlength/2))) , (self.buttonyloc+(self.buttonwidth/2))
            self.screen.blit(textSurf, textRect)

            if (self.button2xloc + self.buttonlength > mouse[0] > self.button2xloc and self.buttonyloc + self.buttonwidth > mouse[1] > self.buttonyloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button2xloc, self.buttonyloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return(True)
            else:
                pygame.draw.rect(self.screen, RED, (self.button2xloc, self.buttonyloc,self.buttonlength,self.buttonwidth))
            textSurf, textRect = self.text_objects(button2label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button2xloc+(self.buttonlength/2))) , (self.buttonyloc+(self.buttonwidth/2)))
            self.screen.blit(textSurf, textRect)
        return(False)
