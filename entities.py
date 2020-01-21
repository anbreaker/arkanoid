import pygame as pg
from pygame.locals import *

FPS = 60

class Racket(pg.sprite.Sprite):
    pictures = 'racket_horizontal.png'
    speed = 10

    def __init__(self, x=355 , y=580):
        self.x = x
        self.y = y

        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = self.rect.w
        self.h = self.rect.h
    
    def go_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)

    def go_right(self):
        self.rect.x = min(self.rect.x + self.speed, 800-self.w)
    
