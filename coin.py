import pygame as pg
import random

class Coin:
    def __init__(self, scale_factor, move_speed):
        # Set a smaller scale factor for the coin
        small_scale_factor = scale_factor * 0.1  # Adjust this value as needed
        self.image = pg.transform.scale_by(pg.image.load("assets/coin.png").convert_alpha(), small_scale_factor)
        self.rect = self.image.get_rect()
        self.rect.x = 600  # Start off-screen to the right
        self.rect.y = random.randint(200, 500)  # Random height for coin
        self.move_speed = move_speed

    def update(self, dt):
        self.rect.x -= int(self.move_speed * dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
