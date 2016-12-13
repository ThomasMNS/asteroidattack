""" Helper functions, useful when creating scenes."""

# Pygame
import pygame
# Standard library
import random
# Game modules
import gameplay_items


def multiline_text(text_list, x, y, screen, color, size):
    """ Accepts a list of text and draws each item on a new line. """
    spacing = 10
    font = pygame.font.Font(None, size)
    for line in text_list:
        size = font.size(line)
        line_height = size[1]
        render = font.render(line, True, color)
        screen.blit(render, (x, y))
        y += line_height
        y += spacing


def initial_falling_objects(count, obj_class, container_1, container_2=None, container_3=None,
                            min_y=-2000, max_y=-200, argument=None):
    """ Creates a given number of existing sprite objects, and adds them to sprite groups. """
    for i in range(count):
        if argument is None:
            funcobj = obj_class()
        else:
            funcobj = obj_class(argument)
        funcobj.rect.x = random.randrange(0, 1024)
        funcobj.rect.y = random.randrange(min_y, max_y)
        container_1.add(funcobj)
        if container_2 is not None:
            container_2.add(funcobj)
        if container_3 is not None:
            container_3.add(funcobj)


def add_falling_object(timer, time, obj_class, container_1, container_2=None,
                       container_3=None, min_x=-2000, max_x = -200, argument=None):
    """ Creates a given existing sprite every x time and adds it to sprite groups. """
    if timer % time == 0:
        if argument is None:
            funcobj = obj_class()
        else:
            funcobj = obj_class(argument)
        funcobj.rect.x = random.randrange(0, 1024)
        funcobj.rect.y = random.randrange(min_x, max_x)
        container_1.add(funcobj)
        if container_2 is not None:
            container_2.add(funcobj)
        if container_3 is not None:
            container_3.add(funcobj)


def death_scene_reset(groups, player):
    """ Takes a list of sprite groups and a player sprite and changes their positions to reset the
    scene after death. """
    for group in groups:
        for sprite in group:
            sprite.rect.y -= 1000

    x = random.randrange(200, 800)
    player.update_pos(x, 600)
    player.speed_boosted = False