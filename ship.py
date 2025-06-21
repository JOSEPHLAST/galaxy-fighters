import pygame

class Ship:
    """Creates a ship instance."""
    def __init__(self, gf_game):
        self.screen = gf_game.screen
        self.screen_rect = gf_game.screen.get_rect()
        self.settings = gf_game.settings
        self.screen_width, self.screen_height = gf_game.screen_width, gf_game.screen_height
        self.ship_width, self.ship_height = gf_game.ship_width, gf_game.ship_height
        self.yellow_ship_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/spaceship_yellow.png"), (self.ship_width, self.ship_height)), 270)
        self.red_ship_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/spaceship_red.png"), (self.ship_width, self.ship_height)), 90)
        self.rect_yellow, self.rect_red = self.yellow_ship_image.get_rect(), self.red_ship_image.get_rect()
        self.border = gf_game.border
        self.border_width, self.border_height = gf_game.border_width, gf_game.border_height
        self.border_color = gf_game.border_color
        self.rect_yellow.x, self.rect_yellow.y = (self.screen_width//2 - self.ship_width)//2, (self.screen_height - self.ship_height)//2
        self.rect_red.x, self.rect_red.y = 3*(self.screen_width)//4 - self.ship_width//2, (self.screen_height - self.ship_height)//2
        self.yellow_moving_left, self.yellow_moving_right, self.yellow_moving_up, self.yellow_moving_down = False, False, False, False
        self.red_moving_left, self.red_moving_right, self.red_moving_up, self.red_moving_down = False, False, False, False

    def update_ship_position(self):
        """Update the ships' position to the display."""
        # Yellowship movement
        if self.yellow_moving_left and self.rect_yellow.left > self.screen_rect.left:
            self.rect_yellow.x -= self.settings.ship_speed
        if self.yellow_moving_right and self.rect_yellow.right < (self.screen_rect.right - self.border_width)//2:
            self.rect_yellow.x += self.settings.ship_speed
        if self.yellow_moving_up and self.rect_yellow.top > self.screen_rect.top:
            self.rect_yellow.y -= self.settings.ship_speed
        if self.yellow_moving_down and self.rect_yellow.bottom < self.screen_rect.bottom:
            self.rect_yellow.y += self.settings.ship_speed

        # Redship movement
        if self.red_moving_left and self.rect_red.left > (self.screen_rect.right + self.border_width)//2:
            self.rect_red.x -= self.settings.ship_speed
        if self.red_moving_right and self.rect_red.right < self.screen_rect.right:
            self.rect_red.x += self.settings.ship_speed
        if self.red_moving_up and self.rect_red.top > self.screen_rect.top:
            self.rect_red.y -= self.settings.ship_speed
        if self.red_moving_down and self.rect_red.bottom < self.screen_rect.bottom:
            self.rect_red.y += self.settings.ship_speed

    def blit_ships(self):
        """Blit the ships to the screen."""
        self.screen.blit(self.yellow_ship_image, (self.rect_yellow))
        self.screen.blit(self.red_ship_image, (self.rect_red))

    def blit_border(self):
        """Blit the border/demarcation to the screen."""
        pygame.draw.rect(self.screen, self.border_color, self.border)
