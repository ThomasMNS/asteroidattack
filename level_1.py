""" The first level of Asteroid Attack. """

# Pygame
import pygame
# Game modules
import level_2
import game_scene
import ui_scenes
import gameplay_items
import scene_tools


class LevelOne(game_scene.GameScene):
    """ Class for the first game level. """
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.health = 100
        super().__init__(pygame.image.load('assets/black_stars.png').convert())

        # Initial Asteroids
        scene_tools.initial_falling_objects(3, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new asteroid every 4 seconds
        scene_tools.add_falling_object(self.timer, 240, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.score, self.lives, self.health, level_2.LevelTwo)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        for alien in self.aliens:
            alien.draw_lasers(screen)
        self.aliens.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)