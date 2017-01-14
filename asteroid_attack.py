""" The main function for Asteroid Attack. Initiates the Pygame window, plays title music
and runs the main game loop. """

# Asteroid Attack - a scrolling space shooter
# Thomas Burke - thomasmns.com
# 14/11/2016
# V1.1 18/12/2016

# Importing required modules
# Pygame
import pygame
# Game modules
import ui_scenes


def main():
    """ Initiates Pygame and the main game loop. """
    # Initiate the Pygame modules
    pygame.init()

    # Set up the screen
    screen_width = 1024
    screen_height = 768
    icon = pygame.image.load('assets/window_icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen_caption = "Asteroid Attack!"
    pygame.display.set_caption(screen_caption)

    # Set up the main game loop
    clock = pygame.time.Clock()
    active_scene = ui_scenes.TitleScene()

    # Main game loop
    while active_scene is not None:
        filtered_events = []
        # Game-wide events that should be handled the same, no-matter what the scene is
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_scene.next_scene = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active_scene.next_scene = None
                else:
                    filtered_events.append(event)
            else:
                filtered_events.append(event)

        # Process events in the filtered event queue
        active_scene.handle_events(filtered_events)

        # Process updates and game logic. E.g. moving sprites
        active_scene.update()

        # Draw the frame
        active_scene.draw(screen)

        # Change the scene. By default, next_scene = self i.e the scene does not change
        active_scene = active_scene.next_scene

        # Update the screen
        pygame.display.flip()

        # Run the game at 60 fps
        clock.tick(60)

# Run the game if this file has not been imported
if __name__ == "__main__":
    main()


