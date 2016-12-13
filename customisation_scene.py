""" Scene for allowing players to change the appearance of their ship. """

#  Pygame
import pygame
# Game modules
import generic_scene
import constants
import gameplay_items
import ui_items
import ui_scenes
import test_level


class CustomisationScene(generic_scene.GenericScene):
    """ Class for a scene allowing players to change the appearance of their ship. """
    def __init__(self, next_level):
        super().__init__()

        self.next_level = next_level

        # Place a player ship in the middle of the scene
        self.ship = gameplay_items.PlayerShip()
        self.ship.rect.x = 512 - (self.ship.rect.width / 2)
        self.ship.rect.y = 480
        self.ship_group = pygame.sprite.Group(self.ship)

        # Buttons
        # Ship class
        self.nova_button = ui_items.RectangleHoverButton("Nova", 300, 90, 42, 90)
        self.nebula_button = ui_items.RectangleHoverButton("Nebula", 300, 90, 362, 90)
        self.galaxy_button = ui_items.RectangleHoverButton("Galaxy", 300, 90, 682, 90)

        # Color
        self.blue_button = ui_items.RectangleHoverButton("", 90, 90, 302, 310, constants.SHIP_BLUE,
                                                         constants.SHIP_BLUE)
        self.green_button = ui_items.RectangleHoverButton("", 90, 90, 412, 310, constants.SHIP_GREEN,
                                                          constants.SHIP_GREEN)
        self.orange_button = ui_items.RectangleHoverButton("", 90, 90, 522, 310, constants.SHIP_ORANGE,
                                                           constants.SHIP_ORANGE)
        self.red_button = ui_items.RectangleHoverButton("", 90, 90, 632, 310, constants.SHIP_RED,
                                                        constants.SHIP_RED)

        # Start
        self.start_button = ui_items.RectangleHoverButton("Start", 300, 90, 362, 640)

        self.buttons = [self.nova_button, self.nebula_button, self.galaxy_button,
                        self.blue_button, self.green_button, self.orange_button, self.red_button,
                        self.start_button]

        # Text
        font = pygame.font.Font(None, 45)
        self.class_text = font.render("Ship class", True, constants.WHITE)
        self.class_text_x = (1024 / 2) - (self.class_text.get_rect().width / 2)
        self.class_text_y = (90 / 2) - (self.class_text.get_rect().height / 2)

        self.color_text = font.render("Ship colour", True, constants.WHITE)
        self.color_text_x = (1024 / 2) - (self.color_text.get_rect().width / 2)
        self.color_text_y = 220 + (90 / 2) - (self.color_text.get_rect().height / 2)

        # Customisation selections
        self.ship_class = "2"
        self.ship_color = "red"
        self.ship_changed = False

    def handle_events(self, events):
        for event in events:
            # Check for button presses and update ship choice accordingly
            # Class
            if event.type == pygame.MOUSEBUTTONDOWN and self.nova_button.mouse_over is True:
                self.ship_class = "1"
                self.ship_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.nebula_button.mouse_over is True:
                self.ship_class = "2"
                self.ship_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.galaxy_button.mouse_over is True:
                self.ship_class = "3"
                self.ship_changed = True
            # Colour
            elif event.type == pygame.MOUSEBUTTONDOWN and self.blue_button.mouse_over is True:
                self.ship_color = "blue"
                self.ship_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.green_button.mouse_over is True:
                self.ship_color = "green"
                self.ship_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.orange_button.mouse_over is True:
                self.ship_color = "orange"
                self.ship_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.red_button.mouse_over is True:
                self.ship_color = "red"
                self.ship_changed = True
            # Start
            elif event.type == pygame.MOUSEBUTTONDOWN and self.start_button.mouse_over is True:
                if self.next_level == "campaign":
                    self.next_scene = ui_scenes.GetReadyScene("campaign", self.ship)
                elif self.next_level == "training":
                    self.next_scene = ui_scenes.TrainingSetupScene(self.ship)
            # Testing
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.next_scene = test_level.TestLevel(self.ship)

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())

        if self.ship_changed is True:
            self.ship.update_appearance('assets/player_ship/playerShip{0}_{1}.png'.format(self.ship_class,
                                                                                          self.ship_color))
            self.ship_changed = False

    def draw(self, screen):
        # Background
        screen.fill(constants.DARKER_GREY)

        # Buttons
        for button in self.buttons:
            button.draw_button(screen)

        # Ship
        self.ship_group.draw(screen)

        # Text
        screen.blit(self.class_text, (self.class_text_x, self.class_text_y))
        screen.blit(self.color_text, (self.color_text_x, self.color_text_y))