""" Classes used to create objects to populate gameplay levels. This includes the player (ship),
obstacles (E.g. asteroids), powerups (E.g. speed boost) and scenery (E.g. stars). """

# Pygame
import pygame
# Standard library
import random
import math
import inspect
# Game modules
import scene_tools


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
        self.lasers_group = pygame.sprite.Group()

        # Shield
        self.shield = None

        self.game_scene = None

        self.alert_played = False
        self.alarm = pygame.mixer.Sound('music/alarm.wav')
        self.alarm.set_volume(0.5)

        # Powerup sound
        self.powerup_sound = pygame.mixer.Sound('music/powerup.wav')
        self.powerup_sound.set_volume(0.5)

        # Star sound
        self.star_sound = pygame.mixer.Sound('music/coin.wav')
        self.star_sound.set_volume(0.2)

        self.health = 100

    def update_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.shield is not None:
            self.shield.update_pos(self)

        if self.game_scene is not None:
            self.collision_detection(self.game_scene.asteroids)
            self.collision_detection(self.game_scene.aliens)
            for alien in self.game_scene.aliens:
                self.collision_detection(alien.lasers)

            # Check if this is player one
            if self.game_scene.player is self:
                # Check if there is a player 2
                if self.game_scene.player_2 is not None:
                    self.collision_detection(self.game_scene.player_2.lasers_group)
            # Check if this is player two
            if self.game_scene.player_2 is self:
                self.collision_detection(self.game_scene.player.lasers_group)

            # Powerup collision detection
            for pup in self.game_scene.pups:
                if pygame.sprite.collide_mask(self, pup):
                    self.game_scene.score += 10
                    if pup.type == "speed":
                        self.speed_boosted = True
                    elif pup.type == "laser":
                        laser_count = self.lasers
                        laser_count += 3
                        if laser_count > 5:
                            laser_count = 5
                        self.lasers = laser_count
                    elif pup.type == "health":
                        self.health += 50
                        if self.health > 100:
                            self.health = 100
                    elif pup.type == "shield":
                        if self.shield is None:
                            self.create_shield(self.game_scene.all_sprites)

                    pup.reset_pos()
                    self.powerup_sound.play()

            # Powerup effects
            if self.speed_boosted is True:
                self.speed = 8
                self.speed_boost_timer += 1
                if self.speed_boost_timer == 600:
                    self.speed_boosted = False
                    self.speed = 4
                    self.speed_boost_timer = 0

            # Collectible star collision detection
            for star in self.game_scene.collectible_stars:
                if pygame.sprite.collide_mask(self, star):
                    if star.star_type == "bronze":
                        self.game_scene.score += 2
                    elif star.star_type == "silver":
                        self.game_scene.score += 4
                    elif star.star_type == "gold":
                        self.game_scene.score += 10
                    star.reset_pos()
                    self.star_sound.play()

        # Don't let the ship move outside the screen
        if self.rect[0] <= 0:
            self.update_pos(0, self.rect.y)
        elif self.rect[0] >= (1024 - self.rect.width):
            self.update_pos(1024 - self.rect.width, self.rect.y)
        if self.rect[1] <= 0:
            self.update_pos(self.rect.x, 0)
        elif self.rect[1] >= (768 - self.rect.height):
            self.update_pos(self.rect.x, 768 - self.rect.height)


        # Death
        if self.health <= 0:
            self.game_scene.lives -= 1
            self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
            scene_tools.death_scene_reset([self.game_scene.asteroids, self.game_scene.pups,
                                           self.game_scene.collectible_stars], self, self.game_scene.player_2)
            self.health = 100
            self.alert_played = False

        self.lasers_group.update()

    def create_shield(self, sprite_group):
        self.shield = Shield(self)
        self.shield.update_pos(self)
        sprite_group.add(self.shield)

    def update_appearance(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def collision_detection(self, enemies):
        for enemy in enemies:
            if self.shield is None:
                if pygame.sprite.collide_mask(enemy, self):
                    enemy.collision()
                    if self.health - enemy.health_decrease < 25 and self.alert_played is False:
                        self.alarm.play()
                        self.alert_played = True
                    self.health -= enemy.health_decrease
            elif self.shield is not None:
                if pygame.sprite.collide_mask(enemy, self.shield):
                    enemy.collision()
                    self.shield.kill()
                    self.shield = None

    def fire_laser(self):
        if self.lasers > 0:
            self.lasers_group.add(Laser(self.game_scene, self.rect.x + 53, self.rect.y + 10))
            self.lasers -= 1


class Shield(pygame.sprite.Sprite):
    """ Appears around a PlayerShip() instance. """
    def __init__(self, ship):
        super().__init__()
        self.image = pygame.image.load('assets/shield.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 10)

    def update_pos(self, ship):
        self.rect.x = ship.rect.x - 17
        self.rect.y = ship.rect.y - 32


class Laser(pygame.sprite.Sprite):
    """ Moves upwards. Instantiated at player ship location. """
    def __init__(self, game_scene, x, y):
        super().__init__()
        self.game_scene = game_scene
        self.image = pygame.image.load('assets/laser_red.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = -7
        self.rect.x = x
        self.rect.y = y
        self.sound = pygame.mixer.Sound('music/laser.ogg')
        self.sound.play()

        self.health_decrease = 20

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -100:
            self.kill()

        self.collision_detection(self.game_scene.asteroids)
        self.collision_detection(self.game_scene.aliens)

    def collision_detection(self, enemies):
        for enemy in enemies:
            if pygame.sprite.collide_mask(enemy, self):
                self.kill()
                enemy.collision()
                self.game_scene.score += enemy.score_increase

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class BrownAsteroid(pygame.sprite.Sprite):
    """ Large sprite that moves slowly down the screen. """
    def __init__(self, game_scene):
        super().__init__()
        self.game_scene = game_scene
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

        self.score_increase = 30
        self.health_decrease = 30

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class GreyAsteroid(pygame.sprite.Sprite):
    """ Large sprite that moves down the screen at med speed. """
    def __init__(self, game_scene):
        super().__init__()
        self.game_scene = game_scene
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

        self.score_increase = 30
        self.health_decrease = 30

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class MedAsteroid(pygame.sprite.Sprite):
    """ Small sprite that moves down the screen quickly. """
    def __init__(self, game_scene):
        super().__init__()
        self.game_scene = game_scene
        randnum = random.randrange(0, 2)
        if randnum == 0:
            self.image = pygame.image.load('assets/meteor_brown_med_1.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/meteor_brown_med_2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = 8

        self.score_increase = 30
        self.health_decrease = 30

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class FragmentingAsteroid(pygame.sprite.Sprite):
    """ A large asteroid. When hit, it breaks into multiple smaller asteroids. """
    def __init__(self, game_scene):
        super().__init__()
        randnum = random.randrange(1, 5)
        self.image = pygame.image.load('assets/meteor_dark_brown_big_{0!s}.png'.format(randnum)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = random.randrange(-2000, -200)
        self.rect.x = random.randrange(0, 1024)

        self.y_speed = 4

        self.game_scene = game_scene

        self.score_increase = 30
        self.health_decrease = 30

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()
        ast1 = FragmentedAsteroid(self.game_scene)
        ast1.rect.x = self.rect.x + (self.rect.width / 2 - ast1.rect.width / 2) + 40
        ast1.rect.y = self.rect.y
        self.game_scene.all_sprites.add(ast1)
        self.game_scene.asteroids.add(ast1)
        ast2 = FragmentedAsteroid(self.game_scene)
        ast2.rect.x = self.rect.x + (self.rect.width / 2 - ast1.rect.width / 2) - 40
        ast2.rect.y = self.rect.y + 30
        self.game_scene.all_sprites.add(ast2)
        self.game_scene.asteroids.add(ast2)


class FragmentedAsteroid(pygame.sprite.Sprite):
    """ A smaller asteroid spawned when a fragmenting asteroid is destroyed. """
    def __init__(self, game_scene):
        super().__init__()
        self.image = pygame.image.load('assets/meteor_brown_med_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.y_speed = 7

        self.rect.y = random.randrange(-2000, -200)
        self.rect.x = random.randrange(0, 1024)

        self.game_scene = game_scene

        self.score_increase = 30
        self.health_decrease = 30

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class StrongAsteroid(pygame.sprite.Sprite):
    """ An asteroid that takes several hits to destroy. """
    def __init__(self, game_scene):
        super().__init__()
        self.randnum = random.randrange(1, 5)
        self.image = pygame.image.load('assets/meteor_purple_big_{0!s}.png'.format(self.randnum)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.game_scene = game_scene
        self.y_speed = 2
        self.score_increase = 30
        self.health_decrease = 30

        self.health = 3

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y > 768:
            self.rect.y = random.randrange(-2000, -200)
            self.rect.x = random.randrange(0, 1024)

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.health -= 1
        if self.health == 2:
            y = self.rect.y
            x = self.rect.x
            self.image = pygame.image.load('assets/meteor_purple_big_{0!s}_damaged_1.png'.format(self.randnum)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
            self.mask = pygame.mask.from_surface(self.image)
        elif self.health == 1:
            y = self.rect.y
            x = self.rect.x
            self.image = pygame.image.load('assets/meteor_purple_big_{0!s}_damaged_2.png'.format(self.randnum)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
            self.mask = pygame.mask.from_surface(self.image)
        elif self.health == 0:
            self.kill()


class Alien(pygame.sprite.Sprite):
    """ Sprite that zigzags down the screen, ocasionally shooting laser sprites. """
    def __init__(self, game_scene):
        super().__init__()
        self.game_scene = game_scene
        self.speed = 4
        rand_num = random.randrange(0, 4)
        if rand_num == 0:
            self.image = pygame.image.load('assets/alien_red.png').convert_alpha()
        elif rand_num == 1:
            self.image = pygame.image.load('assets/alien_blue.png').convert_alpha()
        elif rand_num == 2:
            self.image = pygame.image.load('assets/alien_yellow.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/alien_green.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.x_speed = 4
        self.y_speed = 4

        (self.straight, self.x_min, self.x_max) = self.gen_min_max()

        self.rect.x = random.randrange(self.x_min, self.x_max)
        self.rect.y = random.randrange(-1000, -200)

        self.change_time = 0

        self.lasers = pygame.sprite.Group()

        self.score_increase = 40
        self.health_decrease = 30

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
        self.lasers.add(AlienLaser(self.rect.x + 45, self.rect.y + 45, self.game_scene))

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

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class AlienLaser(pygame.sprite.Sprite):
    """ Sprite that moves down the screen. Used by the Alien class. """
    def __init__(self, x, y, game_scene, angle=0):
        super().__init__()
        self.game_scene = game_scene
        self.image = pygame.image.load('assets/laser_green.png').convert_alpha()

        self.speed = 8
        self.health_decrease = 30

        self.laser_sound = pygame.mixer.Sound('music/laser_alien.ogg')
        self.laser_sound.play()

        # Angle and rotation
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.x_speed = self.speed * math.sin(math.radians(self.angle))
        self.y_speed = self.speed * math.cos(math.radians(self.angle))
        self.real_x = x
        self.real_y = y

    def update(self):
        self.real_x += self.x_speed
        self.real_y += self.y_speed

        self.rect.x = round(self.real_x)
        self.rect.y = round(self.real_y)

        if (0 > self.rect.y > 768) or (0 > self.rect.x > 1024):
            self.kill()

    def collision(self):
        self.game_scene.all_sprites.add(Explosion(self.rect.x, self.rect.y, self.game_scene.images))
        self.kill()


class Boss(pygame.sprite.Sprite):
    """ A large red flying saucer. """
    def __init__(self, game_scene, boss_type=1):
        super().__init__()
        # So we can access other stuff in the level
        self.game_scene = game_scene

        # Different bosses have different phases
        self.boss_type = boss_type

        # Req for all sprites
        if self.boss_type == 1:
            self.image = pygame.image.load("assets/big_red_saucer.png").convert_alpha()
        elif self.boss_type == 2:
            self.image = pygame.image.load("assets/big_green_saucer.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Set location and speed
        self.rect.x = 200
        self.rect.y = 60
        self.speed = 5
        self.vertical_speed = 4

        self.health = 100

        # This will hold the lasers the boss has fired
        self.lasers = pygame.sprite.Group()

        # How much to increase player score by if hit by laser
        self.score_increase = 7

        # Destroy the player if they hit boss
        self.health_decrease = 1000

        # Phase specific variables
        # Rapid Fire
        self.rapid_firing = False
        # Wall fire
        # Should the saucer be firing constantly
        self.wall_firing = False
        # Has it gone from right to left, and is now returning right
        self.run_finished = False
        # Has a random gap location been calculated for the run
        self.gap_needed = True
        # Has the phase just started (needed to prevent a bit of firing from left to right)
        self.just_started = True
        # Ramming Speed
        # Is the ship travelling down the screen
        self.ramming = False
        # Or up the screen
        self.returning_from_ram = False
        # Radial Fire
        self.radial_firing = False
        self.radial_position_needed = True
        self.old_speed_needed = True
        self.radial_position = 0
        self.radial_angle = 180
        self.radial_retreating = False

        self.laser_fire_checked = False
        self.rapid_fire_checked = False
        self.dive_bomb_checked = False
        self.fire_wheel_checked = False

        self.laser_wall_checked = False
        self.ramming_speed_checked = False
        self.spread_fire_checked = False
        self.radial_fire_checked = False

    def update(self, timer):
        # Move from side to side within the screen
        if self.rect.x + self.rect.width >= 1098:
            self.speed *= -1
        elif self.rect.x < -74:
            self.speed *= -1

        # Move
        self.rect.x += self.speed

        if self.boss_type == 1:
            if 75 <= self.health <= 100:
                self.phase = "laserfire"
            elif 50 <= self.health <= 74:
                self.phase = "rapidfire"
            elif 25 <= self.health <= 49:
                self.phase = "divebomb"
            else:
                self.phase = "firewheel"
        elif self.boss_type == 2:
            if 75 <= self.health <= 100:
                self.phase = "laserwall"
            elif 50 <= self.health <= 74:
                self.phase = "rammingspeed"
            elif 25 <= self.health <= 49:
                self.phase = "spreadfire"
            else:
                self.phase = "radialfire"

        if self.phase == "laserfire":
            self.display_phase = "Laser Fire"
            if self.laser_fire_checked is False:
                self.reset()
                if self.reset() is True:
                    self.laser_fire_checked = True
            if self.laser_fire_checked is True:
                if timer % 120 == 0:
                    self.shoot()
        elif self.phase == "rapidfire":
            self.display_phase = "Rapid Fire"
            if self.rapid_fire_checked is False:
                self.reset()
                if self.reset() is True:
                    self.laser_fire_checked = True
            if self.laser_fire_checked is True:
                # Every 4 seconds, set firing to True
                if timer % 180 == 0:
                    self.rapid_firing = True
                    self.rapid_count = 0

                if self.rapid_firing == True:
                    if timer % 10 == 0:
                        if self.rapid_count < 3:
                            self.shoot()
                        self.rapid_count += 1
        elif self.phase == "divebomb":
            self.display_phase = "Dive Bomb"
            if self.dive_bomb_checked is False:
                self.reset()
                if self.reset() is True:
                    self.dive_bomb_checked = True
            if self.dive_bomb_checked is True:
                self.rect.y += self.vertical_speed
                if self.rect.y + self.rect.width > 768:
                    self.vertical_speed *= -1
                elif self.rect.y < 60:
                    self.vertical_speed *= -1
                if timer % 60 == 0:
                    self.shoot()
        elif self.phase == "firewheel":
            self.display_phase = "Fire Wheel"
            if self.fire_wheel_checked is False:
                self.reset()
                if self.reset() is True:
                    self.fire_wheel_checked = True
            if self.fire_wheel_checked is True:
                if timer % 120 == 0:
                    x = 0
                    while x <= 360:
                        self.shoot(x)
                        x += 20
        elif self.phase == "laserwall":
            self.display_phase = "Laser Wall"
            if self.laser_wall_checked is False:
                self.reset()
                if self.reset() is True:
                    self.laser_fire_checked = True
            if self.laser_fire_checked is True:
                # Ship has reached top right corner, start firing
                if self.rect.x + self.rect.width >= 1097:
                    self.wall_firing = True
                    self.run_finished = False
                    self.just_started = False
                # Fire every 1/6 second
                if self.wall_firing is True and self.run_finished is not True and self.just_started is False:
                    if timer % 10 == 0:
                        self.shoot()
                # Random gap location for the run, if needed
                if self.gap_needed is True:
                    self.gap_start = random.randrange(200, 800)
                    self.gap_needed = False
                # If inside the gap, don't fire
                if self.rect.x <= self.gap_start + 100:
                    self.wall_firing = False
                if self.rect.x <= self.gap_start:
                    self.wall_firing = True
                # Ship has reched top left corner, stop firing
                if self.rect.x <= -73:
                    self.wall_firing = False
                    self.run_finished = True
                    self.gap_needed = True
        elif self.phase == "rammingspeed":
            self.display_phase = "Ramming Speed"
            if self.ramming_speed_checked is False:
                self.reset()
                if self.reset() is True:
                    self.ramming_speed_checked = True
            if self.ramming_speed_checked is True:
                # Every 4 seconds
                if timer % 240 == 0 and self.returning_from_ram is False:
                    self.ramming = True
                # If ship reaches bottom of screen, go up and returning_from_ram is True (so can't go down again)
                if self.rect.y + self.rect.height > 767:
                    self.ramming = False
                    self.returning_from_ram = True
                # If ramming, go down screen and shoot
                if self.ramming is True:
                    self.rect.y += self.vertical_speed
                    if timer % 40 == 0:
                        self.shoot()
                # Go up screen in straight line
                if self.ramming is False and self.returning_from_ram is True:
                    self.rect.y -= self.vertical_speed
                    self.speed = 0
                # Once at top of screen, return to side to side movement
                if self.returning_from_ram is True and self.rect.y < 60:
                    self.returning_from_ram = False
                    self.speed = 5
        elif self.phase == "spreadfire":
            self.display_phase = "Spread Fire"
            if self.spread_fire_checked is False:
                self.reset()
                if self.reset() is True:
                    self.spread_fire_checked = True
            if self.spread_fire_checked is True:
                # Every second
                if timer % 60 == 0:
                    for number in (0, 45, 315):
                        self.shoot(number)
        elif self.phase == "radialfire":
            self.display_phase = "Radial Fire"
            if self.radial_fire_checked is False:
                self.reset()
                if self.reset() is True:
                    self.radial_fire_checked = True
            if self.radial_fire_checked is True:
                if self.radial_retreating is False:
                    if self.radial_position_needed is True:
                        self.radial_position = random.randrange(200, 800)
                        self.radial_position_needed = False
                    if (self.radial_position - 10) < self.rect.x < (self.radial_position + 10):
                        if self.old_speed_needed is True:
                            self.old_speed = self.speed
                            self.old_speed_needed = False
                        self.speed = 0
                        if self.rect.y < 350:
                            self.rect.y += self.vertical_speed
                        if 345 < self.rect.y < 355:
                            self.radial_firing = True
                        if self.radial_firing is True:
                            if timer % 10 == 0:
                                self.shoot(self.radial_angle)
                                self.radial_angle -= 15
                            if self.radial_angle == -180:
                                self.radial_angle = 180
                                self.radial_retreating = True
                                self.radial_firing = False
                if self.radial_retreating is True:
                    self.rect.y -= self.vertical_speed
                    if self.rect.y <= 60:
                        self.radial_retreating = False
                        self.speed = self.old_speed
                        self.radial_position_needed = True






        self.lasers.update()

        # Update the health bar
        self.game_scene.boss_health_bar.current_health = self.health

        if self.health <= 0:
            self.kill()
            self.game_scene.all_sprites.add(Explosion(self.rect.center[0], self.rect.center[1], self.game_scene.images))
            for laser in self.lasers:
                laser.kill()

    def shoot(self, angle=0):
        self.lasers.add(AlienLaser(self.rect.center[0], self.rect.center[1], self.game_scene, angle))

    def draw_lasers(self, screen):
        self.lasers.draw(screen)

    def collision(self):
        """ Called if there is a collision with a player laser. """
        self.game_scene.all_sprites.add(Explosion(self.rect.center[0], self.rect.center[1], self.game_scene.images))
        self.health -= 10

    def reset(self):
        """ Phases assume that the saucer is at the top of the screen moving from side to side.
        This makes sure that is the case. """
        if self.rect.y > 60:
            self.rect.y -= abs(self.vertical_speed)
        # Return True if ship is at the top of the screen
        if self.rect.y <= 60:
            return True
        else:
            return False


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

        explosion = pygame.mixer.Sound('music/explosion.wav')
        explosion.set_volume(0.2)
        explosion.play()

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


