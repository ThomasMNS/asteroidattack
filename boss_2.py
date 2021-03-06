""" The second boss fight. """

# Pygame
import pygame
# Game modules
import game_scene
import ui_scenes
import gameplay_items
import ui_items
import constants


class BossTwo(game_scene.GameScene):
    """ Class for a level with 1 boss. """
    def __init__(self, settings, ship, ship_2, score, lives):
        self.settings = settings
        self.player = ship
        self.player_2 = ship_2
        super().__init__(pygame.image.load('assets/black_stars.png').convert())
        self.score = score
        self.lives = lives

        self.boss = gameplay_items.Boss(self, 2)
        self.aliens.add(self.boss)

        # Level unique UI items
        self.boss_health_bar = ui_items.HealthBar()
        self.ending_timer = 0

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()

        # Wait 3 seconds after the boss dies before moving on
        if self.boss.health <= 0:
            self.ending_timer += 1

        if self.ending_timer >= 180:
            self.next_scene = ui_scenes.GameOverScene(self.score, "win", self.player_2, self.settings)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose", self.player_2, self.settings)

        self.boss_health_bar.update()

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)

        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen, True)
        # Level unique UI
        self.boss_health_bar.draw(screen)
        phase_render = self.score_font.render("Phase: {0!s}".format(self.boss.display_phase), True, constants.WHITE)
        phase_render_rect = phase_render.get_rect()
        x = (1024 / 2) - (phase_render_rect.width / 2)
        y = self.boss_health_bar.y + self.boss_health_bar.height + 10
        screen.blit(phase_render, (x, y))
