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
    x.screenmaking("Choose 1 or 2 Players", "Press the down arrow to continue", BLUE, RED, BLACK,"One Player", "Two Player", 'yes')

    MyGrid = classes.Grid(screen)
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
