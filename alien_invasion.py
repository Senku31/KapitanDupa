import sys
from time import sleep

import pygame

from audio import Audio
from button import Button
from scoreboard import Scoreboard
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.audio = Audio()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.resize_background()

        pygame.display.set_caption("Kapitan Dupa")
        self.audio.intro.play()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = False

        self.play_button = Button(self,"Graj")

        self._make_difficulty_buttons()


    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        if not self.game_active:
            if event.key == pygame.K_g:
                self._start_game()
            elif event.key == pygame.K_q:
                sys.exit()
            else:
                return
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()


    def _check_difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'easy'
            self._start_game()
        elif medium_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'medium'
            self._start_game()
        elif hard_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'hard'
            self._start_game()

    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, "Łatwy")
        self.medium_button = Button(self, "Średni")
        self.hard_button = Button(self,"Nic nie czuje")

        self.easy_button.rect.top = self.play_button.rect.top + 1.5 * self.play_button.rect.height
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = self.easy_button.rect.top + 1.5 * self.easy_button.rect.height
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = self.medium_button.rect.top + 1.5 * self.medium_button.rect.height
        self.hard_button._update_msg_position()


    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.game_active = True

        self.audio.music.play(loops=-1)


        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()
        self.sb.prep_ships()

        pygame.mouse.set_visible(False)


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            new_bullet.dzida.play()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _play_audio_every_goal(self):
        if self.stats.score >= self.audio.goal:
            self.audio.play_random_sound()
            self.audio.goal += self.audio.goal

    def _check_bullet_alien_collision(self):
        collisons = pygame.sprite.groupcollide(self.bullets,self.aliens, True,True)
        if collisons:
            for aliens in collisons.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
            self._play_audio_every_goal()
        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self._create_fleet()
            self.audio.ship_hit.play()
            sleep(0.5)
        else:
            self.game_active = False
            self.audio.music.stop()
            self.audio.game_over.play()
            sleep(7)
            self.audio.intro.play()
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2* alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.__change_fleet_direction()
                break

    def __change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()


    def _update_screen(self):

        self.screen.blit(self.settings.background,(0, 0))

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.screen.blit(self.settings.intro_background, (0, 0))
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
