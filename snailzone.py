import pygame
from pygame.locals import *
from random import randint

pygame.init()

SCREEN = pygame.display.set_mode((640, 480))
pygame.display.set_caption(""" _,.=+*'"'*+=.,_,.=+*'"  SnailZone  "'*+=.,_,.=+*'"'*+=.,_ """)
MAN16 = pygame.font.SysFont("Manjari", 16)
MAN32 = pygame.font.SysFont("Manjari", 32)
MAN64 = pygame.font.SysFont("Manjari", 64)
CLOCK = pygame.time.Clock()

SCREEN.fill((0, 0, 0))
SCREEN.blit(MAN32.render("Loading...", 0, (255, 255, 255)), (10, 10))
pygame.display.update()

#COLORS
LGREEN = (121, 232, 84)
LRED = (232, 96, 84)

footsprite = pygame.image.load("foot.png").convert()
footsprite.set_colorkey((100, 100, 50))
bugsprite = pygame.image.load("bugs.png").convert()
snailsprite = pygame.image.load("snail.png").convert()
leafsprite = pygame.image.load("leafs.png").convert()
sidewalksprite = pygame.image.load("sidewalk.png").convert()
explainsprite = pygame.image.load("explain.png").convert()
introsprite = pygame.image.load("intro.png").convert()
endsprite = pygame.image.load("ending.png").convert()

def makebug(i): # i index of bug 0 ant, 1 ladybug, 2 slug, 3 snail
    if i != 3:
        sprite = pygame.surface.Surface((32, 32))
        sprite.set_colorkey((100, 100, 50))
        sprite.blit(bugsprite, (0 - i*64, 0))
    else:
        sprite = pygame.surface.Surface((64, 64))
        sprite.set_colorkey((100,100, 50))
        sprite.blit(snailsprite, (0, 0))
    if i % 2 == 0:
        pos = (randint(55, 640 - 32), 0)
    elif i == 1:
        pos = (randint(55, 640 - 32), 32)
    elif i == 3:
        pos = (randint(55, 640 - 64), 0)
    return [sprite, pos, i]

def deadbug(i):
    if i != 3:
        sprite = pygame.surface.Surface((32, 32))
        sprite.blit(bugsprite, ((0 - i * 32) + 16, 0))
    else:
        sprite = pygame.surface.Surface((64, 64))
        sprite.blit(snailsprite(32, 0))
    return sprite

"""
STRUCTURE
sidewalk:
[         v-- bugs
  [ (sprite, position, bugindex), ... ], 
  [ ... ]
]
"""

def blank_sidewalk(rows):
    surf = pygame.Surface((640, 64*rows))
    for y in range((rows // 4)+1):
        surf.blit(sidewalksprite, (0, y * 256))
    return surf

def draw_actors(sidewalk, rows):
    for i, row in enumerate(rows):
        for bug in row:
            if bug[2] != 3:
                sprite = bug[0]
                X, Y = bug[1]
                sidewalk.blit(sprite, (X, (i*64) + Y))
        for bug in row:
            if bug[2] == 3:
                sprite = bug[0]
                X, Y = bug[1]
                sidewalk.blit(sprite, (X, (i*64) + Y))                
    return sidewalk

def make_rows(rows):
    ROWS = []
    for i in range(rows):
        row = []
        for n in range((i // 20)+1):
            roll = randint(0, 50)
            if 15 < roll <= 25:
                row.append(makebug(randint(0, 2)))
            if 25 < roll <= 35:
                row.append(makebug(3))
            if 35 < roll <= 45:
                row.append(makebug(2))
                row.append(makebug(1))
            if 45 < roll:
                for n in range(3): row.append(makebug(0))
        ROWS.append(row)
    return ROWS[::-1]

def move_actors(rows):
    for row in rows:
        for i in range(len(row)):
            sprite, pos, idx = row[i]
            x, y = pos
            if idx == 0:
                if x - 3 < 55: x = 640 - 32
                row[i][1] = (x - 3, y)
            if idx == 1:
                if x + 5 > 640 - 32: x = 55
                row[i][1] = (x + 5, y)
            if idx == 2:
                if x + 1 > 640 - 32: x = 55
                row[i][1] = (x + 1, y)
            if idx == 3:
                if x + 2 > 640 - 64: x = 55
                row[i][1] = (x + 2, y)
        
def main_menu():
    sidewalk = blank_sidewalk(120)
    rows = make_rows(120)
    draw_actors(sidewalk, rows)
    y = 480 - (64*120)
    SELECTED = 0
    menu = ["start", "explain please"]
    while True:
        CLOCK.tick(30)
        sidewalk = blank_sidewalk(120)
        move_actors(rows)
        draw_actors(sidewalk, rows)
        SCREEN.blit(sidewalk, (0, y))
        SCREEN.blit(MAN64.render("SnailZone", 0, LGREEN), (50, 50))
        for i, option in enumerate(menu):
            if i == SELECTED: col = LRED
            else: col = LGREEN
            SCREEN.blit(MAN32.render(option, 0, col), (100, 100 + (i * 32)))
        y += 1
        if y >= 0:
            y = 640 - (64*30)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_DOWN: SELECTED = (SELECTED + 1) % len(menu)
                if e.key == K_UP: SELECTED = (SELECTED - 1) % len(menu)
                if e.key == K_SPACE:
                    return menu[SELECTED]

def explain():
    while True:
        SCREEN.blit(explainsprite, (0, 0))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key in [K_SPACE, K_ESCAPE]:
                    return

def intro():
    i = 0
    while i <= 1:
        SCREEN.blit(introsprite, (0 - (i*640), 0))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    i += 1

def draw_foot(sidewalk, step, pos):
    if step % 2: sprite = footsprite
    else: sprite = pygame.transform.flip(footsprite, 1, 0)
    x = 55 + (pos[0] * 32)
    y = (120*64) - (((step+1) * 64) + pos[1] * 32)
    sidewalk.blit(sprite, (x, y))

def foot_collision(rows, step, pos):
    """checks if player stepped on a bug, returns the ( step index, bug index )  that was stepped one"""
    checklist = []
    refrence = []
    for i, row in enumerate(rows[::-1]):
        if i in [step-1, step, step+1]:
            for n, bug in enumerate(row):
                x, y = bug[1]
                refrence.append((i, n))
                checklist.append(pygame.rect.Rect((x, y + ((i - step) * 64)), (bug[0].get_width(), bug[0].get_height())))
    x, y = pos
    hitbox = pygame.rect.Rect((55 + (x * 32) + 1, (y * 32)), (30, 60))
    i = hitbox.collidelist(checklist)
    return refrence[i]

def run_game():
    STEP = 0
    foot_pos = (10, 0) #relative, 9 slots horizontal 3 vertical
    rows = make_rows(120)
    while STEP < 120:
        CLOCK.tick(30)
        move_actors(rows)
        sidewalk = draw_actors(blank_sidewalk(120), rows)
        
        mov = [0, 0]
        place = False
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE: place = True
                if e.key == K_LEFT: mov[0] -= 1
                if e.key == K_RIGHT: mov[0] += 1
                if e.key == K_UP: mov[1] += 1
                if e.key == K_DOWN: mov[1] -= 1
                if e.key == K_ESCAPE: explain()
        if 0 <= foot_pos[0] + mov[0] < 18:
            foot_pos = foot_pos[0] + mov[0], foot_pos[1]
        if -1 <= foot_pos[1] + mov[1] <= 1:
            foot_pos = foot_pos[0], foot_pos[1] + mov[1]
        if place:
            bug = foot_collision(rows, STEP, foot_pos)
            if bug is not None: print('hit')
            STEP += 1
            foot_pos = foot_pos[0], 0
        draw_foot(sidewalk, STEP, foot_pos)
        SCREEN.blit(sidewalk, (0, 480 - (64 * 120) + (STEP * 64)))
        pygame.display.update()

                
if __name__ == "__main__":
    choice = None
    while choice != "start":
        choice = main_menu()
        if choice == "explain please": explain()

    intro()
    run_game()
