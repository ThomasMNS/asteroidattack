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
        scene_tools.initial_falling_objects(2, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)
        # Fill it with grey asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

        # Fill it with fragmenting asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.FragmentingAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

        # Fill it with aliens
        scene_tools.initial_falling_objects(1, gameplay_items.Alien, self.aliens, argument=self)

        # Fill it with small asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.MedAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

        self.score = score
        self.lives = lives
        self.health = health

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 12 seconds
        scene_tools.add_falling_object(self.timer, 720, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)
        # Add a new grey asteroid every 17 seconds
        scene_tools.add_falling_object(self.timer, 1020, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)

        # Add a new fragmenting asteroid every 25 seconds
        scene_tools.add_falling_object(self.timer, 1500, gameplay_items.FragmentingAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        # Add a new alien every 20 seconds
        scene_tools.add_falling_object(self.timer, 1200, gameplay_items.Alien, self.aliens, argument=self)

        # Add a new small asteroid every 30 seconds
        scene_tools.add_falling_object(self.timer, 1800, gameplay_items.MedAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.player,
                                                           self.score, self.lives, self.health, level_6.LevelSix)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose")

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)