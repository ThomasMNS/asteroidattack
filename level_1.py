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
    def __init__(self, ship, ship_2=None):

        self.player = ship
        # If there is only one player, self.player_2 = None
        self.player_2 = ship_2

        self.score = 0
        if self.player_2 is None:
            self.lives = 3
        else:
            self.lives = 2
        super().__init__(pygame.image.load('assets/black_stars.png').convert())

        # Initial Asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new asteroid every 8 seconds
        scene_tools.add_falling_object(self.timer, 480, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.player, self.player_2, self.score, self.lives,
                                                           level_2.LevelTwo)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose", self.player_2)

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)