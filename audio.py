import random

import pygame
import os


class Audio:
    def __init__(self):
        self.goal = 200
        self.intro = pygame.mixer.Sound("audio/intro.mp3")
        self.music = pygame.mixer.Sound("audio/amper.mp3")
        self.ship_hit = pygame.mixer.Sound("audio/dalnie.mp3")
        self.game_over = pygame.mixer.Sound("audio/gameover.mp3")
        pliki = os.listdir("audio/goal_sound")

        self.random_audio_list = [
            pygame.mixer.Sound(f"audio/goal_sound/{plik}") for plik in pliki
        ]

    def play_random_sound(self):
        self.sound = random.choice(self.random_audio_list)
        self.sound.play()

