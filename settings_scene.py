""" Scene for allowing players to change game settings. """

# Pygame
import pygame
# Game modules
import generic_scene
import ui_items
import constants
import ui_scenes
# Standard library
import pickle


class SettingsScene(generic_scene.GenericScene):
    """ Class for a scene allowing players to change game settings. """
    def __init__(self):
        super().__init__()

        # Buttons
        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.buttons = [self.return_button]

        # Text
        self.header_font = pygame.font.Font(None, 45)
        self.header_render = self.header_font.render("Audio Settings", True, constants.WHITE)
        self.header_rect = self.header_render.get_rect()

        self.font = pygame.font.Font(None, 25)
        self.volume_render = self.font.render("Sound volume", True, constants.WHITE)

        # Load the existing settings file, if possible
        try:
            f = open('asteroid-attack-program-settings.p', 'rb')
            self.settings = pickle.load(f)
            f.close()
        except FileNotFoundError:
            f = open('asteroid-attack-program-settings.p', 'wb')
            f.close()
            self.settings = {"sound_volume": 50}
        except EOFError:
            self.settings = {"sound_volume": 50}

        # Create a slider, showing the value loaded from the file
        self.slider = ui_items.Slider(100, 250, 200, 0, 100, self.settings["sound_volume"])

    def handle_events(self, events):
        for event in events:
            self.slider.handle_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.mouse_over is True:
                    self.save_settings()
                    self.next_scene = ui_scenes.TitleScene()

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())

        self.slider.update()

    def draw(self, screen):
        # Background
        screen.fill(constants.DARKER_GREY)

        for button in self.buttons:
            button.draw_button(screen)

        screen.blit(self.header_render, ((1024 / 2) - (self.header_rect.width / 2), 40))
        screen.blit(self.volume_render, (100, 200))
        self.slider.draw(screen)

    def save_settings(self):
        self.settings["sound_volume"] = self.slider.value
        f = open('asteroid-attack-program-settings.p', 'wb')
        pickle.dump(self.settings, f)
        f.close()