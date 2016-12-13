# """ A level for testing. """
#
# # Pygame
# import pygame
# # Game modules
# import level_2
# import game_scene
# import ui_scenes
# import gameplay_items
# import scene_tools
#
#
# class TestLevel(game_scene.GameScene):
#     """ Class for a level for testing things. """
#     def __init__(self, ship):
#         self.score = 0
#         self.lives = 3
#         self.health = 100
#         self.player = ship
#         super().__init__(pygame.image.load('assets/black_stars.png').convert())
#
#         # Initial fragmenting asteroids
#         scene_tools.initial_falling_objects(5, gameplay_items.FragmentingAsteroid, self.all_sprites, argument=self)
#
#     def handle_events(self, events):
#         super().handle_events(events)
#
#     def update(self):
#         super().update()
#
#         if self.timer == 5000:
#             self.next_scene = ui_scenes.LevelCompleteScene(self.player, self.score, self.lives, self.health,
#                                                            level_2.LevelTwo)
#
#         if self.lives == 0:
#             self.next_scene = ui_scenes.GameOverScene(self.score, "lose")
#
#     def draw(self, screen):
#         super().draw(screen)
#         self.all_sprites.draw(screen)
#         self.collectible_stars.draw(screen)
#
#         # Drawing UI text needs to be done after everything else so that it is on top
#         game_scene.GameScene.draw_text(self, screen)

""" Level 8 of Asteroid Attack. """
import pygame
import game_scene
import ui_scenes


class TestLevel(game_scene.GameScene):
    def __init__(self, ship):
        self.player = ship
        super().__init__(pygame.image.load('assets/black_stars.png').convert())

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()
        self.next_scene = ui_scenes.TitleScene()

    def draw(self, screen):
        super().draw(screen)