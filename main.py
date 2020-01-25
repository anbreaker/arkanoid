import pygame as pg
from pygame.locals import *
import sys

from entities import *

FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

nivel = (['XXXXXXXXXX', 'XXXXXXXXXX', 'XXXXXXXXXX', 'XXXXXXXXXX', 'XXXXXXXXXX'],
         ['XXXXXXXXXX', '-XXXXXXXX-', '--XXXXXX--', '---XXXX---', '----XX----'],
         ['X---------', 'XXX-------', 'XXXXX-----', 'XXXXXXX---', 'XXXXXXXXX-'],
         ['-XXXXXXXX-', '-XXXXXXXX-', '-XXXXXXXX-', '-XXXXXXXX-', '-XXXXXXXX-'],
         ['----XX----', '---XXXX---', '--XXXXXX--', '-XXXXXXXX-', 'XXXXXXXXXX'])


class Game:
    clock = pg.time.Clock()
    score = 0
    niveles = 1

    def __init__(self):
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption('Mi Arkanoid')

        self.background_img = pg.image.load('resources/background_1.png').convert()

        self.fontGran = pg.font.Font('resources/fonts/PressStart2P.ttf', 25)
        self.font = pg.font.Font('resources/fonts/PressStart2P.ttf', 20)
        self.text_nivel = self.font.render('Level', True, WHITE)
        self.label_level = self.font.render('1', True, WHITE)
        self.text_marcador = self.font.render('Score', True, WHITE)
        self.marcador = self.font.render('0', True, WHITE)
        self.text_lives = self.font.render('Lives', True, WHITE)
        self.livescounter = self.font.render('0', True, WHITE)
        self.text_game_over = self.fontGran.render('GAME OVER', True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Insert coin', True, WHITE)
        self.text_congratulations = self.fontGran.render('LEVEL COMPLETED', True, YELLOW)
        self.text_next_level = self.font.render('<SPACE> - Go to Next Level', True, WHITE)
        self.text_end_game = self.fontGran.render('CONGRATULATIONS', True, YELLOW)
        self.text_push_to_start = self.font.render('<SPACE> - Push to start', True, WHITE)
        
        self.player = Racket()
        self.ball = Ball()
        self.tileGroup = pg.sprite.Group()

        self.playerGroup = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()
        self.playerGroup.add(self.player)

        self.start_partida()


    def create_tile(self):
        self.tileGroup.empty()
        self.allSprites.empty()

        self.mapa = Mapa()
        self.tileGroup = self.mapa.bricks(self.level)

        self.allSprites.add(self.tileGroup)
        self.allSprites.add(self.player)
        self.allSprites.add(self.ball)


    def start_partida(self):
        self.score = 0
        self.player.lives = 3
        self.player.rect.x = 355
        self.player.rect.y = 580
        self.ball.start()
        self.niveles = 1
        self.level = nivel[0]
        self.create_tile()


    def start_new_level(self):
        self.player.rect.x = 355
        self.player.rect.y = 580
        self.ball.start()
        self.niveles += 1
        self.set_level()
        self.create_tile()


    def set_level(self):
        for ind in range(len(nivel)):
            if self.level == nivel[ind]:
                ind += 1
                self.level = nivel[ind]
                break


    def next_level(self):
        self.handleEvents_NL()
        self.ball.speed == 0

        rect = self.text_congratulations.get_rect()
        self.screen.blit(self.text_congratulations, ((800 - rect.w)//2, 300))
        rect = self.text_next_level.get_rect()
        self.screen.blit(self.text_next_level, ((800 - rect.w)//2, 380))


    def gameOver(self):
        self.handleEvents_GO()

        rect = self.text_game_over.get_rect()
        self.screen.blit(self.text_game_over, ((800 - rect.w)//2, 300))
        rect = self.text_insert_coin.get_rect()
        self.screen.blit(self.text_insert_coin, ((800 - rect.w)//2, 380))


    def gameEnd(self):
        self.handleEvents_GO()

        rect = self.text_end_game.get_rect()
        self.screen.blit(self.text_end_game, ((800 - rect.w)//2, 300))
        rect = self.text_push_to_start.get_rect()
        self.screen.blit(self.text_push_to_start, ((800 - rect.w)//2, 380))


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


    def handleEvents_NL(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitOver()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.start_new_level()

    
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

            if self.player.lives > 0 and len(self.tileGroup) != 0:
                self.bucle_partida(dt)

            elif self.niveles == len(nivel) and len(self.tileGroup) == 0:
                self.gameEnd()

            elif len(self.tileGroup) == 0:
                self.next_level()
            
            else:
                self.gameOver()

            pg.display.flip()
    

    def bucle_partida(self, dt):
        self.handleEvents()

        self.ball.test_collisions(self.playerGroup)
        self.score += self.ball.test_collisions(self.tileGroup, True)

        if len(self.tileGroup) != 0 and self.ball.speed == 0:
            self.player.lives -= 1
            self.ball.start()

        self.livescounter = self.font.render(str(self.player.lives), True, WHITE)
        self.marcador = self.font.render(str(self.score), True, WHITE)
        self.label_level = self.font.render(str(self.niveles), True, WHITE)
        self.screen.blit(self.background_img, (0,0))

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen)

        self.screen.blit(self.text_lives, (10, 10))
        self.screen.blit(self.livescounter, (120, 10))
        self.screen.blit(self.text_nivel, (350, 10))
        self.screen.blit(self.label_level, (460, 10))
        self.screen.blit(self.text_marcador, (620, 10))
        self.screen.blit(self.marcador, (735, 10))


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.mainloop()
