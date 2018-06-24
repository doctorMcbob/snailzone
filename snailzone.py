import pygame
from pygame.locals import *

# COLORS
FOOT = (230, 80, 110)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def draw_foot(left, coord, dest):
    if not left:
        rects = [
            ((coord[0], coord[1]+10), (30, 70)),
            ((coord[0], coord[1]+8), (38, 40)),
            ((coord[0]+5, coord[1]+50), (30, 35)),
            ((coord[0]+1, coord[1]+7), (8, 8)),
            ((coord[0]+7, coord[1]+2) , (8, 10)),
            ((coord[0]+12, coord[1]) , (8, 10)),
            ((coord[0]+18, coord[1]) , (8, 10)),
            ((coord[0]+25, coord[1]) , (12, 17)),
        ]
    else:
        rects = [
            ((coord[0], coord[1]+10), (30, 70)),
            ((coord[0]-8, coord[1]+8), (38, 40)),
            ((coord[0]-5, coord[1]+50), (30, 35)),
            ((coord[0]+21, coord[1]+7), (8, 8)),
            ((coord[0]+15, coord[1]+2) , (8, 10)),
            ((coord[0]+10, coord[1]) , (8, 10)),
            ((coord[0]+4, coord[1]) , (8, 10)),
            ((coord[0]-7, coord[1]) , (12, 17)),
        ]
    for rect in rects:
        pygame.draw.ellipse(dest, FOOT, pygame.Rect(rect))


if __name__ == """__main__""":
    screen = pygame.display.set_mode((640, 480))
    
    while True:
        screen.fill(WHITE)
        c = 0
        while c < 10:
            
            draw_foot(c%2, ([400, 450][c%2], 400 - c*80), screen)
            c += 1
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
