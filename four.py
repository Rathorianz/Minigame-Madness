
##################################################################################################################################
#       Project Name:   Connect Four
#       Developers:     Ariel Khatchatourian, Jacob Croes, Ben Winston, Greg Barton
#       Date Finished:  5/2/2017
#       Objective:      Create a connect four game that allows the user to chose whether they will play against another person
#                       or a computer.  It keeps track of the history of winnings.  The player must get four in a row to win
#                       the game.
##################################################################################################################################

import pygame
import classes

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
    x = classes.screens("Times New Roman", screen)
    x.screenmaking("Welcome to Connect Four!!", "Click the button to continue", BLUE, RED, BLACK, "Continue!","nothing", 'no')
    returnvalue = x.screenmaking("Choose 1 or 2 Players", "", BLUE, RED, BLACK,"One Player", "Two Player", 'yes')
    if (returnvalue == 'OnePlayer'):
        MyGrid = classes.Grid(screen)
    else:
        MyGrid = classes.Grid(screen, 'twoplayer')

    done = False
    MyGrid.drawgrid()
    pygame.display.flip()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
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
