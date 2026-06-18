import pygame as pg
import sys
import time
from bird import Bird
from pipe import Pipe
from coin import Coin

pg.init()

class Game:
    def __init__(self):
        # Setting window config
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.bird = Bird(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes = []
        self.coins = []
        self.pipe_generate_counter = 71
        self.coin_generate_counter = 150
        self.score = 0
        self.total_speed = 0
        self.coin_count = 0
        self.font = pg.font.Font(None, 36)
        self.game_over = False

        self.setUpBgAndGround()
        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            dt = self.get_delta_time(last_time)
            last_time = time.time()

            self.handle_events(dt)
            if not self.game_over:
                self.updateEverything(dt)
                self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def get_delta_time(self, last_time):
        return time.time() - last_time

    def handle_events(self, dt):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.game_over:
                        self.restart_game()
                    else:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                if event.key == pg.K_SPACE and self.is_enter_pressed and not self.game_over:
                    self.bird.flap(dt, self.score)

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 568:
                self.game_over = True
                self.is_enter_pressed = False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.game_over = True

        for coin in self.coins:
            if self.bird.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1
                self.total_speed += abs(int(self.bird.y_velocity))
                self.coin_count += 1
                self.bird.reset_speed()  # Reset speed when collecting a coin

    def updateEverything(self, dt):
        if self.is_enter_pressed and not self.game_over:
            self.update_ground(dt)
            self.generate_pipes()
            self.generate_coins()

            for pipe in self.pipes:
                pipe.update(dt)
            self.pipes = [pipe for pipe in self.pipes if pipe.rect_up.right > 0]

            for coin in self.coins:
                coin.update(dt)
            self.coins = [coin for coin in self.coins if coin.rect.x > -coin.rect.width]

            self.bird.update(dt, self.score)

    def update_ground(self, dt):
        self.ground1_rect.x -= int(self.move_speed * dt)
        self.ground2_rect.x -= int(self.move_speed * dt)

        if self.ground1_rect.right < 0:
            self.ground1_rect.x = self.ground2_rect.right
        if self.ground2_rect.right < 0:
            self.ground2_rect.x = self.ground1_rect.right

    def generate_pipes(self):
        if self.pipe_generate_counter > 70:
            self.pipes.append(Pipe(self.scale_factor, self.move_speed))
            self.pipe_generate_counter = 0
        self.pipe_generate_counter += 1

    def generate_coins(self):
        if self.coin_generate_counter > 100:
            self.coins.append(Coin(self.scale_factor, self.move_speed))
            self.coin_generate_counter = 0
        self.coin_generate_counter += 1

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        for coin in self.coins:
            coin.draw(self.win)

        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.win.blit(score_surface, (10, 10))

        # Display the bird's speed
        speed_surface = self.font.render(f'Speed: {abs(int(self.bird.y_velocity))}', True, (255, 255, 255))
        self.win.blit(speed_surface, (10, 50))

        if self.game_over:
            self.display_game_over()

    def display_game_over(self):
        self.win.fill((255, 255, 255))
        game_over_surface = self.font.render('Game Over!', True, (0, 0, 0))
        restart_surface = self.font.render('Press Enter to Restart', True, (0, 0, 0))
        score_surface = self.font.render(f'Final Score: {self.score}', True, (0, 0, 0))

        average_speed = self.total_speed / self.coin_count if self.coin_count > 0 else 0
        average_speed_surface = self.font.render(f'Average Speed: {average_speed:.2f}', True, (0, 0, 0))

        self.win.blit(game_over_surface, (self.width // 2 - 100, self.height // 2 - 50))
        self.win.blit(restart_surface, (self.width // 2 - 150, self.height // 2))
        self.win.blit(score_surface, (self.width // 2 - 100, self.height // 2 + 50))
        self.win.blit(average_speed_surface, (self.width // 2 - 150, self.height // 2 + 100))

    def restart_game(self):
        self.pipes.clear()
        self.coins.clear()
        self.bird.reset()
        self.score = 0
        self.total_speed = 0
        self.coin_count = 0
        self.is_enter_pressed = False
        self.game_over = False
        self.pipe_generate_counter = 71
        self.coin_generate_counter = 150

    def setUpBgAndGround(self):
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

if __name__ == "__main__":
    Game()
