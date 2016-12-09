""" Level 5 of Asteroid Attack. """

# Pygame
import pygame
# Game modules
import game_scene
import ui_scenes
import gameplay_items
import scene_tools
import level_6


class LevelFive(game_scene.GameScene):
    """ Class for level 5. """
    def __init__(self, ship, score, lives, health):
        self.player = ship
        super().__init__(pygame.image.load('assets/dark_purple_stars.png').convert())
        # Fill it with brown asteroids
        scene_tools.initial_falling_objects(3, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)
        # Fill it with grey asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids)
        # Fill it with small asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.MedAsteroid, self.all_sprites, self.asteroids)

        self.score = score
        self.lives = lives
        self.health = health

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 5 seconds
        scene_tools.add_falling_object(self.timer, 300, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)
        # Add a new grey asteroid every 10 seconds
        scene_tools.add_falling_object(self.timer, 600, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids)
        # Add a new small asteroid every 15 seconds
        scene_tools.add_falling_object(self.timer, 900, gameplay_items.MedAsteroid, self.all_sprites, self.asteroids)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.score, self.lives, self.health, level_6.LevelSix)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)