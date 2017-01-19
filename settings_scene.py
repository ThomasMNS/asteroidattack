""" Scene for allowing players to change game settings. """

# Game modules
import pygame
import generic_scene
import ui_items
import constants
import ui_scenes


class SettingsScene(generic_scene.GenericScene):
    """ Class for a scene allowing players to change game settings. """
    def __init__(self):
        super().__init__()

        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.buttons = [self.return_button]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.mouse_over is True:
                    self.next_scene = ui_scenes.TitleScene()

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        # Background
        screen.fill(constants.DARKER_GREY)

        for button in self.buttons:
            button.draw_button(screen)