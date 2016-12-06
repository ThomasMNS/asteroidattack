""" Classes used to create objects to populate gameplay levels. This includes the player (ship),
obstacles (E.g. asteroids), powerups (E.g. speed boost) and scenery (E.g. stars). """

# Pygame
import pygame
# Game modules
import random


# Gameplay
class PlayerShip(pygame.sprite.Sprite):
    """ Player ship. Instantiated in a game scene. Moves around, can generate a shield. """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/blue_ship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4
        self.x_speed = 0
        self.y_speed = 0

        # Powerups
        self.speed_boosted = False
        self.speed_boost_timer = 0

        # Weapons
        self.lasers = 5

        # Shield
        self.shield = None

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.shield is not None:
            self.shield.update_pos(self)

    def create_shield(self, sprite_group):
        self.shield = Shield(self)
        sprite_group.add(self.shield)


class Shield(pygame.sprite.Sprite):
    """ Appears around a PlayerShip() instance. """
    def __init__(self, ship):
        super().__init__()
        self.image = pygame.image.load('assets/shield.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 10)

    def update_pos(self, ship):
        self.rect.x = ship.rect.x - 17
        self.rect.y = ship.rect.y - 32


class Laser(pygame.sprite.Sprite):
    """ Moves upwards. Instantiated at player ship location. """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/laser_red.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = -7
        self.rect.x = x
        self.rect.y = y
        self.sound = pygame.mixer.Sound('music/laser.ogg')
        self.sound.play()

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -100:
            self.kill()


class BrownAsteroid(pygame.sprite.Sprite):
    """ Large sprite that moves slowly down the screen. """
    def __init__(self):
        super().__init__()
        randnum = random.randrange(0, 4)
        if randnum == 0:
            self.image = pygame.image.load('assets/meteor_brown_big_1.png').convert_alpha()
        elif randnum == 1:
            self.image = pygame.image.load('assets/meteor_brown_big_2.png').convert_alpha()
        elif randnum == 2:
            self.image = pygame.image.load('assets/meteor_brown_big_3.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/meteor_brown_big_4.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = 3

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)


class GreyAsteroid(pygame.sprite.Sprite):
    """ Large sprite that moves down the screen at med speed. """
    def __init__(self):
        super().__init__()
        randnum = random.randrange(0, 4)
        if randnum == 0:
            self.image = pygame.image.load('assets/meteor_grey_big_1.png').convert_alpha()
        elif randnum == 1:
            self.image = pygame.image.load('assets/meteor_grey_big_2.png').convert_alpha()
        elif randnum == 2:
            self.image = pygame.image.load('assets/meteor_grey_big_3.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/meteor_grey_big_4.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = 5

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)


class MedAsteroid(pygame.sprite.Sprite):
    """ Small sprite that moves down the screen quickly. """
    def __init__(self):
        super().__init__()
        randnum = random.randrange(0, 2)
        if randnum == 0:
            self.image = pygame.image.load('assets/meteor_brown_med_1.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/meteor_brown_med_2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = 8

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)


class Alien(pygame.sprite.Sprite):
    """ Sprite that zigzags down the screen, ocasionally shooting laser sprites. """
    def __init__(self):
        super().__init__()
        self.speed = 4
        rand_num = random.randrange(0, 4)
        if rand_num == 0:
            self.image = pygame.image.load('assets/alien_red.png')
        elif rand_num == 1:
            self.image = pygame.image.load('assets/alien_blue.png')
        elif rand_num == 2:
            self.image = pygame.image.load('assets/alien_yellow.png')
        else:
            self.image = pygame.image.load('assets/alien_green.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.x_speed = 4
        self.y_speed = 4

        (self.straight, self.x_min, self.x_max) = self.gen_min_max()

        self.rect.x = random.randrange(self.x_min, self.x_max)
        self.rect.y = random.randrange(-1000, -200)

        self.change_time = 0

        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('music/laser_alien.ogg')

    def update(self, timer):
        self.rect.y += self.y_speed

        if self.rect.y > 768:
            self.reset_pos()
            self.x_speed = self.speed

        if self.straight is True:
            self.x_speed = 0
        elif self.straight is False:
            if self.rect.x > self.x_max:
                self.x_speed = -self.speed
            if self.rect.x < self.x_min:
                self.x_speed = self.speed

        self.rect.x += self.x_speed

        time = random.randrange(100, 400)
        if timer % time == 0 and self.rect.y > -400:
            self.shoot()

        self.lasers.update()

    def draw_lasers(self, screen):
        self.lasers.draw(screen)

    def shoot(self):
        self.lasers.add(AlienLaser(self.rect.x + 45, self.rect.y + 45))
        self.laser_sound.play()

    def gen_min_max(self):
        num_1 = random.randrange(0, 1000)
        num_2 = random.randrange(0, 1000)

        if num_1 > num_2:
            x_max = num_1
            x_min = num_2
        elif num_2 > num_1:
            x_max = num_2
            x_min = num_1
        else:
            x_max = num_1
            x_min = num_2 - 1

        if x_max - x_min < 300:
            straight = True
        else:
            straight = False

        return straight, x_min, x_max

    def reset_pos(self):
        (self.straight, self.x_min, self.x_max) = self.gen_min_max()
        self.rect.y = random.randrange(-10000, -200)
        self.rect.x = random.randrange(self.x_min, self.x_max)


class AlienLaser(pygame.sprite.Sprite):
    """ Sprite that moves down the screen. Used by the Alien class. """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/laser_green.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = x
        self.rect.y = y

        self.speed = 8

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 768:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """ An explosion animation. """
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.index = 0

    def update(self):
        pass
        self.index += 1
        if self.index < len(self.images):
            self.image = self.images[self.index]
        else:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """Sprites that move down the screen, and reset position when they reach the bottom.
    Different images depending on what is passed to the constructor.
    Has a timer that can be used to time effets. """
    def __init__(self, powerup_type):
        super().__init__()
        self.y_min = -10000
        self.speed = 4
        self.timer = 0
        if powerup_type == "speed":
            self.type = "speed"
            self.image = pygame.image.load('assets/green_square_bolt.png').convert_alpha()
        elif powerup_type == "laser":
            self.type = "laser"
            self.image = pygame.image.load('assets/red_square_star.png').convert_alpha()
        elif powerup_type == "health":
            self.type = "health"
            self.image = pygame.image.load('assets/yellow_square_pill.png').convert_alpha()
        elif powerup_type == "shield":
            self.type = "shield"
            self.image = pygame.image.load('assets/blue_square_shield.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(self.y_min, -200)
        self.rect.x = random.randrange(0, 1024)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(self.y_min, -200)
            self.rect.x = random.randrange(0, 1024)

    def reset_pos(self):
        self.rect.y = random.randrange(self.y_min, -200)
        self.rect.x = random.randrange(0, 1024)


    def powerup_over(self):
        self.timer += 1
        if self.timer > 300:
            return True


class CollectStar(pygame.sprite.Sprite):
    """Sprites that move down the screen and reset position when they reach the bottom.
    Different images depending on what is passed to the constructor. """
    def __init__(self, star_type):
        super().__init__()
        self.star_type = star_type
        if star_type == "bronze":
            self.image = pygame.image.load('assets/star_bronze.png').convert_alpha()
            self.speed = 3
            self.y_min = -5000
            self.y_max = -100
        elif star_type == "silver":
            self.image = pygame.image.load('assets/star_silver.png').convert_alpha()
            self.speed = 4
            self.y_min = -5000
            self.y_max = -100
        elif star_type == "gold":
            self.image = pygame.image.load('assets/star_gold.png').convert_alpha()
            self.speed = 5
            self.y_min = -5000
            self.y_max = -100
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = random.randrange(self.y_min, self.y_max)
        self.rect.x = random.randrange(0, 1024)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(self.y_min, -200)
            self.rect.x = random.randrange(0, 1024)

    def reset_pos(self):
        self.rect.y = random.randrange(self.y_min, -200)
        self.rect.x = random.randrange(self.y_min, self.y_max)


# Scenery
class Star:
    """"Small dots that move down the screen."""
    def __init__(self, min_r=230, max_r=255, min_g=230, max_g=255, min_b=230, max_b=255, min_size=1, max_size=3,
                 min_speed=1, max_speed=4):
        self.x = random.randrange(0, 1024)
        self.y = random.randrange(0, 768)
        self.color = (random.randrange(min_r, max_r), random.randrange(min_g, max_g), random.randrange(min_b, max_b))
        self.speed = random.randrange(min_speed, max_speed)
        self.size = random.randrange(min_size, max_size)

    def update_pos(self):
        self.y += self.speed
        if self.y > 768:
            self.y = random.randrange(-100, 0)
            self.x = random.randrange(0, 1024)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


