import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Creates a bullet instance."""
    def __init__(self, gf_game):
        super().__init__()
        self.screen = gf_game.screen
        self.settings = gf_game.settings
        self.bullet_width, self.bullet_height = gf_game.bullet_width, gf_game.bullet_height
        self.bullet_rect = pygame.Rect(0, 0 , self.bullet_width, self.bullet_height) 

class YellowBullet(Bullet):
    def __init__(self, gf_game):
        super().__init__(gf_game)
        self.yellow_color = gf_game.yellow_color
        self.yellow_bullet_rect = self.bullet_rect
        self.yellow_bullet_rect.midright = gf_game.ship.rect_yellow.midright

    def update(self):
        """Movement of the yellow bullets."""
        self.yellow_bullet_rect.x += self.settings.bullet_speed

    def draw_yellow_bullets(self):
        """Draw the yellow bullets to the screen."""
        pygame.draw.rect(self.screen, self.yellow_color, self.yellow_bullet_rect)

class RedBullet(Bullet):
    def __init__(self, gf_game):
        super().__init__(gf_game)
        self.red_color = gf_game.red_color
        self.red_bullet_rect = self.bullet_rect
        self.red_bullet_rect.midleft = gf_game.ship.rect_red.midleft

    def update(self):
        """Movement of the red bullets."""
        self.red_bullet_rect.x -= self.settings.bullet_speed

    def draw_red_bullets(self):
        """Draw the red bullets to the screen."""
        pygame.draw.rect(self.screen, self.red_color, self.red_bullet_rect)