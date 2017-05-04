
##################################################################################################################################
#       Project Name:   Connect Four
#       Developers:     Ariel Khatchatourian, Jacob Croes, Ben Winston, Greg Barton
#       Date Finished:  5/2/2017
#       Objective:      Create a connect four game that allows the user to chose whether they will play against another person
#                       or a computer.  It keeps track of the history of winnings.  The player must get four in a row to win
#                       the game.  In order to move the pieces, the user must use the left and right arrow.  To drop the piece
#                       the user must press the down arrow.
##################################################################################################################################

import pygame
import classes

# initializes the game in python
pygame.init()

size = (700, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Connect Four")

BLACK=(0,0,0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHTRED = (100,0,0)
YELLOW = (255,255,0)
end_it=False


def main():
    Difficulty = 1
    #creates the first two screens that the user will see
    x = classes.screens("Times New Roman", screen)
    x.screenmaking("Welcome to Connect Four!!", "Click the button to continue", BLUE, RED, BLACK, "Continue!","nothing", 'no')
    returnvalue = x.screenmaking("Choose 1 or 2 Players", "", BLUE, RED, BLACK,"One Player", "Two Player", 'yes')

    #if the user returns one player it gives then the option of an easy or hard mode and returns a value accordingly
    if (returnvalue == 'OnePlayer'):
        returnvalue = x.screenmaking("Choose difficulty" , "", BLUE ,RED ,BLACK , "Easy", "Hard", 'difficult')
        if(returnvalue == 'Easy'):
            Difficulty = 1
        else:
            Difficulty = 2
        MyGrid = classes.Grid(screen, Difficulty)
    else:
        MyGrid = classes.Grid(screen, Difficulty, 'twoplayer')


    done = False
    MyGrid.drawgrid()
    pygame.display.flip()

    while not done:
        #continues to display the game until the user quits out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                #if the user presses the right, left or down arrow key it specifies a move right, left or dropping it respectively
                if event.key == pygame.K_LEFT:
                    MyGrid.MoveMovingPiece('L')
                    pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    MyGrid.MoveMovingPiece('R')
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    MyGrid.MoveMovingPiece('D')
                    pygame.display.flip()

    pygame.quit()

main()
