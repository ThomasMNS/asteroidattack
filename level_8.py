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
    def __init__(self, ship, ship_2, score, lives):
        self.player = ship
        self.player_2 = ship_2
        super().__init__(pygame.image.load('assets/purple_stars.png').convert())
        self.score = score
        self.lives = lives

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

        # Fill it with strong asteroids
        scene_tools.initial_falling_objects(1, gameplay_items.StrongAsteroid, self.all_sprites, self.asteroids,
                                            argument=self)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        # Add a new brown asteroid every 10 seconds
        scene_tools.add_falling_object(self.timer, 600, gameplay_items.BrownAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)
        # Add a new grey asteroid every 12 seconds
        scene_tools.add_falling_object(self.timer, 720, gameplay_items.GreyAsteroid, self.all_sprites, self.asteroids,
                                       argument=self)

        # Add a new fragmenting asteroid every 20 seconds
        scene_tools.add_falling_object(self.timer, 1200, gameplay_items.FragmentingAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        # Add a new alien every 15 seconds
        scene_tools.add_falling_object(self.timer, 900, gameplay_items.Alien, self.aliens, argument=self)

        # Add a new small asteroid every 30 seconds
        scene_tools.add_falling_object(self.timer, 1800, gameplay_items.MedAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        # Add a new strong asteroid every 30 seconds
        scene_tools.add_falling_object(self.timer, 1800, gameplay_items.StrongAsteroid, self.all_sprites,
                                       self.asteroids, argument=self)

        # Single or multiplayer (for highscores)
        if self.player_2 is None:
            players = "single"
        else:
            players = "multi"

        if self.lives == 0:
            self.next_scene = ui_scenes.GameOverScene(self.score, "lose", players)

        if self.timer == 5000:
            self.next_scene = ui_scenes.GameOverScene(self.score, "win", players)

    def draw(self, screen):
        super().draw(screen)
        self.all_sprites.draw(screen)
        self.collectible_stars.draw(screen)
        # Drawing UI text needs to be done after everything else so that it is on top
        game_scene.GameScene.draw_text(self, screen)