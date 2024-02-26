import pygame.image


class Settings:
    def __init__(self):
        self.screen_width = None
        self.screen_height = None
        self.intro_background = pygame.image.load('images/kapitandupa.jpg')
        self.background = pygame.image.load('images/galaktyka.png')

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.5
        self.score_scale = 1.5

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()


    def resize_background(self):
        self.intro_background = pygame.transform.scale(
            self.intro_background,(
                self.screen_width, self.screen_height))
        self.background = pygame.transform.scale(
            self.background,(
                self.screen_width, self.screen_height))


    def initialize_dynamic_settings(self):
        if self.difficulty_level == 'easy':
            self.ship_limit = 3
            self.ship_speed = 10
            self.bullet_speed = 10.0
            self.alien_speed = 1.0
        if self.difficulty_level == 'medium':
            self.ship_limit = 2
            self.ship_speed = 15
            self.bullet_speed = 15.0
            self.alien_speed = 1.5
        if self.difficulty_level == 'hard':
            self.ship_limit = 1
            self.ship_speed = 30
            self.bullet_speed = 20.0
            self.alien_speed = 3.0

        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)



