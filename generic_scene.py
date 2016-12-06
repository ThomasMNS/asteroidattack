""" A class that all game scenes inherit from."""

# Pygame
import pygame


# Class definitions
# Defining a generic base scene. Game scenes are children of this.
class GenericScene:
    """ A generic base class. Game scenes are children of this.
     Essentially, ensures all scenes have a next_scene attribute, and
      handle_events, update and draw methods. """
    def __init__(self):
        # By default, the next scene is the same as the current scene
        self.next_scene = self
        pygame.mouse.set_visible(True)

    def handle_events(self, events):
        """ Go through the filtered event list and deal with the events there."""
        # Print an error message so overridding this is not forgotten.
        print("Info - handle_events in GenericScene has not been overridden.")

    def update(self):
        """ Updates and game logic are handled here. For example, changing the position of a sprite. """
        # Print an error message so overridding this is not forgotten.
        print("Info - update in GenericScene has not been overridden.")

    def draw(self, screen):
        """ Draw the frame. E.g. blitting sprites and text. Updating the screen and
         handling the loop is taken care of in the main loop. """
        # Print an error message so overridding this is not forgotten.
        print("Info - draw in GenericScene has not been overridden.")