#!/usr/bin/python3
#
# a random snow animation
#

import pygame, math
from numpy import array, random

pygame.init()

class Snowflake():

    __slots__ = [
            '__rand',
            '__mass',
            '__pos',
            '__vel',
            '__acc'
        ] # non-dynamic attributes

    def __init__(self, mass = 1):
        self.__rand = (random.random()*0.35)+0.65
        self.__mass = mass

        self.__pos = array(
                [random.random()*(screen_size[0]+40)-20 ,
                    -5+self.__mass-5]
            )
        self.__vel = array( [(random.random()-0.5)*0.3, 0.0] )
        self.__acc = array( [0.0, 0.5] )*self.__mass

    def update(self):
        if self.__vel[1] < 0.9*self.__mass:
            self.__vel += self.__acc
        self.__pos += self.__vel

    def render(self, on):
        self.update()
        pygame.draw.circle(
                on,
                white,
                (int(self.__pos[0]), int(self.__pos[1])),
                int(5*self.__mass*self.__rand)
            )

    @property
    def off(self):
        if (self.__pos[1] > screen_size[1]+5*self.__mass or
                self.__pos[0] < -30 or
                self.__pos[0] > screen_size[0]+30):
            return True
        return False


# setup
info = pygame.display.Info()
screen_size = (info.current_w,info.current_h)

# colors
black = (0,0,0)
white = (255,255,255)

# init
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
pygame.display.set_caption("Snowflakes!")
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

# main loop
running = True # run program?
gen = True # generate snow?
snow = []

while running:
    screen.fill(black) # redraw screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_SPACE: gen = not gen # toggle snow

    if random.random() <= 0.35 and gen == True: # only in 35% of time
        random_mass = 0
        while random_mass < 0.5: random_mass = random.random()
        snow.append( Snowflake(random_mass) )

    for i in range( len(snow)-10 ): # don't delete all off screens,
        if snow[i].off: del snow[i] # preserve the last ten

    for flake in snow:
        flake.render(screen)

    pygame.display.update()
    clock.tick(120) # 120 fps
