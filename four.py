

import pygame
import classes

# Define some colors

pygame.init()

# Set the width and height of the screen [width, height]
size = (600, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
# Used to manage how fast the screen updates
#clock = pygame.time.Clock()

# -------- Main Program Loop -----------
MyGrid = classes.Grid(screen)
done = False
MyGrid.drawgrid()
pygame.display.flip()

while not done:
    # --- Main event loop
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
