""" Classes that create user interface scenes, for example menus. """

# Pygame
import pygame
# Standard library
import datetime
import pickle
# Game modules
import ui_items
import constants
import generic_scene
import scene_tools
import level_1
import training_scene
import customisation_scene
import settings_scene
# Third party Pygame modules
import eztext


class OpeningScene(generic_scene.GenericScene):
    """ The initial screen. Displays the UnderSand logo and loads the settings file. """
    def __init__(self):
        super().__init__()
        # Load the existing settings file
        try:
            # File loaded fine, unpickle settings dict into self.settings
            f = open('asteroid-attack-program-settings.p', 'rb')
            self.settings = pickle.load(f)
            f.close()
        except FileNotFoundError:
            # File does not exist (probably first load). Create the file, create a self.settings dict
            # and populate it with the default settings, then save the file
            f = open('asteroid-attack-program-settings.p', 'wb')
            self.settings = {"sound_volume": 50, "music_volume": 50, "menu_music_playing": False,
                             "level_music_playing": False}
            pickle.dump(self.settings, f)
            f.close()

        self.settings['menu_music_playing'] = False
        self.settings['level_music_playing'] = False

        # Load and play the waves sound
        self.waves = pygame.mixer.Sound('music/waves.ogg')
        self.waves.set_volume(self.settings['music_volume'] / 100)
        self.waves.play()

        # Load the logo image
        self.logo = pygame.image.load('assets/undersand_logo.png').convert()
        self.alpha = 0
        self.logo.set_alpha(self.alpha)

        # Create a timer, starting at 0
        self.timer = 0


    def handle_events(self, events):
        for event in events:
            # Skip intro if user presses a button or clicks mouse
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Stop the waves sound so it doesn't continue playing in the title scene
                self.waves.stop()
                self.next_scene = TitleScene(self.settings)

    def update(self):
        self.timer += 1

        # Black until 1 second

        # Fade in logo between 1 and 4 seconds
        if 60 < self.timer < 240:
            if self.alpha < 255:
                self.alpha += 2
                self.logo.set_alpha(self.alpha)

        # Fade out logo between 5.5 and 8.5 seconds
        elif 331 < self.timer < 510:
            if self.alpha > 0:
                self.alpha -= 2
                self.logo.set_alpha(self.alpha)

        # Next scene after 9 seoonds
        if self.timer >= 540:
            self.next_scene = TitleScene(self.settings)

    def draw(self, screen):
        screen.fill(constants.BLACK)
        screen.blit(self.logo, (237, 171))


class TitleScene(generic_scene.GenericScene):
    """ Contains buttons to navigate to other UI scenes. Shown after the dev logo. """
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        # Creating buttons
        self.button_color = constants.LIGHT_GREY
        self.button_hover_color = constants.DARK_GREY
        self.start_button = ui_items.RectangleHoverButton("Play", 300, 85, 362, 250, self.button_color,
                                                 self.button_hover_color)
        self.highscores_button = ui_items.RectangleHoverButton("High-Scores", 300, 85, 362, 345, self.button_color,
                                                      self.button_hover_color)
        self.settings_button = ui_items.RectangleHoverButton("Settings", 300, 85, 362, 440, self.button_color,
                                                      self.button_hover_color)
        self.instruction_button = ui_items.RectangleHoverButton("Help", 300, 85, 362, 535, self.button_color,
                                                       self.button_hover_color)
        self.end_button = ui_items.RectangleHoverButton("End", 300, 85, 362, 630, self.button_color,
                                                        self.button_hover_color)
        self.buttons = [self.start_button, self.highscores_button, self.settings_button,
                        self.instruction_button, self.end_button]
        self.background = pygame.image.load('assets/title_bg.png').convert()

        # Buttons sound
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

        # Creating and centering logo
        self.logo = pygame.image.load('assets/asteroid_attack_logo.png').convert_alpha()
        logo_size = self.logo.get_rect()
        self.logo_x = logo_size[2]
        self.logo_x = ((1024 / 2) - (self.logo_x / 2))

        self.timer = 0

        if self.settings['menu_music_playing'] is False:
            pygame.mixer.music.load('music/title_music.ogg')
            pygame.mixer.music.set_volume(self.settings['music_volume'] / 100)
            pygame.mixer.music.play(-1)
            self.settings['level_music_playing'] = False
            self.settings['menu_music_playing'] = True

    def handle_events(self, events):
        for event in events:
            # Checking if a button has been clicked on.
            # If it has, update the next scene
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = GameModeSelectionScene(self.settings)
                elif self.highscores_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = HighScoresScene(self.settings)
                elif self.settings_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = settings_scene.SettingsScene(self.settings)
                elif self.instruction_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = InstructionsScene(self.settings)
                elif self.end_button.mouse_over is True:
                    self.next_scene = None

    def update(self):
        # Pass the mouse location to the button objects.
        # They will then update self.mouse_over to be True or False
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())
        self.timer += 1

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, (300, 50))
        for button in self.buttons:
            button.draw_button(screen)


class HighScoresScene(generic_scene.GenericScene):
    """ Displays the contents of asteroid-attack-program-highscores.p and gives the option
    to replace the contents with a blank list. """
    def __init__(self, settings, highscore_to_highlight=None, players="single"):
        super().__init__()

        self.settings = settings

        # An item in high_score list may be passed if the previous scene was a game over.
        # This is highlighted in green in the draw method.
        self.highscore_to_highlight = highscore_to_highlight
        # Is the score to be highlighted single or multiplayer, so the correct tab is opened
        self.list_showing = players
        # Open the highscores list and store in highscores_list. If there is no highscores file (ie
        # the game has been started for the first time), make a blank list.
        try:
            f = open('asteroid-attack-program-highscores.p', 'rb')
            self.highscore_list = pickle.load(f)
            f.close()
        except FileNotFoundError:
            self.highscore_list = [[], []]

        self.single_highscores = self.highscore_list[0]
        self.multi_highscores = self.highscore_list[1]

        # Sort key to be passed to the sorted function
        def sort_by(item):
            return item[1]

        # Sort the highscores for display
        self.single_highscores = sorted(self.single_highscores, key=sort_by, reverse=True)
        self.multi_highscores = sorted(self.multi_highscores, key=sort_by, reverse=True)

        # Buttons
        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 202, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.clear_button = ui_items.RectangleHoverButton("Clear High-Scores", 300, 90, 522, 640, (constants.DARKER_RED),
                                                          (constants.DARK_GREY))

        self.single_button = ui_items.RectangleHoverButton("Single-Player", 140, 40, 300, 70, color=constants.DARK_GREY,
                                                           text_size=25)
        if self.list_showing == "multi":
            self.single_button.color = constants.LIGHT_GREY
            self.single_button.hover_color = constants.DARK_GREY

        self.multi_button = ui_items.RectangleHoverButton("Multi-Player", 140, 40, 450, 70, color=constants.LIGHT_GREY,
                                                          hover_color=constants.DARK_GREY, text_size=25)

        if self.list_showing == "multi":
            self.multi_button.color = constants.DARK_GREY
            self.multi_button.hover_color = constants.LIGHT_GREY

        self.buttons = [self.return_button, self.clear_button, self.single_button, self.multi_button]
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

        self.font = pygame.font.Font(None, 25)

        self.confirmation_popup = ui_items.Modal(["Are you sure you want to delete",
                                                  "all high-scores?",
                                                  "This will remove the contents of file",
                                                  "asteroid-attack-program-highscores.p"], 500, 300, 0,
                                                 0, 1024, 768, constants.LIGHT_GREY_2, constants.DARKER_GREY, "OK",
                                                 "Cancel")
        self.show_popup = False

    def handle_events(self, events):
        # If there is no popup, handle events as normal
        if self.show_popup is False:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.clear_button.mouse_over is True:
                        self.button_sound.play()
                        self.show_popup = True
                    elif self.return_button.mouse_over is True:
                        self.button_sound.play()
                        self.next_scene = TitleScene(self.settings)
                    elif self.single_button.mouse_over is True:
                        self.list_showing = "single"
                        self.single_button.color = constants.DARK_GREY
                        self.multi_button.color = constants.LIGHT_GREY
                    elif self.multi_button.mouse_over is True:
                        self.list_showing = "multi"
                        self.single_button.color = constants.LIGHT_GREY
                        self.multi_button.color = constants.DARK_GREY
        # If there is a popup, only input relating to the popup should be handled
        elif self.show_popup is True:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirmation_popup.button_1.mouse_over is True:
                        self.button_sound.play()
                        self.highscore_list = [[], []]
                        try:
                            f = open('asteroid-attack-program-highscores.p', 'wb')
                            pickle.dump(self.highscore_list, f)
                            f.close()
                        except:
                            pass
                        self.show_popup = False
                    elif self.confirmation_popup.button_2.mouse_over is True:
                        self.show_popup = False

    def update(self):
        if self.show_popup is False:
            for button in self.buttons:
                button.mouse_on_button(pygame.mouse.get_pos())
        else:
            self.confirmation_popup.update(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        # Highscores section background
        pygame.draw.rect(screen, constants.DARK_GREY, (300, 110, 420, 480))
        for button in self.buttons:
            button.draw_button(screen)
        if self.list_showing == "single":
            if len(self.single_highscores) > 0:
                y = 160
                rank = 1
                for score in self.single_highscores:
                    if score == self.highscore_to_highlight:
                        color = constants.BRIGHT_GREEN
                    else:
                        color = constants.WHITE
                    rank_text = "{0!s}.".format(rank)
                    rank_render = self.font.render(rank_text, True, color)
                    screen.blit(rank_render, (367, y))
                    name_text = "{0!s}".format(score[0])
                    name_render = self.font.render(name_text, True, color)
                    screen.blit(name_render, (367 + 40, y))
                    score_text = "{0!s}".format(score[1])
                    score_render = self.font.render(score_text, True, color)
                    screen.blit(score_render, (367 + 170, y))
                    date_text = "{0!s}".format(score[2])
                    date_render = self.font.render(date_text, True, color)
                    screen.blit(date_render, (367 + 230, y))
                    y += 40
                    rank += 1
            else:
                scene_tools.multiline_text(["No high-scores yet!", "Why don't you play and see how you do?"],
                                           340, 160, screen, constants.WHITE, 25)
        elif self.list_showing == "multi":
            if len(self.multi_highscores) > 0:
                y = 160
                rank = 1
                for score in self.multi_highscores:
                    if score == self.highscore_to_highlight:
                        color = constants.GREEN
                    else:
                        color = constants.WHITE
                    rank_text = "{0!s}.".format(rank)
                    rank_render = self.font.render(rank_text, True, color)
                    screen.blit(rank_render, (367, y))
                    name_text = "{0!s}".format(score[0])
                    name_render = self.font.render(name_text, True, color)
                    screen.blit(name_render, (367 + 40, y))
                    score_text = "{0!s}".format(score[1])
                    score_render = self.font.render(score_text, True, color)
                    screen.blit(score_render, (367 + 170, y))
                    date_text = "{0!s}".format(score[2])
                    date_render = self.font.render(date_text, True, color)
                    screen.blit(date_render, (367 + 230, y))
                    y += 40
                    rank += 1
            else:
                scene_tools.multiline_text(["No high-scores yet!", "Why don't you play and see how you do?"],
                                           340, 160, screen, constants.WHITE, 25)
        if self.show_popup is True:
            self.confirmation_popup.draw(screen)


class GameModeSelectionScene(generic_scene.GenericScene):
    """ A class for a screen with different buttons that can be clicked to take the user to
    different game mode scenes. """
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        # Images
        self.campaign_banner = pygame.image.load('assets/campaign_banner.png').convert_alpha()
        self.training_banner = pygame.image.load('assets/training_banner.png').convert_alpha()
        # Buttons
        self.campaign_button = ui_items.RectangleHoverButton("Campaign", 200, 70, 700, 210, constants.LIGHT_GREY,
                                                             constants.DARK_GREY, 30)
        self.training_button = ui_items.RectangleHoverButton("Training", 200, 70, 700, 510, constants.LIGHT_GREY,
                                                             constants.DARK_GREY, 30)
        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.buttons = [self.campaign_button, self.training_button, self.return_button]

        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

    def handle_events(self, events):
        for event in events:
            # Checking for clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.campaign_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = PlayerNumberScene("campaign", self.settings)
                elif self.training_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = PlayerNumberScene("training", self.settings)
                elif self.return_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = TitleScene(self.settings)

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        screen.blit(self.campaign_banner, (20, 20))
        screen.blit(self.training_banner, (20, 320))
        for button in self.buttons:
            button.draw_button(screen)

        scene_tools.multiline_text(["Battle asteroids and aliens in", "eight intense stages to",
                                                         "try and claim a high-score"], 665, 85, screen, constants.WHITE, 30)

        scene_tools.multiline_text(["Test your skills by creating", "your own customised",
                                                         "training simulation"], 665, 385, screen, constants.WHITE, 30)


class PlayerNumberScene(generic_scene.GenericScene):
    """ A class for a screen with buttons allowing the player to select single or multi-player mode. """
    def __init__(self, game_mode, settings):
        super().__init__()

        self.settings = settings

        self.game_mode = game_mode

        # Check if there is a joystick connected. To be used to check whether multiplaer can be selected.
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count >= 1:
            self.joystick_connected = True
        else:
            self.joystick_connected = False

        self.single_button = ui_items.RectangleHoverButton("One Player", 300, 90, 362, 400)
        if self.joystick_connected is True:
            self.multi_button = ui_items.RectangleHoverButton("Two Players", 300, 90, 362, 500)
        else:
            # If there is no joystick, display as greyed out
            self.multi_button = ui_items.RectangleHoverButton("Two Players", 300, 90, 362, 500, color=constants.DARK_GREY)
        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 600)
        self.buttons = [self.single_button, self.multi_button, self.return_button]
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

        # Tooltip
        self.multi_tip = ui_items.Tooltip(["No joystick", "detected"], 130, 70)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.single_button.mouse_over is True:
                self.button_sound.play()
                self.next_scene = customisation_scene.CustomisationScene(self.settings, self.game_mode, 1,
                                                                         self.settings)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.multi_button.mouse_over is True:
                if self.joystick_connected is True:
                    self.button_sound.play()
                    self.next_scene = customisation_scene.CustomisationScene(self.settings, self.game_mode, 2, 1,
                                                                             self.settings)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.return_button.mouse_over is True:
                self.button_sound.play()
                self.next_scene = GameModeSelectionScene(self.settings)

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())
        self.multi_tip.update()

        if self.multi_button.mouse_over is True:
            self.multi_tip.visible = True
        else:
            self.multi_tip.visible = False

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        for button in self.buttons:
            button.draw_button(screen)
        if self.multi_tip.visible is True and self.joystick_connected is False:
            self.multi_tip.draw(screen)


class TrainingSetupScene(generic_scene.GenericScene):
    """ A class for a screen that contains various UI components to change variables such as the number of
    asteroids, powerups etc. These are then passed to a training scene. """
    def __init__(self, ship, settings, ship_2=None):
        super().__init__()

        self.settings = settings

        self.ship = ship
        self.ship_2 = ship_2
        self.start_button = ui_items.RectangleHoverButton("Start", 300, 90, 202, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 202 + 20 + 300, 640, constants.DARKER_RED,
                                                           constants.DARK_RED)
        self.buttons = [self.start_button, self.return_button]
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

        self.column_1_x = 20
        self.column_spacing = 300

        self.row_1_y = 20
        self.row_spacing = 125

        self.brown_asteroid_toggle = ui_items.OptionButton(self.column_1_x, self.row_1_y, "Brown asteroids",
                                                           "No brown asteroids")
        self.brown_asteroid_toggle.value = 1
        self.brown_asteroid_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing, self.row_1_y, "brown asteroids to begin")
        self.brown_asteroid_time_selector = ui_items.NumberSelect(self.column_1_x + 2 * self.column_spacing,
                                                                  self.row_1_y, "seconds between new brown asteroids",
                                                                  default=10, min=1)

        self.grey_asteroid_toggle = ui_items.OptionButton(self.column_1_x, self.row_1_y + self.row_spacing, "Grey asteroids",
                                                           "No grey asteroids")
        self.grey_asteroid_toggle.value = 1
        self.grey_asteroid_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing, self.row_1_y + self.row_spacing, "grey asteroids to begin")
        self.grey_asteroid_time_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing * 2,
                                                                 self.row_1_y + self.row_spacing, "seconds between new grey asteroids",
                                                                 default=10, min=1)

        self.small_asteroid_toggle = ui_items.OptionButton(self.column_1_x, self.row_1_y + self.row_spacing * 2, "Small asteroids",
                                                           "No small asteroids")
        self.small_asteroid_toggle.value = 1
        self.small_asteroid_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing, self.row_1_y + self.row_spacing * 2, "small asteroids to begin")
        self.small_asteroid_time_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing * 2,
                                                                 self.row_1_y + self.row_spacing * 2, "seconds between new small asteroids",
                                                                  default=10, min=1)

        self.alien_toggle = ui_items.OptionButton(self.column_1_x, self.row_1_y + self.row_spacing * 3, "Aliens", "No aliens")
        self.alien_toggle.value = 1
        self.alien_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing, self.row_1_y + self.row_spacing * 3, "aliens to begin")
        self.alien_time_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing * 2,
                                                                 self.row_1_y + self.row_spacing * 3, "seconds between new aliens",
                                                         default=10, min=1)

        self.powerups_toggle = ui_items.OptionButton(self.column_1_x, self.row_1_y + self.row_spacing * 4, "Powerups",
                                                  "No powerups")
        self.lives_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing,
                                                    self.row_1_y + self.row_spacing * 4, "lives", default=3, min=1)
        self.health_selector = ui_items.NumberSelect(self.column_1_x + self.column_spacing * 2,
                                                    self.row_1_y + self.row_spacing * 4, "health", default=100,
                                                     min=10, max=1000, increment=10)

        self.persistent_components = [self.brown_asteroid_toggle, self.grey_asteroid_toggle, self.small_asteroid_toggle, self.alien_toggle,
                              self.powerups_toggle, self.lives_selector, self.health_selector]
        self.brown_asteroid_components = [self.brown_asteroid_selector, self.brown_asteroid_time_selector]
        self.grey_asteroid_components = [self.grey_asteroid_selector, self.grey_asteroid_time_selector]
        self.small_asteroid_components = [self.small_asteroid_selector, self.small_asteroid_time_selector]
        self.alien_components = [self.alien_selector, self.alien_time_selector]
        self.all_components = [self.persistent_components, self.brown_asteroid_components, self.grey_asteroid_components,
                               self.small_asteroid_components, self.alien_components]

    def handle_events(self, events):
        for list in self.all_components:
            for component in list:
                component.handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.mouse_over is True:
                    self.button_sound.play()
                    self.next_scene = GameModeSelectionScene(self.settings)
                elif self.start_button.mouse_over is True:
                    training_choices = [self.brown_asteroid_toggle.value, self.brown_asteroid_selector.value,
                                        self.brown_asteroid_time_selector.value,
                                        self.grey_asteroid_toggle.value, self.grey_asteroid_selector.value,
                                        self.grey_asteroid_time_selector.value,
                                        self.small_asteroid_toggle.value, self.small_asteroid_selector.value,
                                        self.small_asteroid_time_selector.value,
                                        self.alien_toggle.value, self.alien_selector.value,
                                        self.alien_time_selector.value,
                                        self.powerups_toggle.value, self.lives_selector.value,
                                        self.health_selector.value]
                    self.next_scene = GetReadyScene(self.settings, "training", self.ship, self.ship_2, training_choices)

    def update(self):
        for button in self.buttons:
            button.mouse_on_button(pygame.mouse.get_pos())

        for list in self.all_components:
            for component in list:
                component.update(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        for button in self.buttons:
            button.draw_button(screen)

        for component in self.persistent_components:
            component.draw(screen)

        if self.brown_asteroid_toggle.value == 0:
            for component in self.brown_asteroid_components:
                component.draw(screen)

        if self.grey_asteroid_toggle.value == 0:
            for component in self.grey_asteroid_components:
                component.draw(screen)

        if self.small_asteroid_toggle.value == 0:
            for component in self.small_asteroid_components:
                component.draw(screen)

        if self.alien_toggle.value == 0:
            for component in self.alien_components:
                component.draw(screen)


class InstructionsScene(generic_scene.GenericScene):
    """ A class for a screen outlining how to play the game. """
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 202, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.acknowledgements_button = ui_items.RectangleHoverButton("Acknowledgements", 300, 90, 522, 640, constants.LIGHT_GREY,
                                                                     constants.DARK_GREY)
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.return_button.mouse_over == True:
                self.button_sound.play()
                self.next_scene = TitleScene(self.settings)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.acknowledgements_button.mouse_over == True:
                self.button_sound.play()
                self.next_scene = AcknowledgementsScene(self.settings)

    def update(self):
        self.return_button.mouse_on_button(pygame.mouse.get_pos())
        self.acknowledgements_button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        self.return_button.draw_button(screen)
        self.acknowledgements_button.draw_button(screen)
        scene_tools.multiline_text(["Welcome to Asteroid Attack! Avoid the asteroids and angry aliens for as long as you can.",
                                    "Colliding with obstacles reduces your ship's health. When your health reaches zero you die,",
                                    "when you run out of lives, it's game over.",
                                    "",
                                    "Move your ship using the WASD keys. Use your laser cannon (space) to clear a path",
                                    "through the debris, but remember - you don't have many charges left.",
                                    "",
                                    "There are various powerups to help you on your way:",
                                    "- Red: Recharge Laser Cannon",
                                    "- Green: Increase speed for a limited time",
                                    "- Yellow: Restore health",
                                    "- Blue: Activate shield",
                                    "",
                                    "In campaign mode, battle your way through a series of stages to try and get a high-score.",
                                    "In training mode, test your skills by creating your own training simulation.",
                                    "",
                                    "Good luck!"], 50, 50, screen, constants.WHITE, 30)


class AcknowledgementsScene(generic_scene.GenericScene):
    """ A class for a scene that displays the credits. """
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.return_button.mouse_over is True:
                self.button_sound.play()
                self.next_scene = InstructionsScene(self.settings)

    def update(self):
        self.return_button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        self.return_button.draw_button(screen)
        scene_tools.multiline_text(["- Art assets: Kenney",
                                    "http://kenney.nl/assets (CC0 1.0)",
                                    "- Explosion animation: WrathGames Studio (wrathgames.com/blog)",
                                    "http://opengameart.org/content/wgstudio-explosion-animation (CC-BY 3.0)",
                                    "- Star collection sound: ProjectsU012",
                                    "https://www.freesound.org/people/ProjectsU012/sounds/341695/ (CC-BY 3.0)",
                                    "- Powerup sound: wildweasel",
                                    "https://www.freesound.org/people/wildweasel/sounds/39017/ (CC-BY 3.0)",
                                    "- Explosion sound: ryansnook",
                                    "https://www.freesound.org/people/ryansnook/sounds/110113/ (CC-BY-NC 1.0)",
                                    "- Alarm sound: jbum",
                                    "https://www.freesound.org/people/jbum/sounds/32089/ (CC-BY-NC 1.0)",
                                    "- Title music: maxstack",
                                    "http://opengameart.org/content/freelance (CC-BY-SA 3.0)",
                                    "- Level music: Arthur",
                                    "http://opengameart.org/content/space-walk (CC-BY-SA 3.0)",
                                    "",
                                    "https://creativecommons.org/publicdomain/zero/1.0/",
                                    "https://creativecommons.org/licenses/by/3.0/",
                                    "https://creativecommons.org/licenses/by-nc/3.0/"], 160, 30, screen, constants.WHITE, 25)


class GetReadyScene(generic_scene.GenericScene):
    """ Displayed before Level 1 begins to give the player a moment to prepare."""
    def __init__(self, settings, mode, ship, ship_2=None, choices=None):
        super().__init__()

        self.settings = settings

        self.mode = mode
        self.choices = choices
        self.ship = ship
        self.ship_2 = ship_2

        self.font = pygame.font.Font(None, 190)
        self.get_ready_text = "Get ready!"
        self.get_ready_render = self.font.render(self.get_ready_text, True, constants.WHITE)
        self.timer = 0

        if self.settings['level_music_playing'] is False and self.settings['menu_music_playing'] is True:
            # Get the volume of the title music
            self.volume = pygame.mixer.music.get_volume()
            self.volume_reduction_increment = self.volume / 10

        self.first_time = False

    def handle_events(self, events):
        pass

    def update(self):
        if self.settings['level_music_playing'] is False and self.settings['menu_music_playing'] is True:
            self.first_time = True
            # If the title music has not faded out yet
            if pygame.mixer.music.get_volume() - self.volume_reduction_increment > 0:
                if self.timer % 30 == 0:
                    self.volume -= self.volume_reduction_increment
                    pygame.mixer.music.set_volume(self.volume)
            # If the title music has faded out
            else:
                self.settings['menu_music_playing'] = False
        elif self.settings['level_music_playing'] is False and self.settings['menu_music_playing'] is False:
            pygame.mixer.music.load('music/level_music.ogg')
            pygame.mixer.music.set_volume(self.settings['music_volume'] / 100)
            pygame.mixer.music.play(-1)
            self.settings['level_music_playing'] = True

        # Display the screen for 4 seconds, then move to Level 1
        self.timer += 1

        if self.first_time == True:
            time = 600
        elif self.first_time == False:
            time = 300

        if self.timer > time:
            if self.mode == "campaign":
                self.next_scene = level_1.LevelOne(self.settings, self.ship, self.ship_2)
            elif self.mode == "training":
                self.next_scene = training_scene.TrainingScene(self.settings, self.ship, self.ship_2, self.choices)

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        screen.blit(self.get_ready_render, (185, 329))


class LevelCompleteScene(generic_scene.GenericScene):
    """ Displayed between levels. Shows the player's score and gives them a chance to prepare. """
    def __init__(self, settings, ship, ship_2, score, lives, level):
        super().__init__()
        self.settings = settings
        self.score = score
        self.lives = lives
        self.level = level
        self.timer = 0
        self.player = ship
        self.player_2 = ship_2

        self.font = pygame.font.Font(None, 150)
        self.smaller_font = pygame.font.Font(None, 60)
        self.get_ready_text = "Get ready!"
        self.get_ready_render = self.font.render(self.get_ready_text, True, constants.WHITE)

        score_text = "Score so far: {0!s}".format(self.score)
        self.score_render = self.smaller_font.render(score_text, True, constants.WHITE)

        lives_text = "Lives remaining: {0!s}".format(self.lives)
        self.lives_render = self.smaller_font.render(lives_text, True, constants.WHITE)

    def handle_events(self, events):
        """ No events, everything handled by the timer. """
        pass

    def update(self):
        self.timer += 1
        if self.timer > 240:
            self.next_scene = self.level(self.settings, self.player, self.player_2, self.score, self.lives)

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        screen.blit(self.get_ready_render, (260, 250))
        screen.blit(self.score_render, (344, 400))
        screen.blit(self.lives_render, (327, 475))


class GameOverScene(generic_scene.GenericScene):
    """ Reads the highscores and allows the user to enter a name for their
    highscore entry if they are in the top 10. Displays game over or congrats depending on what is passed
    to the constructor. """
    def __init__(self, score, game_over_type, player_2, settings):
        super().__init__()

        self.settings = settings

        self.score = score
        self.type = game_over_type
        if player_2 is None:
            self.players = "single"
        else:
            self.players = "multi"
        try:
            f = open('asteroid-attack-program-highscores.p', 'rb')
            self.high_scores_list = pickle.load(f)
            f.close()
        except FileNotFoundError:
            f = open('asteroid-attack-program-highscores.p', 'wb')
            f.close()
            self.high_scores_list = [[], []]
        except EOFError:
            self.high_scores_list = [[], []]

        # Sort by score (second item)
        def sort_by(item):
            return item[1]

        if self.players == "single":
            # If it's a single player game that has just finished, sort the first list in self.high_scores_list
            # which is for single player
            self.high_scores_list[0] = sorted(self.high_scores_list[0], key=sort_by, reverse=True)
            # Set self.high_scores_mod, which will be manipulated
            self.high_scores_mod = self.high_scores_list[0]
        else:
            # Otherwise, sort the second list, which is for multiplayer
            self.high_scores_list[1] = sorted(self.high_scores_list[1], key=sort_by, reverse=True)
            # Set self.high_scores_mod
            self.high_scores_mod = self.high_scores_list[1]

        # Find the lowest highscore
        if len(self.high_scores_mod) == 0:
            # No high scores, so lowest is zero
            lowest_high_score = 0
        else:
            # Otherwise, the last score in the list
            lowest_high_score = self.high_scores_mod[len(self.high_scores_mod) - 1][1]

        # Find out of the score is a highscore
        if (self.score > lowest_high_score) or (len(self.high_scores_mod) < 10):
            self.new_high_score = True
        else:
            self.new_high_score = False

        self.font = pygame.font.Font(None, 150)
        self.font_smaller = pygame.font.Font(None, 55)
        self.font_smallest = pygame.font.Font(None, 40)
        if self.type == "lose":
            self.game_over_text = "Game Over!"
        elif self.type == "win":
            self.game_over_text = "You win!"
        self.game_over_render = self.font.render(self.game_over_text, True, constants.WHITE)
        game_over_rect = self.game_over_render.get_rect()
        self.game_over_rect = game_over_rect.width
        self.game_over_x = (1024 / 2) - (self.game_over_rect / 2)
        self.score_text = "Your score: {0!s}".format(self.score)
        self.score_render = self.font_smaller.render(self.score_text, True, constants.WHITE)
        score_rect = self.score_render.get_rect()
        self.score_rect = score_rect.width
        self.score_x = (1024 / 2) - (self.score_rect / 2)

        if self.new_high_score is True:
            self.congratulations_text = "Congratulations! New high-score!"
            self.congratulations_render = self.font_smallest.render(self.congratulations_text, True, constants.WHITE)
            self.textbox = eztext.Input(maxlength = 20, color=constants.WHITE, prompt="Name: ", font=self.font_smallest)
            self.textbox.x = 30
            self.textbox.y = 350

            self.return_button = ui_items.RectangleHoverButton("Submit", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                      constants.DARK_GREY)
        else:
            self.return_button = ui_items.RectangleHoverButton("Return", 300, 100, 362, 620, constants.LIGHT_GREY,
                                                      constants.DARK_GREY)
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.return_button.mouse_over == True:
                self.button_sound.play()
                if self.new_high_score is True:
                    self.update_score()
                    self.next_scene = HighScoresScene(self.settings, self.score, self.players)
                else:
                    self.next_scene = TitleScene(self.settings)
        if self.new_high_score is True:
            self.textbox.update(events)

    def update(self):
        self.return_button.mouse_on_button(pygame.mouse.get_pos())
        if self.new_high_score is True:
            self.name = self.textbox.value

    def update_score(self):
        """ Called if there is a new high score"""
        if len(self.name) == 0:
            self.name = "Unknown"
        # Create a list to store name, score and date
        self.score = [self.name, self.score, datetime.date.today().strftime("%d / %m / %Y")]
        # Cut off the last high score, since a new one is being added
        self.high_scores_mod = self.high_scores_mod[:9]
        self.high_scores_mod.append(self.score)
        if self.players == "single":
            new_high_scores = [self.high_scores_mod, self.high_scores_list[1]]
        else:
            new_high_scores = [self.high_scores_list[0], self.high_scores_mod]
        try:
            f = open('asteroid-attack-program-highscores.p', 'wb')
            pickle.dump(new_high_scores, f)
            f.close()
        except:
            pass

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        screen.blit(self.game_over_render, (self.game_over_x, 30))
        screen.blit(self.score_render, (self.score_x, 150))
        self.return_button.draw_button(screen)
        if self.new_high_score is True:
            screen.blit(self.congratulations_render, (30, 300))
            self.textbox.draw(screen)


class TrainingGameOverScene(generic_scene.GenericScene):
    """ Displays game over. """
    def __init__(self, score, game_over_type, settings):
        super().__init__()

        self.settings = settings

        self.score = score
        self.type = game_over_type
        self.font = pygame.font.Font(None, 150)
        self.font_smaller = pygame.font.Font(None, 55)

        self.simulation_render = self.font.render("Simulation", True, constants.WHITE)
        simulation_rect = self.simulation_render.get_rect()
        self.simulation_rect = simulation_rect.width
        self.simulation_x = (1024 / 2) - (self.simulation_rect / 2)

        self.complete_render = self.font.render("complete", True, constants.WHITE)
        complete_rect = self.complete_render.get_rect()
        self.complete_rect = complete_rect.width
        self.complete_x = (1024 / 2) - (self.complete_rect / 2)

        # Score text
        score_text = "Score: {0!s}".format(self.score)
        self.score_render = self.font_smaller.render(score_text, True, constants.WHITE)
        score_rect = self.score_render.get_rect()
        self.score_rect = score_rect.width
        self.score_x = (1024 / 2) - (self.score_rect / 2)

        self.return_button = ui_items.RectangleHoverButton("Return", 300, 90, 362, 640, constants.LIGHT_GREY,
                                                           constants.DARK_GREY)
        self.button_sound = pygame.mixer.Sound('music/button.ogg')
        self.button_sound.set_volume(self.settings['sound_volume'] / 100)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.return_button.mouse_over is True:
                self.button_sound.play()
                self.next_scene = TitleScene(self.settings)

    def update(self):
        self.return_button.mouse_on_button(pygame.mouse.get_pos())

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)
        # Complete text
        screen.blit(self.simulation_render, (self.simulation_x, 30))
        screen.blit(self.complete_render, (self.complete_x, 150))
        screen.blit(self.score_render, (self.score_x, 330))
        self.return_button.draw_button(screen)

