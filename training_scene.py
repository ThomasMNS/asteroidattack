""" A scene for the 'training' game mode. Inherits from the game_scene but with the init method overriden
to allow for player chosen numbers of enemies, powerups etc. """

# Pygame
import pygame
# Standard library
import os
# Game modules
import game_scene
import gameplay_items
import scene_tools
import constants
import ui_scenes


class TrainingScene(game_scene.GameScene):
    """ A scene for the 'training' game mode. Inherits from the game_scene but with some attributs overriden
    to allow for player chosen numbers of enemies, powerups etc. """
    def __init__(self, ship, ship_2, training_choices):
        self.player = ship
        self.player_2 = ship_2
        self.score = 0
        super().__init__(pygame.image.load('assets/training_background.png').convert())
        self.next_scene = self
        # Getting the user choices
        self.brown_asteroids_toggle = training_choices[0]
        self.brown_asteroid_count = training_choices[1]
        self.brown_asteroid_seconds = training_choices[2]

        self.grey_asteroids_toggle = training_choices[3]
        self.grey_asteroid_count = training_choices[4]
        self.grey_asteroid_seconds = training_choices[5]

        self.small_asteroids_toggle = training_choices[6]
        self.small_asteroid_count = training_choices[7]
        self.small_asteroid_seconds = training_choices[8]

        self.alien_toggle = training_choices[9]
        self.alien_count = training_choices[10]
        self.alien_seconds = training_choices[11]

        self.powerups_toggle = training_choices[12]
        self.lives = training_choices[13]
        self.health = training_choices[14]

        # Make stars green to fit with the simulator theme
        for star in self.top_stars:
            star.color = constants.BRIGHT_GREEN
        for star in self.bottom_stars:
            star.color = constants.BRIGHT_GREEN

        # Create brown asteroids if the option is selected
        if self.brown_asteroids_toggle == 0:
            scene_tools.initial_falling_objects(self.brown_asteroid_count, gameplay_items.BrownAsteroid,
                                                self.all_sprites, self.asteroids, argument=self)

        # Create grey asteroids if the option is selected
        if self.grey_asteroids_toggle == 0:
            scene_tools.initial_falling_objects(self.grey_asteroid_count, gameplay_items.GreyAsteroid,
                                                self.all_sprites, self.asteroids, argument=self)

        # Create small asteroids if the option is selected
        if self.small_asteroids_toggle == 0:
            scene_tools.initial_falling_objects(self.small_asteroid_count, gameplay_items.MedAsteroid,
                                                self.all_sprites, self.asteroids, argument=self)

        # Create aliens if the option is selected
        if self.alien_toggle == 0:
            scene_tools.initial_falling_objects(self.alien_count, gameplay_items.Alien,
                                                self.aliens, argument=self)

        # Delete powerups if option not selected
        if self.powerups_toggle == 1:
            for powerup in self.pups:
                powerup.kill()

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()

        # Add new brown asteroids every x seconds if option is selected
        if self.brown_asteroids_toggle == 0:
            scene_tools.add_falling_object(self.timer, self.brown_asteroid_seconds * 60, gameplay_items.BrownAsteroid,
                                           self.all_sprites, self.asteroids, argument=self)

        # Add new grey asteroids every x seconds if option is selected
        if self.grey_asteroids_toggle == 0:
            scene_tools.add_falling_object(self.timer, self.grey_asteroid_seconds * 60, gameplay_items.GreyAsteroid,
                                           self.all_sprites, self.asteroids, argument=self)


        # Add new small asteroids every x seconds if option is selected
        if self.small_asteroids_toggle == 0:
            scene_tools.add_falling_object(self.timer, self.small_asteroid_seconds * 60, gameplay_items.MedAsteroid,
                                           self.all_sprites, self.asteroids, argument=self)

        # Add new alien every x seconds if option is selected
        if self.alien_toggle == 0:
            scene_tools.add_falling_object(self.timer, self.alien_seconds * 60, gameplay_items.Alien, self.aliens,
                                           argument=self)

        if self.timer == 5000:
            self.next_scene = ui_scenes.TrainingGameOverScene(self.score, "win")

        if self.lives == 0:
            self.next_scene = ui_scenes.TrainingGameOverScene(self.score, "lose")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        for alien in self.aliens:
            alien.draw_lasers(screen)
        self.aliens.draw(screen)
        game_scene.GameScene.draw_text(self, screen)