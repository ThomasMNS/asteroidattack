""" A baseplate game scene, which game levels inherit from. """

# Standard library
import os
# Pygame
import pygame
# Game modules
import generic_scene
import gameplay_items
import constants
import scene_tools
import ui_scenes


class GameScene(generic_scene.GenericScene):
    """ A starter class for a game level. Includes a scrolling background image, upper and lower
    scrolling stars, a player ship, powerups, scores etc. """
    def __init__(self, background_image):
        super().__init__()

        pygame.mouse.set_visible(False)

        # Setting up the game stats
        self.score = 0
        self.lives = 3
        self.health = 100
        # Text and scores
        self.score_font = pygame.font.Font(None, 25)
        self.timer = 0

        # Preloading explosion GFX
        self.images = []
        mypath = os.path.join(os.path.dirname(__file__), 'assets', 'explosion')
        for file in os.listdir(mypath):
            myfile = "assets/explosion/{0}".format(file)
            self.images.append(pygame.image.load(myfile).convert_alpha())

        # Endlessly scrolling stars background
        self.background = background_image
        self.background_y = -768
        self.background_2 = background_image
        self.background_2_y = -2304

        # Create two lists of star objects. One will be drawn before the ship and the other after
        # to give an illusion of depth
        self.bottom_stars = []
        for i in range(30):
            star = gameplay_items.Star()
            self.bottom_stars.append(star)

        self.top_stars = []
        for i in range(20):
            star = gameplay_items.Star()
            self.top_stars.append(star)

        # Create a container to hold all *sprites*. Images, drawings etc will not be in here
        self.all_sprites = pygame.sprite.Group()
        # Other containers for more granular control
        self.asteroids = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create a player ship object, and place near the bottom of the screen
        self.player.update_pos(50, 600)
        self.all_sprites.add(self.player)
        # Creating a container for lasers
        self.lasers = pygame.sprite.Group()

        # Spawn powerups
        self.pups = pygame.sprite.Group()
        # Create a speed powerup
        self.powerup = gameplay_items.PowerUp("speed")
        self.all_sprites.add(self.powerup)
        self.pups.add(self.powerup)
        # Create a laser ammo powerup
        self.powerup = gameplay_items.PowerUp("laser")
        self.all_sprites.add(self.powerup)
        self.pups.add(self.powerup)
        # Create a health powerup
        self.powerup = gameplay_items.PowerUp("health")
        self.all_sprites.add(self.powerup)
        self.pups.add(self.powerup)
        # Create a shield powerup
        self.powerup = gameplay_items.PowerUp("shield")
        self.all_sprites.add(self.powerup)
        self.pups.add(self.powerup)

        # Spawn stars. These are not added to all_sprites so they can be rendered on top.
        self.collectible_stars = pygame.sprite.Group()
        for i in range(2):
            star = gameplay_items.CollectStar("gold")
            self.collectible_stars.add(star)
        for i in range(5):
            star = gameplay_items.CollectStar("silver")
            self.collectible_stars.add(star)
        for i in range(11):
            star = gameplay_items.CollectStar("bronze")
            self.collectible_stars.add(star)

        # Level ending beep
        self.ending_beep = pygame.mixer.Sound('music/zap.ogg')

    def handle_events(self, events):
        for event in events:
            # Ship keyboard controls
            # Checking for key press
            if event.type == pygame.KEYDOWN:
                # Movement
                if event.key == pygame.K_w:
                    self.player.y_speed = -self.player.speed
                elif event.key == pygame.K_s:
                    self.player.y_speed = self.player.speed
                elif event.key == pygame.K_d:
                    self.player.x_speed = self.player.speed
                elif event.key == pygame.K_a:
                    self.player.x_speed = -self.player.speed
                # Fire laser
                elif event.key == pygame.K_SPACE:
                    if self.player.lasers > 0:
                        self.lasers.add(gameplay_items.Laser(self, self.player.rect.x + 53, self.player.rect.y + 10))
                        self.player.lasers -= 1
            # Checking for key release
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.player.y_speed = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.x_speed = 0

    def update(self):
        self.timer += 1
        if self.timer % 300 == 0:
            self.score += 1

        # Background scrolling
        self.background_y += 1
        self.background_2_y += 1
        if self.background_y >= 768:
            self.background_y = self.background_2_y - 1536
        if self.background_2_y >= 768:
            self.background_2_y = self.background_y - 1536

        for star in self.bottom_stars:
            star.update_pos()

        for star in self.top_stars:
            star.update_pos()

        # Death
        if self.health <= 0:
            self.lives -= 1
            self.all_sprites.add(gameplay_items.Explosion(self.player.rect.x, self.player.rect.y, self.images))
            scene_tools.death_scene_reset([self.asteroids, self.pups, self.collectible_stars], self.player)
            self.health = 100
            self.player.alert_played = False

        # Level ending beeps
        if self.timer == 4700 or self.timer == 4760 or self.timer == 4820 or self.timer == 4880 or self.timer == 4940:
            self.ending_beep.play()

        self.all_sprites.update()
        self.lasers.update()
        self.collectible_stars.update()
        self.aliens.update(self.timer)

    def draw(self, screen):
        # Background
        screen.fill(constants.BLACK)
        screen.blit(self.background, (0, self.background_y))
        screen.blit(self.background_2, (0, self.background_2_y))
        for star in self.bottom_stars:
            star.draw(screen)

        self.aliens.draw(screen)
        for alien in self.aliens:
            alien.draw_lasers(screen)
        self.lasers.draw(screen)
        self.all_sprites.draw(screen)

        for star in self.top_stars:
            star.draw(screen)

    def draw_text(self, screen):
        # Top left
        progress_text = "Progress through asteroid field: {0!s}%".format(int((self.timer / 100) * 2))
        progress_render = self.score_font.render(progress_text, True, constants.WHITE)
        screen.blit(progress_render, (10, 10))
        score_text = "Score: {0!s}".format(self.score)
        score_render = self.score_font.render(score_text, True, constants.WHITE)
        screen.blit(score_render, (10, 40))
        health_text = "Health: {0!s}".format(self.health)
        health_render = self.score_font.render(health_text, True, constants.WHITE)
        screen.blit(health_render, (10, 70))
        lives_text = "Lives: {0!s}".format(self.lives)
        lives_render = self.score_font.render(lives_text, True, constants.WHITE)
        screen.blit(lives_render, (10, 100))
        # Bottom left
        if self.player.speed_boosted is True:
            speed_boost_render = self.score_font.render("Speed boosted!", True, constants.WHITE)
            screen.blit(speed_boost_render, (10, 680))
        x_speed = self.player.x_speed
        y_speed = self.player.y_speed
        if y_speed < 0:
            y_speed = abs(y_speed)
        elif y_speed > 0:
            y_speed = - y_speed
        speed_text = "Ship speed: {0!s} / {1!s}".format(int(y_speed), int(x_speed))
        speed_render = self.score_font.render(speed_text, True, constants.WHITE)
        screen.blit(speed_render, (10, 710))
        lasers_text = "Laser charges remaining: {0!s}".format(self.player.lasers)
        lasers_render = self.score_font.render(lasers_text, True, constants.WHITE)
        screen.blit(lasers_render, (10, 740))


