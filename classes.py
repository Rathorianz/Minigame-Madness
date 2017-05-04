import math
import pygame
import random
import json
import os

class Grid:
    ##################################################################################################################################
    #       Developer:      Ariel Khatchatourian and Jacob Croes
    #       Date Finished:  5/2/2017
    #       Definition:     The objective of this class is to create the grid for the connect four game
    #                       The class includes one player and two player modes
    ##################################################################################################################################

    def __init__(self, screen, playermode = 'oneplayer', startingplayer = 'U', initx = 7, inity = 6, initwidth = 75):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Initializes the game and calls NewGame
        #####################################################################################
        self.NewGame(screen, playermode, startingplayer, initx, inity, initwidth)

    def GetXLocation(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Find the x value of where the piece should be placed in terms
        #                       of the actual pixal location
        #####################################################################################
        returnValue = self.xOffset+ (self.gridLineWidth*(self.MovingPiecePosition) +(self.initwidth * self.MovingPiecePosition))
        return returnValue

    def GetXGridLocation(self,x):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Finds the x location of where the piece is located in the grid
        #                       not the actual pixel location.  The x locations are labeled 1
        #                       through the number of spaces which in this case is
        #####################################################################################
        returnValue = self.xOffset+ (self.gridLineWidth*(x) +(self.initwidth * x))
        return returnValue

    def GetYGridLocation(self,y):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Finds the y location of where the piece is located in the grid
        #                       not the actual pixel location.  The y locations are labeled 1
        #                       through the number of spaces which in this case is 6
        #####################################################################################
        returnValue = self.boardYOffset+(self.gridLineWidth*(self.inity - y) +(self.initwidth * (self.inity - y)))
        return returnValue

    def startGame(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Starts the game by setting the currentMovingPiece to be zero
        #                       (the first one) and fills the screen with the color given
        #####################################################################################
        self.screen.fill(self.color)
        self.currentMovingPiece = 0
        self.continueGame()

    def continueGame(self, center = 'no'):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Continues the game for the user if no one has won.  It also
        #                       removes the piece if it is in the center and it should not be.
        #####################################################################################
        if (center == 'yes'):
            self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())
            self.MovingPiecePosition = (self.initx//2)+1
        self.pieces[self.currentMovingPiece].drawMoving(self.screen, self.yOffset ,self.GetXLocation())

    def MoveMovingPiece(self,direction, center = 'no'):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     This function moves the pieces according to the button pressed
        #                       by the user.  If the direction is L or R then the function calls
        #                       the function to remove the piece from where it is and repaint
        #                       it where the user wants it to be.  If the user drops the piece,
        #                       the drops the piece and changes changes the current player.
        #                       If the player is the computer it calls the functions to make an
        #                       intelligent move.
        #####################################################################################
        BLACK=(0,0,0)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        YELLOW = (255,255,0)
        # L for left,  R for right and D for down.
        if (self.validateMove(direction) == True):

            if (direction == 'L' or direction == 'R'):
                self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())
                if (center == 'yes'):
                    self.MovingPiecePosition = (self.initx//2)+1

                if (direction == 'L'):
                    self.MovingPiecePosition-=1
                if (direction == 'R'):
                    self.MovingPiecePosition+=1
                self.continueGame()

            if (direction == 'D'):
                if (self.checkNewAvailableSquare(self.MovingPiecePosition) != -1):
                    xcheck = self.MovingPiecePosition
                    ycheck = self.checkNewAvailableSquare(self.MovingPiecePosition)
                    if (self.getPieceGivenXY(xcheck,ycheck) == ''):
                        self.pieces[self.currentMovingPiece].y = ycheck
                        self.pieces[self.currentMovingPiece].x = xcheck

                    else:
                        print("Problem")

                    if (self.currentMovingPiece < (self.initx * self.inity) - 1):
                        self.currentMovingPiece += 1
                        self.continueGame(center)
                        self.drawgrid()
                    else:
                        self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())
                        self.drawgrid()
                        self.displaywinningmessage('no')

                    if (self.didPlayerWin() == True):
                        self.displaywinningmessage('yes')

                    if (self.playermode == 1 and self.currentplayer == 'U'):
                        X = self.IntelligentMove()
                        if (X == -1):
                            X = self.RandomMove()

                        self.MovetoPosition(X)
                        self.currentplayer = 'U'
                    else:
                        if (self.currentplayer == 'U'):
                            self.currentplayer = 'C'
                        else:
                            self.currentplayer = 'U'

                else:
                    print("no move")

    def IntelligentMove(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Places in order the kinds of moves that the computer should go
        #                       through when making a move.  It goes through the four conditions
        #                       in a specific order and executes the first one that is possible.
        #####################################################################################

        #condition 1 is if the computer can win it will place the piece there
        x = self.CanWin('C')
        if (x != -1):
            return x

        #condition 2 is if the user can win it will place the piece there and block them
        x = self.CanWin('U')
        if (x != -1):
            return x

        #condition 3 is if the user has 2 pieces in a row it will place a piece on one side of it
        #to block them from making 3 in a row
        x = self.CanImproveWin('U')
        if (x != -1):
            return x

        #condition 4 is if the user has 2 pieces in a row it will place a piece on one side of it
        #to make 3 in a row
        x = self.CanImproveWin('C')
        if (x != -1):
            return x

        return -1

    def CanImproveWin(self, usertype):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to order the rules defined below to give priority
        #                       with diagonal having the highest  prefreance followed by
        #                       horizontal and vertical
        #####################################################################################
        x = self.CanImproveWinDiagnoally(usertype)
        if (x != -1):
            return x

        x = self.CanImproveWinHorizontally(usertype)
        if (x != -1):
            return x

        x = self.CanImproveWinVertically(usertype)
        if (x != -1):
            return x

        return -1

    def CanImproveWinHorizontally(self, usertype):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check for three in a row horizontally where
        #                       there is two in a row or one piece with a gap and then another
        #                       piece
        #####################################################################################
        for i in range (self.inity):
            for j in range (1, self.initx-1):

                x = self.CheckTwoPossiblePieces(usertype, j, i, j+1,i , j-1, i , j+2 , i)
                if (x != -1):
                    return x

                x = self.CheckTwoPossiblePieces(usertype, j-1, i, j+1,i , j, i , j , i  )
                if (x != -1):
                    return x

        return -1

    def CheckTwoPossiblePieces(self,usertype, x1,y1,x2,y2,p1,p2,p3,p4):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check if the pieces next to eachother or the
        #                       pieces with the gap in between are the same color
        #####################################################################################
        piece1 = self.getPieceGivenXY(x1, y1)
        piece2 = self.getPieceGivenXY(x2, y2)

        if self.checkforpossibleimprovewinning(piece1, piece2, usertype) == True:
            x = self.IsPlayable(p1,p2, p3, p4)
            if (x != -1):
                return x

        return -1

    def CanImproveWinVertically(self, usertype):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check for two in a row vertically. And if true
        #                       adds the piece on top
        #####################################################################################
        for i in range (self.inity-2):
            for j in range (self.initx):
                x = self.CheckTwoPossiblePieces(usertype, j, i, j, i+1, j, i+2, j, i+2)
                if (x != -1):
                    return x

        return -1

    def CanImproveWinDiagnoally(self, usertype):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check for possible diagonals of three in a row
        #                       either where there is two in a row or one piece with a gap and
        #                       then another piece. It uses bounds too check for impossible cases
        #                       and to not execute if the bounds are not met
        #####################################################################################
        for i in range(self.inity):
            for j in range(self.initx):

                if (j-2 >= 0 and i-2>= 0):
                    x = self.CheckTwoPossiblePieces(usertype, j-2, i-2, j-1, i-1, j, i, j, i)
                    if (x != -1):
                        return x

                if (j+2 < self.initx and i-2 >=0):
                    x = self.CheckTwoPossiblePieces(usertype, j+2, i-2, j+1, i-1, j, i, j, i)
                    if (x != -1):
                        return x

                if (j+2 <self.initx and i+2 < self.inity):
                    x = self.CheckTwoPossiblePieces(usertype, j+2, i+2, j+1, i+1, j, i, j, i)
                    if (x != -1):
                        return x

                if (j-2 >= 0 and i+2 < self.inity):
                    x = self.CheckTwoPossiblePieces(usertype, j-2, i+2, j-1, i+1, j, i, j, i)
                    if (x != -1):
                        return x

                if (j-1 >=0 and i-1 >=0 and j+1 < self.initx and i+1< self.inity):
                    x = self.CheckTwoPossiblePieces(usertype, j-1, i-1, j+1, i+1, j, i, j, i)
                    if (x != -1):
                        return x

                if (j-1 >=0 and i+1 <self.inity and j+1 < self.initx and i-1 >=0):
                    x = self.CheckTwoPossiblePieces(usertype, j-1, i+1, j+1, i-1, j, i, j, i)
                    if (x != -1):
                        return x

        return -1

    def checkforpossibleimprovewinning(self,piece1,piece2, usertype):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:
        #####################################################################################
        if (piece1 != "" and  piece2 != "" and piece1.color == piece2.color  and piece1.playertype == piece2.playertype == usertype):
            return True

        else:
            return False

    def IsPlayable(self, x1, y1, x2, y2):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check the bounds
        #####################################################################################
        x = self.IsPlayablePiece(x1, y1)
        if (x != -1):
            return x

        x = self.IsPlayablePiece(x2, y2)
        if (x != -1):
            return x

        return -1

    def IsPlayablePiece(self, x, y):
        #####################################################################################
        #       Developer:      Jacob Croes
        #       Definition:     This is used to check the bounds
        #####################################################################################
        if (x > 0 and x <= self.initx and y >= 0 and y <= self.inity):
            if (self.getPieceGivenXY(x,y) == ""):
                if (self.getPieceGivenXY(x ,y-1) != "" or y==0):
                    return x

        return -1

    def CanWin(self, usertype):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the user or computer can win.  The usertype
        #                       is needed to see what pieces it should be checking.
        #####################################################################################
        x = self.CanWinHorizontally(usertype)
        if (x != -1):
            return x

        x = self.CanWinVertically(usertype)
        if (x != -1):
            return x

        x = self.CanWinDiagnoally(usertype)
        if (x != -1):
            return x

        return -1

    def CanWinHorizontally(self, usertype):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if there is three pieces with the same user type
        #                       in a row horizontally.  If so it will return the x value to
        #                       complete the three or block the user.
        #####################################################################################
        for i in range (self.inity):
            for j in range (1, self.initx-2):

                x = self.CheckPossiblePieces(usertype, j, i, j+1,i , j+2, i, j-1, i, j+3, i)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, j, i, j+1,i , j+3, i, j+2, i, j+2, i)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, j, i, j+2,i , j+3, i, j+1, i, j+1, i)
                if (x != -1):
                    return x

        return -1

    def CheckPossiblePieces(self,usertype, x1,y1,x2,y2,x3,y3,p1,p2,p3,p4):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Given the  and y coordinates it checks to see what piece is in
        #                       that place and then sends the pieces to the next function
        #####################################################################################
        piece1 = self.getPieceGivenXY(x1, y1)
        piece2 = self.getPieceGivenXY(x2, y2)
        piece3 = self.getPieceGivenXY(x3, y3)

        if self.checkforpossiblewinning(piece1, piece2, piece3, usertype) == True:
            x = self.IsPlayable(p1,p2, p3, p4)
            if (x != -1):
                return x

        return -1

    def CanWinVertically(self, usertype):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if there is three pieces with the same user type
        #                       in a row vertically.  If so it will return the x value to
        #                       complete the three or block the user.
        #####################################################################################
        for i in range (1, self.initx + 1):
            for j in range (self.inity - 3):
                x = self.CheckPossiblePieces(usertype, i, j, i, j+1, i, j+2, i, j+3, i, j+3)
                if (x != -1):
                    return x

        return -1

    def CanWinDiagnoally(self, usertype):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if there is three pieces with the same user type
        #                       in a row diagonally.  If so it will return the x value to
        #                       complete the three or block the user.
        #####################################################################################
        for i in range (self.inity ):
            for j in range (1, self.initx):

                x = self.CheckPossiblePieces(usertype, j, i, j+1, i+1, j+2, i+2, j-1, i-1, j+3, i+3)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, j, i, j+1, i+1, j+3, i+3, j+2, i+2, j+2, i+2)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, j, i, j+2, i+2, j+3, i+3, j+1, i+1, j+1, i+1)
                if (x != -1):
                    return x

        for i in range (1, self.initx):
            for j in range (self.inity, 0, -1):

                x = self.CheckPossiblePieces(usertype, i, j, i+1, j-1, i+2, j-2, i-1, j+1, i+3, j-3)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, i, j, i+2, j-2, i+3, j-3, i+1, j-1, i+1, j-1)
                if (x != -1):
                    return x

                x = self.CheckPossiblePieces(usertype, i, j, i+1, j-1, i+3, j-3, i+2, j-2, i+2, j-2)
                if (x != -1):
                    return x

        return -1

    def checkforpossiblewinning(self,piece1,piece2,piece3, usertype):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the player or computer as three pieces
        #                       in a row and can win on the newxt turn.
        #####################################################################################
        if (piece1 != "" and  piece2 != "" and  piece3 != "" and piece1.color == piece2.color == piece3.color and piece1.playertype == piece2.playertype == piece3.playertype == usertype):

            return True
        else:
            return False

    def IsPlayable(self, x1, y1, x2, y2):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if option on either side of the three in a row
        #                       is a payable move.
        #####################################################################################
        x = self.IsPlayablePiece(x1, y1)
        if (x != -1):
            return x

        x = self.IsPlayablePiece(x2, y2)
        if (x != -1):
            return x

        return -1

    def IsPlayablePiece(self, x, y):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the coordinate given is in the grid and
        #                       if there is a piece below it or not.
        #####################################################################################
        if (x > 0 and x <= self.initx and y >= 0 and y <= self.inity):
            if (self.getPieceGivenXY(x,y) == ""):
                if (self.getPieceGivenXY(x ,y-1) != "" or y==0):
                    return x

        return -1

    def displaywinningmessage(self,win):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Depending on if someone has won and who it was it displays a
        #                       message on the next screen that comes up accordingly.
        #                       It also adds to the JSON file who has won the game and stores it.
        #####################################################################################
        BLACK=(0,0,0)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        YELLOW = (255,255,0)
        myfile = file('connectfour.json')
        if(win == 'yes'):
            if (self.playermode == 1):
                if(self.currentplayer == 'U'):
                    winningmessage = 'Congrats you won!!!'
                    myfile.writeJSONfile('P1')

                else:
                    winningmessage = 'You Lost!!!'
                    myfile.writeJSONfile('C')

            else:
                if (self.currentplayer == 'U'):
                    winningmessage = 'Player 1 won!!!'
                    myfile.writeJSONfile('P1')
                else:
                    winningmessage = 'Player 2 won!!!'
                    myfile.writeJSONfile('P2')

        else:
            winningmessage = 'Tie!'
            myfile.writeJSONfile('T')

        self.drawgrid()
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        BLACK=(0,0,0)
        x = screens("Times New Roman", self.screen)
        returnvalue = x.screenmaking(winningmessage, "", BLUE, RED, BLACK, "Winning History","Start Over", 'history', 'history')
        if (returnvalue == 'history'):

            historymessage = myfile.readJSONfile()
            y = screens("Times New Roman", self.screen)
            returnvalue = y.screenmaking(historymessage[0], historymessage[1], BLUE, RED, BLACK, "Start Over","mean nothing", 'no', 'history', historymessage[2], historymessage[3])

        if (returnvalue == 'restart'):
            z = screens("Times New Roman", self.screen)
            returnvalue = z.screenmaking("Choose 1 or 2 Players", "", BLUE, RED, BLACK,"One Player", "Two Player", 'yes')
            if (returnvalue == 'OnePlayer'):
                self.NewGame(self.screen)
            else:
                self.NewGame(self.screen, 'twoplayer')
            self.drawgrid()
            pygame.display.flip()

    def NewGame(self, screen, playermode = 'oneplayer', startingplayer = 'C', initx = 7, inity = 6, initwidth = 75):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Starts a new game and sets all of the attributes of the class.
        #                       It also initializes the pieces and makes them prior to the game
        #                       beginning.
        #####################################################################################
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
        self.currentplayer = 0
        self.startingplayer = startingplayer
        if (playermode == 'oneplayer'):
            self.playermode = 1
        else:
            self.playermode = 2

        if (self.startingplayer == 'U'):
            self.secondplayer = 'C'
        else:
            self.secondplayer = 'U'

        self.currentplayer = self.startingplayer
        self.pieces = []
        self.pieces.clear()

        for i in range (self.initx * self.inity):
            if (i%2==0):
                self.pieces.append(Piece(self.startingplayer,self.initwidth))
            else:
                self.pieces.append(Piece(self.secondplayer,self.initwidth))

        self.startGame()

    def MovetoPosition(self, X):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     When given an x position it moves the piece for the computer
        #####################################################################################
        erasepiece = 'yes'
        self.pieces[self.currentMovingPiece].RemoveMe(self.screen, self.yOffset ,self.GetXLocation())
        self.MovingPiecePosition = (self.initx//2)+1

        if (X > 4):
            value = X - 4
            for i in range (value):
                self.delay()
                self.MoveMovingPiece('R', erasepiece)
                erasepiece = 'no'

        if(X < 4):
            value = 4-X
            for i in range (value):
                self.delay()
                self.MoveMovingPiece('L', erasepiece)
                erasepiece = 'no'

        self.currentplayer = 'C'
        self.delay()
        self.MoveMovingPiece('D', 'yes')
        self.delay()

    def delay(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     delays the move of the computer by 500 milliseconds
        #                       so that the user can see the computer moving
        #####################################################################################
        pygame.display.flip()
        pygame.time.delay(500)

    def RandomMove(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Performs a random move for the computer if there is no
        #                       better move.
        #####################################################################################
        found = False
        while (found == False):
            X = random.randrange(1,self.initx)
            for i in range (1, self.inity):
                if (self.getPieceGivenXY(X, i) == ""):
                    if (i == self.inity - 1):
                        found = True
                        return X

    def didPlayerWin(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Returns true if the player won either horizontally,
        #                       vertically, or diagonally.
        #####################################################################################
        if(self.didPlayerWinHorizontally() == True or self.didPlayerWinVertically() == True or self.didPlayerWinDiagonally() == True):
            return True

    def getPieceGivenXY(self,x,y):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Finds if there is a piece in the spot given the x and y coordinates
        #####################################################################################
        for i in range (self.initx * self.inity):
            if (self.pieces[i].x == x and self.pieces[i].y == y):
                return self.pieces[i]

        return ""

    def didPlayerWinHorizontally(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the player has won horizontally with
        #                       four pieces in a row.
        #####################################################################################
        for i in range (self.inity):
            for j in range (self.initx - 2):
                piece1 = self.getPieceGivenXY(j, i)
                piece2 = self.getPieceGivenXY(j + 1, i)
                piece3 = self.getPieceGivenXY(j + 2, i)
                piece4 = self.getPieceGivenXY(j + 3, i)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    self.paintwinningpieces(j, i, j+1, i, j+2, i, j+3, i)
                    return True

        return False

    def didPlayerWinVertically(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the player has won vertically with
        #                       four pieces in a row.
        #####################################################################################
        for i in range (self.initx + 1):
            for j in range (self.inity - 3):
                piece1 = self.getPieceGivenXY(i, j)
                piece2 = self.getPieceGivenXY(i, j + 1)
                piece3 = self.getPieceGivenXY(i, j + 2)
                piece4 = self.getPieceGivenXY(i, j + 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    self.paintwinningpieces(i, j, i, j+1, i, j+2, i, j+3)
                    return True

        return False

    def SetPieceColorGivenXY(self,x,y, color):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Colors the piece given by the x and y coordinate and the color
        #                       to change it to
        #####################################################################################
        BLACK=(0,0,0)
        BLUE = (0, 0, 255)

        for i in range (self.initx * self.inity):
            if (self.pieces[i].x == x and self.pieces[i].y == y):
                self.pieces[i].SetColor(color)

    def paintwinningpieces(self, x1,y1,x2,y2,x3,y3,x4,y4):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Makes the winning pieces blink back and forth between blue
        #                       and black 6 times.
        #####################################################################################
        BLACK=(0,0,0)
        BLUE = (0, 0, 255)
        value = True
        color = BLACK
        accum = 0
        while (accum <= 6):
            if (color == BLACK):
                color = BLUE
            else:
                color = BLACK
            self.SetPieceColorGivenXY(x1, y1, color)
            self.SetPieceColorGivenXY(x2, y2, color)
            self.SetPieceColorGivenXY(x3, y3, color)
            self.SetPieceColorGivenXY(x4, y4, color)
            self.drawgrid()
            pygame.display.flip()
            pygame.time.delay(500)
            accum += 1

    def checkforwinning(self,piece1, piece2, piece3, piece4):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if a player has won the game either vertially,
        #                       horiontally, or diagonally
        #####################################################################################
        BLACK=(0,0,0)

        if (piece1 != "" and  piece2 != "" and  piece3 != "" and piece4 != "" and piece1.color == piece2.color == piece3.color == piece4.color):
            return True
        else:
            return False

    def didPlayerWinDiagonally(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks to see if the player has won horizontally with
        #                       four pieces in a row.
        #####################################################################################
        for i in range (self.inity - 2):
            for j in range (self.initx - 2):
                piece1 = self.getPieceGivenXY(j, i)
                piece2 = self.getPieceGivenXY(j + 1, i + 1)
                piece3 = self.getPieceGivenXY(j + 2, i + 2)
                piece4 = self.getPieceGivenXY(j + 3, i + 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    self.paintwinningpieces(j, i, j+1, i+1, j+2, i+2, j+3, i+3)

                    return True

        for i in range (self.initx - 2):
            for j in range (self.inity, 2, -1):
                piece1 = self.getPieceGivenXY(i, j)
                piece2 = self.getPieceGivenXY(i + 1, j - 1)
                piece3 = self.getPieceGivenXY(i + 2, j - 2)
                piece4 = self.getPieceGivenXY(i + 3, j - 3)
                if self.checkforwinning(piece1, piece2, piece3, piece4) == True:
                    self.paintwinningpieces(i, j, i+1, j-1, i+2, j-2, i+3, j-3)

                    return True

        return False

    def checkNewAvailableSquare(self,x):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Checks the next square that the piece can go into once dropped.
        #####################################################################################
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
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Validates that if the user pushes the right or left key that
        #                       they will actually be allowed to move the pice in that direction
        #                       and it will not go off the grid
        #####################################################################################
        if (direction == 'L'):
            if (self.MovingPiecePosition <=1):
                return False

        if (direction == 'R'):
            if (self.MovingPiecePosition >=self.initx):
                return False

        if (direction == 'D'):
            return True

        return True

    def drawpieces(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     draws all of the pieces before starting the game and sets
        #                       their position to be -1 -1 so that they are not displayed on
        #                       the screen
        #####################################################################################
        for i in range (self.initx * self.inity):
            if (self.pieces[i].x != -1 and self.pieces[i].y != -1):
                self.pieces[i].drawObject(self.screen,self.GetXGridLocation(self.pieces[i].x),self.GetYGridLocation(self.pieces[i].y))

    def drawgrid(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Draws the 6 by 7 grid on the screen in the color white.
        #####################################################################################
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

class Piece:
    ##################################################################################################################################
    #       Developer:      Ariel Khatchatourian
    #       Date Finished:  5/2/2017
    #       Definition:     The objective of this class is to create the pieces that will be used for the game.  The cals can set a color
    #                       and draws and removes the piece when it is moved around.  It also stores the position of the piece once
    #                       it is placed.
    ##################################################################################################################################
    def __init__(self, playertype,diameter, x=-1, y=-1):
        self.x = x
        self.y = y
        GREEN = (0,255 , 0)
        BLUE = (0, 0, 255)
        RED = (255,0,0)
        YELLOW = (255,255,0)
        self.backColor = BLUE
        self.playertype = playertype
        if (playertype == "C"):
            self.color = YELLOW
        else:
            self.color = RED
        self.diameter = diameter -2

    def SetColor(self, color):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Sets the color of the piece
        #####################################################################################
        self.color = color

    def drawObject(self,screen,rect_x,rect_y):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     As long as the piece is on the board, it will redraw each
        #                       piece every turn
        #####################################################################################
        if (self.x != -1 and self.y != -1):
            pygame.draw.circle(screen, self.color, [rect_x+self.diameter//2, rect_y],(self.diameter-10)//2)

    def drawMoving(self,screen,rectY,rectX):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Draws the piece above the grid for the user to move right
        #                       and left.
        #####################################################################################
        pygame.draw.circle(screen, self.color, [rectX+self.diameter//2, rectY] ,((self.diameter-10)//2))

    def RemoveMe(self,screen,rectY,rectX):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Paints over where the piece originally was with the background
        #                       color.
        #####################################################################################
        pygame.draw.circle(screen, self.backColor, [rectX+self.diameter//2, rectY] ,((self.diameter-10)//2))

class screens:
    ##################################################################################################################################
    #       Developer:      Ariel Khatchatourian
    #       Date Finished:  5/2/2017
    #       Definition:     The objective of this class is to create different screens for the user to see with different captions
    #                       and instructions for the user to follow.  It also displays buttons on the screen that the user can click
    #                       to go to different screens.
    ##################################################################################################################################
    def __init__(self, fonttype, screen):
        self.button1xloc = 125
        self.button2xloc = 425
        self.button1yloc = 450
        self.button2yloc = 300
        self.buttonlength = 100
        self.buttonwidth = 50
        self.fonttype = fonttype
        self.screen = screen
        self.labelxloc = 125
        self.label1yloc = 150
        self.label2yloc = 200
        self.label3yloc = 250
        self.label4yloc = 300
        self.historybuttony = self.button2yloc + 50
        self.xmiddlelocation = (self.button1xloc + self.button2xloc) / 2

    def text_objects(self, text, font, color):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Places texts onto the buttons that display to the user.
        #####################################################################################
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def screenmaking(self,label1, label2, screencolor, fontcolor, fontcolortxt, button1label, button2label, value, method='button', label3 = "", label4 = ""):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Constructs different screens depending on the texts given to
        #                       the user and how many buttons specified.
        #####################################################################################
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        BLACK=(0,0,0)
        end_it = False
        while (end_it==False):
            self.screen.fill(screencolor)
            myfont = pygame.font.SysFont(self.fonttype, 40)
            nlabel = myfont.render(label1, 1, fontcolor)
            hlabel = myfont.render(label2, 2, fontcolor)
            ilabel = myfont.render(label3, 3, fontcolor)
            jlabel = myfont.render(label4, 4, fontcolor)
            end_it = self.button(fontcolortxt, button1label, button2label, value, method)

            #if end_it is not False an action needs to take place
            if (not(end_it == False or end_it == True)):
                return end_it

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    end_it=True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.blit(nlabel,(self.labelxloc,self.label1yloc))
            self.screen.blit(hlabel,(self.labelxloc,self.label2yloc))
            self.screen.blit(ilabel,(self.labelxloc,self.label3yloc))
            self.screen.blit(jlabel,(self.labelxloc,self.label4yloc))
            pygame.display.flip()

    def button(self, fontcolortxt, button1label, button2label, value, method = 'button'):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Cretes buttons to be placed on the screen.  The number of
        #                       buttons on the screen depends on how many is specified and
        #                       it also allows the user to click the button and return a
        #                       certain value depending on what screen the user is on.
        #####################################################################################
        RED = (255, 0, 0)
        LIGHTRED = (100,0,0)
        BLACK=(0,0,0)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (value == 'no'):
            if (self.xmiddlelocation + self.buttonlength > mouse[0] > self.xmiddlelocation and self.button1yloc + self.buttonwidth > mouse[1] > self.button1yloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.xmiddlelocation, self.button1yloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    if (method == 'history'):
                        return('restart')
                    else:
                        return(True)
            else:
                pygame.draw.rect(self.screen, RED, (self.xmiddlelocation, self.button1yloc,self.buttonlength,self.buttonwidth))
            smallfont=pygame.font.SysFont(self.fonttype, 20)
            textSurf, textRect = self.text_objects(button1label, smallfont, fontcolortxt)
            textRect.center = ( ((self.xmiddlelocation)+(self.buttonlength/2))) , (self.button1yloc+(self.buttonwidth/2))
            self.screen.blit(textSurf, textRect)

        if (value == 'yes'):
            if (self.button1xloc + self.buttonlength > mouse[0] > self.button1xloc and self.button2yloc + self.buttonwidth > mouse[1] > self.button2yloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button1xloc, self.button2yloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    if (method == 'button'):
                        return('OnePlayer')
                    else:
                        return('restart')
            else:
                pygame.draw.rect(self.screen, RED, (self.button1xloc, self.button2yloc,self.buttonlength,self.buttonwidth))
            smallfont=pygame.font.SysFont(self.fonttype, 20)
            textSurf, textRect = self.text_objects(button1label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button1xloc)+(self.buttonlength/2))) , (self.button2yloc+(self.buttonwidth/2))
            self.screen.blit(textSurf, textRect)

            if (self.button2xloc + self.buttonlength > mouse[0] > self.button2xloc and self.button2yloc + self.buttonwidth > mouse[1] > self.button2yloc):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button2xloc, self.button2yloc,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return('TwoPlayer')
            else:
                pygame.draw.rect(self.screen, RED, (self.button2xloc, self.button2yloc,self.buttonlength,self.buttonwidth))
            textSurf, textRect = self.text_objects(button2label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button2xloc+(self.buttonlength/2))) , (self.button2yloc+(self.buttonwidth/2)))
            self.screen.blit(textSurf, textRect)

        if (value == 'history'):
            if (self.button1xloc + self.buttonlength > mouse[0] > self.button1xloc and self.historybuttony + self.buttonwidth > mouse[1] > self.historybuttony):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button1xloc, self.historybuttony,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return('history')
            else:
                pygame.draw.rect(self.screen, RED, (self.button1xloc, self.historybuttony,self.buttonlength,self.buttonwidth))
            smallfont=pygame.font.SysFont(self.fonttype, 20)
            textSurf, textRect = self.text_objects(button1label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button1xloc)+(self.buttonlength/2))) , (self.historybuttony+(self.buttonwidth/2))
            self.screen.blit(textSurf, textRect)

            if (self.button2xloc + self.buttonlength > mouse[0] > self.button2xloc and self.historybuttony + self.buttonwidth > mouse[1] > self.historybuttony):
                pygame.draw.rect(self.screen, LIGHTRED, (self.button2xloc, self.historybuttony,self.buttonlength,self.buttonwidth))
                if (click[0] == 1):
                    return('restart')
            else:
                pygame.draw.rect(self.screen, RED, (self.button2xloc, self.historybuttony,self.buttonlength,self.buttonwidth))
            textSurf, textRect = self.text_objects(button2label, smallfont, fontcolortxt)
            textRect.center = ( ((self.button2xloc+(self.buttonlength/2))) , (self.historybuttony+(self.buttonwidth/2)))
            self.screen.blit(textSurf, textRect)

        return(False)

class file:
    ##################################################################################################################################
    #       Developer:      Ariel Khatchatourian
    #       Date Finished:  5/2/2017
    #       Definition:     This class writes to a JSON file and records the winning history of the player
    ##################################################################################################################################
    def __init__(self, filename):
        self.filename = filename

    def readfromfile(self,user, message):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Opens up the file and reads it.
        #####################################################################################
        open(filename, 'r')

    def writefile(self, text):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Writes certain text into a file.
        #####################################################################################
        outfile = open(self.filename, "a+")
        outfile.write(text)
        outfile.write("\r\n")
        outfile.close()

    def doesfileexist(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:    Checks to see if the file exists on the computer already
        #####################################################################################
        return os.path.exists(self.filename)

    def readJSONfile(self):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     If there is no file it writes a JSON file on the computer.
        #                       If one exists it updates the number of times that person
        #                       has won.
        #####################################################################################
        if (self.doesfileexist() == False):
            config = {'Player_1': 0 , 'Player_2' : 0, 'Computer': 0, 'No_Winner' : 0}
            with open(self.filename, 'w') as f:
                json.dump(config,f)

        with open (self.filename, 'r') as f:
            config = json.load(f)

        computerwins = config['Computer']
        player1wins = config['Player_1']
        player2wins = config['Player_2']
        Ties = config['No_Winner']

        returnvalue1 = []
        returnvalue1.append ("Player 1 has won " + str(player1wins) + " times.")
        returnvalue1.append ("Player 2 has won " + str(player2wins) + " times.")
        returnvalue1.append ("Computer has won " + str(computerwins) + " times.")
        returnvalue1.append ("There has been " + str(Ties) + " ties.")
        return returnvalue1

    def writeJSONfile(self, winner):
        #####################################################################################
        #       Developer:      Ariel Khatchatourian
        #       Definition:     Writes into the JSON file already made depending on who has
        #                       won the game, that is why the winner is needed when calling
        #                       this function.  It adds adds one to the player that has
        #                       won the game to keep track.
        #####################################################################################
        if (self.doesfileexist() == False):
            config = {'Player_1': 0 , 'Player_2' : 0, 'Computer': 0, 'No_Winner' : 0}
            with open(self.filename, 'w') as f:
                json.dump(config,f)

        with open (self.filename, 'r') as f:
            config = json.load(f)
        if (winner == 'C'):
            config['Computer'] = config['Computer'] + 1
        if (winner == 'P1'):
            config['Player_1'] = config['Player_1'] + 1
        if (winner == 'P2'):
            config['Player_2'] = config['Player_2'] + 1
        if (winner == 'T'):
            config['No_Winner'] = config['No_Winner'] + 1

        with open(self.filename, 'w') as f:
            json.dump(config,f)
