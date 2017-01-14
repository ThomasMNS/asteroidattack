""" Level 3 of Asteroid Attack. """

# Pygame
import pygame
# Game modules
import game_scene
import ui_scenes
import gameplay_items
import scene_tools
import level_4


class LevelThree(game_scene.GameScene):
    """ Class for level 3. """
    def __init__(self, ship, ship_2, score, lives):
        self.player = ship
        self.player_2 = ship_2
        super().__init__(pygame.image.load('assets/dark_blue_stars.png').convert())
        # Fill it with brown asteroids
        scene_tools.initial_falling_objects(2, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)
        # Fill it with grey asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

        # Fill it with fragmenting asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.FragmentingAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

        self.score = score
        self.lives = lives

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 8 seconds
        scene_tools.add_falling_object(self.timer, 480, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)
        # Add a new grey asteroid every 15 seconds
        scene_tools.add_falling_object(self.timer, 900, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)

        # Add a new fragmenting asteroid every 25 seconds
        scene_tools.add_falling_object(self.timer, 1500, gameplay_items.FragmentingAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        if self.timer == 5000:
            self.next_scene = ui_scenes.LevelCompleteScene(self.player, self.player_2, self.score, self.lives,
                                                           level_4.LevelFour)

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose", self.player_2)

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)