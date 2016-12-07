""" Scene for allowing players to change the appearance of their ship. """

#  Pygame
import pygame
# Game modules
import generic_scene
import constants
import gameplay_items
import ui_items


class CustomisationScene(generic_scene.GenericScene):
    """ Class for a scene allowing players to change the appearance of their ship. """
    def __init__(self):
        super().__init__()
        # Place a player ship in the middle of the scene
        self.ship = gameplay_items.PlayerShip()
        self.ship.rect.x = 512 - (self.ship.rect.width / 2)
        self.ship.rect.y = 384 - (self.ship.rect.height / 2)
        self.ship_group = pygame.sprite.Group(self.ship)

        # Button
        self.button = ui_items.RectangleHoverButton("Change", 300, 100, 10, 10)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.button.mouse_over is True:
                self.ship.update_appearance('assets/player_ship/playerShip2_orange.png')
                self.ship.rect.x = 512 - (self.ship.rect.width / 2)
                self.ship.rect.y = 384 - (self.ship.rect.height / 2)

    def update(self):
        self.button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        self.ship_group.draw(screen)
        self.button.draw_button(screen)