import pygame as pg
from pygame.locals import *
import sys

from entities import *

FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Game:
    clock = pg.time.Clock()
    score = 0

    def __init__(self):
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption('Mi Arkanoid')

        self.background_img = pg.image.load('resources/background.png').convert()

        self.fontGran = pg.font.Font('resources/fonts/PressStart2P.ttf', 28)
        self.font = pg.font.Font('resources/fonts/PressStart2P.ttf', 28)
        self.marcador = self.font.render('0', True, WHITE)
        self.livescounter = self.font.render('0', True, WHITE)
        self.text_game_over = self.fontGran.render('GAME OVER', True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Insert coin', True, WHITE)
        
        self.player = Racket()
        self.ball = Ball()
        self.tileGroup = pg.sprite.Group()

        self.playerGroup = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()
        self.playerGroup.add(self.player)


        self.start_partida()


    def create_tiles(self):
        self.tileGroup.empty()
        self.allSprites.empty()
        for j in range(5):
            for i in range(16):
                t = Tile(i*50, 60+j*32)
                self.tileGroup.add(t)
        
        self.tileGroup = Map(level1)
        self.allSprites.add(self.tileGroup)
        self.allSprites.add(self.player)
        self.allSprites.add(self.ball)


    def start_partida(self):
        self.player.lives = 3
        self.ball.start()
        self.create_tiles()
        self.score = 0


    def quitOver(self):
        pg.quit()
        sys.exit()

    def handleEvents_GO(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitOver()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.start_partida()

    
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitOver()

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

            if self.player.lives > 0:
                self.bucle_partida(dt)
            else:
                self.gameOver()

            pg.display.flip()
    

    def bucle_partida(self, dt):
        self.handleEvents()

        self.ball.test_collisions(self.playerGroup)
        self.score += self.ball.test_collisions(self.tileGroup, True)

        if self.ball.speed == 0:
            self.player.lives -= 1
            self.ball.start()
     
        self.livescounter = self.font.render(str(self.player.lives), True, WHITE)
        self.marcador = self.font.render(str(self.score), True, WHITE)

        self.screen.blit(self.background_img, (0,0))

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen)

        self.screen.blit(self.marcador, (750, 10))
        self.screen.blit(self.livescounter, (50, 10))

    def gameOver(self):
        self.handleEvents_GO()

        rect = self.text_game_over.get_rect()
        self.screen.blit(self.text_game_over, ((800 - rect.w)//2, 300))
        rect = self.text_insert_coin.get_rect()
        self.screen.blit(self.text_insert_coin, ((800 - rect.w)//2, 380))



if __name__ == '__main__':
    pg.init()
    game = Game()
    game.mainloop()
