""" Classes for creating interfaces. E.g. buttons etc. """

# Pygame
import pygame
# Game modules
import constants
import scene_tools


class Button:
    """ A button for use in menus and other interfaces. """
    def __init__(self, text, width, height, x, y, text_size=35):
        # Input attributes
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, text_size)

        # None input attributes
        self.mouse_over = False

        # Calculated attributes
        self.button_area = ((self.x, self.y), (self.x + self.width, self.y), (self.x, self.y + self.height,
                                                                         self.x + self.width, self.y + self.height))

    def draw_button(self, screen):
        render = self.font.render(self.text, True, (255, 255, 255))
        text_size = self.font.size(self.text)
        text_width = text_size[0]
        x = (self.width / 2) - (text_width / 2)
        text_height = text_size[1]
        y = (self.height / 2) - (text_height / 2)
        screen.blit(render, (x + self.x, y + self.y))

    def mouse_on_button(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        start_button_area = self.button_area
        if (start_button_area[0][0] <= mouse_x <= start_button_area[1][0]) and (start_button_area[0][1] <= mouse_y <= start_button_area[2][1]):
            self.mouse_over = True
        else:
            self.mouse_over = False


class RectangleHoverButton(Button):
    """ A rectangular button which changes colour on mouseover, for use in menus and other interfaces. """
    def __init__(self, text, width, height, x, y, color, hover_color, text_size=35):
        super().__init__(text, width, height, x, y, text_size)
        self.color = color
        self.hover_color = hover_color

    def draw_button(self, screen):
        if self.mouse_over is True:
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        super().draw_button(screen)


class Popup:
    """ A coloured box that displays some text. Positioned at a given XY location, unless
    screen dimensions are given, where it is centered. """
    def __init__(self, text, width, height, x, y, window_width=None,
                 window_height=None, bg_color=constants.LIGHT_GREY_2):
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height
        # If no screen dimensions are given, place at given XY location
        if self.window_width is None and self.window_height is None:
            self.x = x
            self.y = y
        # If screen dimensions are given, center
        else:
            self.x = (self.window_width / 2) - (self.width / 2)
            self.y = (self.window_height / 2) - (self.height / 2)
        self.bg_color = bg_color
        self.text = text
        self.showing = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        scene_tools.multiline_text(self.text, self.x + 10, self.y + 50, screen, constants.WHITE, 35)


class Modal(Popup):
    """ A coloured box that displays some text and fades out the rest of the screen.
    Two buttons can be optionally defined. """
    def __init__(self, text, width, height, x, y, window_width=None, window_height=None, bg_color=constants.LIGHT_GREY_2,
                 fade_color=constants.DARKER_GREY, button_1_text=None, button_2_text=None):
        super().__init__(text, width, height, x, y, window_width, window_height, bg_color)

        self.fade_color = fade_color
        self.button_1_text = button_1_text
        self.button_2_text = button_2_text

        # Create a rectangle to cover the screen, fading it out
        self.background_fade_surface = pygame.Surface((1024, 768))
        self.background_fade_surface.set_alpha(190)
        self.background_fade_surface.fill(self.fade_color)

        # Check how many buttons the user has defined
        if self.button_1_text is None and self.button_2_text is None:
            self.no_of_buttons = 0
        elif self.button_1_text is not None and self.button_2_text is None:
            self.no_of_buttons = 1
        else:
            self.no_of_buttons = 2

        # If there is just one button, place it in the middle
        if self.no_of_buttons == 1:
            button_1_x = self.x + ((self.width / 2) - (100 / 2))
            button_1_y = (self.y + self.height - 30 - 20)
            self.button_1 = RectangleHoverButton(self.button_1_text, 100, 30, button_1_x, button_1_y,
                                                 constants.LIGHT_GREY, constants.DARK_GREY, 20)
        elif self.no_of_buttons == 2:
            # If there are two buttons, place them in the middle
            button_1_x = self.x + ((self.width / 2) - (215 / 2))
            button_1_y = (self.y + self.height - 30 - 20)
            button_2_x = button_1_x + 115
            button_2_y = button_1_y
            self.button_1 = RectangleHoverButton(self.button_1_text, 100, 30, button_1_x, button_1_y,
                                                 constants.LIGHT_GREY, constants.DARK_GREY, 20)
            self.button_2 = RectangleHoverButton(self.button_2_text, 100, 30, button_2_x, button_2_y,
                                                 constants.LIGHT_GREY, constants.DARK_GREY, 20)

    def update(self, mouse_pos):
        if self.no_of_buttons == 1:
            self.button_1.mouse_on_button(mouse_pos)
        elif self.no_of_buttons == 2:
            self.button_1.mouse_on_button(mouse_pos)
            self.button_2.mouse_on_button(mouse_pos)

    def draw(self, screen):
        screen.blit(self.background_fade_surface, (0, 0))
        super().draw(screen)
        if self.no_of_buttons == 1:
            self.button_1.draw_button(screen)
        elif self.no_of_buttons == 2:
            self.button_1.draw_button(screen)
            self.button_2.draw_button(screen)


class NumberSelect:
    """ A UI component for selecting a number. Users may press up and down arrows to increase or decrease
    the number. The number is stored as an attribute. """
    def __init__(self, x, y, text="None", default=0, min=0, max=100, increment=1):
        self.x = x
        self.y = y
        self.value = default
        if min > self.value:
            self.value = min
        self.min = min
        self.max = max
        self.increment = increment
        self.increase_button = RectangleHoverButton("", 55, 30, self.x, self.y, constants.LIGHT_GREY,
                                                    constants.DARK_GREY)
        self.decrease_button = RectangleHoverButton("", 55, 30, self.x, self.y + 75, constants.LIGHT_GREY,
                                                    constants.DARK_GREY)
        self.font = pygame.font.Font(None, 25)

        self.text = text
        if text is not None:
            self.text_render = self.font.render(text, True, constants.WHITE)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.increase_button.mouse_over is True:
                self.value += self.increment
            elif event.type == pygame.MOUSEBUTTONDOWN and self.decrease_button.mouse_over is True:
                self.value -= self.increment

    def update(self, mouse_pos):
        self.increase_button.mouse_on_button(mouse_pos)
        self.decrease_button.mouse_on_button(mouse_pos)
        if self.value < self.min:
            self.value = self.min
        elif self.value > self.max:
            self.value = self.max

    def draw(self, screen):
        self.increase_button.draw_button(screen)
        self.decrease_button.draw_button(screen)
        pygame.draw.rect(screen, constants.LIGHT_GREY_2, (self.x, self.y + 30, 55, 45))
        value = str(self.value)
        render = self.font.render(value, True, constants.WHITE)
        text_rect = render.get_rect()
        x = ((55 / 2) - (text_rect[2] / 2)) + self.x
        y = (45 / 2) - (text_rect[3] / 2) + self.y + 31
        screen.blit(render, (x, y))
        x = ((55 / 2) - (20 / 2))
        y = ((30 / 2) - (15 / 2))
        pygame.draw.polygon(screen, constants.LIGHTER_GREY, ((self.x + x, self.y + 15 + y), (self.x + x + 10, self.y + y), (self.x + x + 20, self.y + 15 + y)))
        pygame.draw.polygon(screen, constants.LIGHTER_GREY, (
        (self.x + x, self.y + y + 75), (self.x + x + 10, self.y + 15 + y + 75), (self.x + x + 20, self.y + y + 75)))

        if self.text is not None:
            screen.blit(self.text_render, (self.x + 70, self.y + 45))


class OptionButton:
    """ A UI component consisting of two circles, which can be clicked to select an option. """
    def __init__(self, x, y, text_1, text_2):
        self.value = 0
        self.mouse_on_0 = False
        self.mouse_on_1 = False

        self.x = x
        self.y = y

        self.text_1 = text_1
        self.text_2 = text_2
        self.font = pygame.font.Font(None, 25)
        self.text_1_render = self.font.render(self.text_1, True, constants.WHITE)
        self.text_2_render = self.font.render(self.text_2, True, constants.WHITE)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_on_0 is True:
                self.value = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and self.mouse_on_1 is True:
                self.value = 1

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        if (self.x <= mouse_x <= self.x + 30) and (self.y <= mouse_y <= self.y + 30):
            self.mouse_on_0 = True
        else:
            self.mouse_on_0 = False

        if (self.x <= mouse_x <= self.x + 30) and (self.y + 40 <= mouse_y <= self.y + 40 + 30):
            self.mouse_on_1 = True
        else:
            self.mouse_on_1 = False

    def draw(self, screen):
        if self.value == 0:
            circle_0_width = 0
            circle_1_width = 5
        else:
            circle_0_width = 5
            circle_1_width = 0
        pygame.draw.ellipse(screen, constants.LIGHT_GREY, (self.x, self.y, 30, 30), circle_0_width)
        pygame.draw.ellipse(screen, constants.LIGHT_GREY, (self.x, self.y + 40, 30, 30), circle_1_width)
        screen.blit(self.text_1_render, (self.x + 40, self.y + 7))
        screen.blit(self.text_2_render, (self.x + 40, self.y + 47))