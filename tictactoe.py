import pygame, sys, itertools
from pygame.locals import *


FPS = 30

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Box(object):
    state = 0
    
    def __init__(self, x, y, size):
        self.size = size
        self.line_width = int(self.size / 40) if self.size > 40 else 1
        self.radius = (self.size / 2) - (self.size / 8)
        self.rect = pygame.Rect(x, y, size, size)
    
    def mark_x(self):
        pygame.draw.line(surface, RED, (self.rect.centerx - self.radius, self.rect.centery - self.radius), (self.rect.centerx + self.radius, self.rect.centery + self.radius), self.line_width)
        pygame.draw.line(surface, RED, (self.rect.centerx - self.radius, self.rect.centery + self.radius), (self.rect.centerx + self.radius, self.rect.centery - self.radius), self.line_width)
    
    def mark_o(self):
        pygame.draw.circle(surface, BLUE, (self.rect.centerx, self.rect.centery), self.radius, self.line_width)


class Board(object):
    turn = 1
    
    def __init__(self, grid_size=3, box_size=200, border=20, line_width=5):
        self.grid_size = grid_size
        self.box_size = box_size
        self.border = border
        self.line_width = line_width
        
    def setup(self):
        self.draw_lines()
        self.initialize_boxes()
        self.calculate_winners()
    
    def draw_lines(self):
        for i in xrange(1, self.grid_size):
            start_position = ((self.box_size * i) + (self.line_width * (i - 1))) + self.border
            width = surface.get_width() - (2 * self.border)
            pygame.draw.rect(surface, BLACK, (start_position, self.border, self.line_width, width))
            pygame.draw.rect(surface, BLACK, (self.border, start_position, width, self.line_width))
    
    def initialize_boxes(self):
        self.boxes = []
        
        top_left_numbers = []
        for i in range(0, self.grid_size):
            num = ((i * self.box_size) + self.border + (i *self.line_width))
            top_left_numbers.append(num)
        
        box_coordinates = list(itertools.product(top_left_numbers, repeat=2))
        for x, y in box_coordinates:
            self.boxes.append(Box(x, y, self.box_size))
    
    def get_box_at_pixel(self, x, y):
        for index, box in enumerate(self.boxes):
            if box.rect.collidepoint(x, y):
                return box
        return None
    
    def play_turn(self, box):
        if box.state != 0:
            return
        if self.turn == 1:
            box.mark_x()
            box.state = 1
            self.turn = 2
        elif self.turn == 2:
            box.mark_o()
            box.state = 2
            self.turn = 1
        return
    
    def calculate_winners(self):
        self.winners = []
        box_combinations = list(itertools.combinations([i for i in xrange(0, len(self.boxes))], self.grid_size))
        for combination in box_combinations:            
            diffs = []
            for i in xrange(0, self.grid_size - 1):
                diff = combination[i + 1] - combination[i]
                diffs.append(diff)
            if all(i == diff for i in diffs):
                # Vertical rows
                if diff == 1 and combination[0] % self.grid_size == 0:
                    self.winners.append(combination)
                # Horizontal rows
                if diff == self.grid_size:
                    self.winners.append(combination)
                # Diagonal rows
                if diff == self.grid_size + 1 and combination[0] == 0:
                    self.winners.append(combination)
                if diff == self.grid_size - 1 and combination[0] == self.grid_size - 1:
                    self.winners.append(combination)
    
    def check_for_winner(self):
        winner_player = 0
        for winner in self.winners:
            states = []
            for index in winner:
                states.append(self.boxes[index].state)
            if all(x == 1 for x in states):
                winner_player = 1
            if all(x == 2 for x in states):
                winner_player = 2
        return winner_player


def main():
    global surface
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    board = Board(4, 150, 50, 10)
    surface_size = (board.grid_size * board.box_size) + (board.border * 2) + (board.line_width * (board.grid_size - 1))
    
    surface = pygame.display.set_mode((surface_size, surface_size), 0, 32)
    pygame.display.set_caption('Tic Tac Toe')
    surface.fill(WHITE)
    board.setup()

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
                    winner = board.check_for_winner()
                    if winner:
                        winner_text = 'Player %s won!' % winner
                        font = pygame.font.Font('freesansbold.ttf', surface_size / 8)
                        text = font.render(winner_text, True, BLACK)
                        rect = text.get_rect()
                        rect.center = (surface_size / 2, surface_size / 2)
                        surface.blit(text, rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()