""" Level 2 of Asteroid Attack. """

# Pygame
import pygame
# Game modules
import game_scene
import ui_scenes
import gameplay_items
import scene_tools
import level_3


class LevelTwo(game_scene.GameScene):
    """ Class for level 2. """
    def __init__(self, ship, score, lives, health):
        self.player = ship
        super().__init__(pygame.image.load('assets/black_stars.png').convert())
        self.score = score
        self.lives = lives
        self.health = health

        # Fill it with brown asteroids
        scene_tools.initial_falling_objects(6, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 3 seconds
        scene_tools.add_falling_object(self.timer, 180, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.score, self.lives, self.health, level_3.LevelThree)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)