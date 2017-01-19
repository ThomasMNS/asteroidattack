""" A level for testing. """

# Pygame
import pygame
# Game modules
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