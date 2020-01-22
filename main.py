import pygame as pg
from pygame.locals import *
import sys

from entities import *

FPS = 60

class Game:
    clock = pg.time.Clock()

    def __init__(self):
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption('Mi Arkanoid')

        self.background_img = pg.image.load('resources/background.png').convert()
        self.player = Racket()
        self.ball = Ball()

        self.tileGroup = pg.sprite.Group()
        for j in range(5):
            for i in range(16):
                t = Tile(i*50, 10+j*32)
                self.tileGroup.add(t)

        self.playerGroup = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()
        self.playerGroup.add(self.player)
        self.allSprites.add(self.player)
        self.allSprites.add(self.ball)
        self.allSprites.add(self.tileGroup)
        self.score = 0

    def gameOver(self):
        pg.quit()
        sys.exit()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.gameOver()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.player.go_left()
                if event.key == K_RIGHT:
                    self.player.go_right()
        
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.player.go_left()
        if keys_pressed[K_RIGHT]:
            self.player.go_right()

    def mainloop(self):
        while True:
            dt = self.clock.tick(FPS)

            self.handleEvents()

            self.ball.test_collisions(self.playerGroup)
            self.score += self.ball.test_collisions(self.tileGroup, True)
            print(self.score)

            if self.ball.speed == 0:
                self.player.lives -= 1
                self.ball.start()

            if self.player.lives == 0:
                self.gameOver()

            self.screen.blit(self.background_img, (0,0))

            self.allSprites.update(dt)
            self.allSprites.draw(self.screen)

            pg.display.flip()


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.mainloop()
