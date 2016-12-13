""" Level 8 of Asteroid Attack. """

# Pygame
import pygame
# Game modules
import game_scene
import ui_scenes
import gameplay_items
import scene_tools


class LevelEight(game_scene.GameScene):
    """ Class for level 8. """
    def __init__(self, ship, score, lives, health):
        self.player = ship
        super().__init__(pygame.image.load('assets/purple_stars.png').convert())
        self.score = score
        self.lives = lives
        self.health = health

        # Fill it with brown asteroids
        scene_tools.initial_falling_objects(3, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)
        # Fill it with grey asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids)
        # Fill it with small asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.MedAsteroid, self.all_sprites, self.asteroids)
        # Fill it with aliens
        scene_tools.initial_falling_objects(1, gameplay_items.Alien, self.aliens)
        # Fill with fragmenting asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.FragmentingAsteroid, self.all_sprites, argument=self)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 10 seconds
        scene_tools.add_falling_object(self.timer, 600, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids)
        # Add a new grey asteroid every 10 seconds
        scene_tools.add_falling_object(self.timer, 600, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids)
        # Add a new small asteroid every 10 seconds
        scene_tools.add_falling_object(self.timer, 600, gameplay_items.MedAsteroid, self.all_sprites, self.asteroids)
        # Add a new alien every 15 seconds
        scene_tools.add_falling_object(self.timer, 900, gameplay_items.Alien, self.aliens)
        # Add a new fragmenting asteroid every 20 seconds
        scene_tools.add_falling_object(self.timer, 1200, gameplay_items.FragmentingAsteroid, self.all_sprites,
                                       argument=self)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose")

        if self.timer == 5000:
            self.next_scene = ui_scenes.GameOverScene(self.score, "win")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)