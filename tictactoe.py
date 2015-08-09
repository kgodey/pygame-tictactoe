import pygame, sys
from pygame.locals import QUIT, MOUSEBUTTONUP

from lib import Board


pygame.init()
clock = pygame.time.Clock()
board = Board(4, 150, 50, 10)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            x, y = event.pos
            box = board.get_box_at_pixel(x, y)
            if box is not None:
                board.play_turn(box)
                board.check_for_winner()

    pygame.display.update()
    clock.tick(30)
