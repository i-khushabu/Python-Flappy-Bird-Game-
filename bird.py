import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super(Bird, self).__init__()
        self.img_list = [
            pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_factor),
            pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(), scale_factor)
        ]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 384))
        self.y_velocity = 0
        self.base_gravity = 500
        self.base_flap_strength = 250
        self.anim_counter = 0
        self.update_on = False

    def reset(self):
        self.rect.center = (100, 384)
        self.y_velocity = 0
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.anim_counter = 0
        self.update_on = False

    def reset_speed(self):
        self.y_velocity = 0  # Reset the vertical speed when collecting a coin

    def update(self, dt, score):
        if self.update_on:
            self.playAnimation()
            self.applyGravity(dt)

            if self.rect.y < 0:
                self.rect.y = 0
                self.y_velocity = 0

            if self.rect.bottom >= 768:
                self.rect.bottom = 768
                self.update_on = False

    def applyGravity(self, dt):
        # Adjust gravity based on score
        gravity = self.base_gravity
        self.y_velocity += gravity * dt
        self.rect.y += self.y_velocity * dt

    def flap(self, dt, score):
        flap_strength = self.base_flap_strength
        self.y_velocity = -flap_strength

    def playAnimation(self):
        if self.anim_counter >= 5:
            self.image_index = 1 - self.image_index
            self.image = self.img_list[self.image_index]
            self.anim_counter = 0
        self.anim_counter += 1
