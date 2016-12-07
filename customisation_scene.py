""" Scene for allowing players to change the appearance of their ship. """

# Game modules
import generic_scene
import constants


class CustomisationScene(generic_scene.GenericScene):
    """ Class for a scene allowing players to change the appearance of their ship. """
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(constants.DARKER_GREY)