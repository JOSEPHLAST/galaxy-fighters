import pygame
from settings import Settings
from ship import Ship
from bullet import YellowBullet, RedBullet
pygame.font.init()
pygame.mixer.init()
from random import randint

class GalaxyFighters:
    """Handles the overall game."""
    yellow_score, red_score = Settings().players_scores

    def __init__(self):
        self.settings = Settings()
        self.screen_width, self.screen_height = self.settings.screen_dimensions
        self.ship_width, self.ship_height = self.settings.ship_dimensions
        self.ship_speed = self.settings.ship_speed
        self.border_width, self.border_height = self.settings.border_dimensions
        self.border_color = self.settings.border_color
        self.score_font = pygame.font.SysFont("comicsans", 50, "bold")
        self.health_font = pygame.font.SysFont("comicsans", 20)
        self.gameover_font = pygame.font.SysFont("comicsans", 35, "bold")
        self.bg_image = pygame.transform.scale(pygame.image.load("assets/space.png"), (self.screen_width, self.screen_height))
        self.fire_sound = pygame.mixer.Sound("assets/red.mp3")
        self.hit_sound = pygame.mixer.Sound("assets/yellow.mp3")
        self.gameover_sound = pygame.mixer.Sound("assets/wrong.mp3")
        self.gameover_text = self.gameover_font.render(f"", 1, "white")
        self.screen = pygame.display.set_mode((self.settings.screen_dimensions))
        pygame.display.set_caption("Galaxy Fighters")
        self.border = pygame.Rect((self.screen_width - self.border_width)//2, 0, self.border_width, self.border_height)
        self.ship = Ship(self)
        self.rect_yellow, self.rect_red = self.ship.rect_yellow, self.ship.rect_red
        self.yellow_color, self.red_color = self.settings.bullet_colors
        self.bullet_width, self.bullet_height = self.settings.bullet_dimensions
        self.yellow_bullets, self.red_bullets = pygame.sprite.Group(), pygame.sprite.Group()
        self.yellow_lives, self.red_lives = self.settings.lives
        self.busted = False
        self.restart_text = self.gameover_font.render(f"", 1, "white")
        self.yellow_score_text = self.score_font.render(f"{self.yellow_score}", 1, "white")
        self.red_score_text = self.score_font.render(f"{self.red_score}", 1, "white")

    def run_game(self):
        """Runs the main game."""
        
        while self.busted == False:
            self._check_events()
            self.ship.update_ship_position()
            self._update_yellow_bullets()
            self._update_red_bullets()
            self._handle_gameover_events()
            self._update_screen()
            if self.busted:
                pygame.time.delay(3000)
                self.__init__()
                self.run_game()

    def _check_events(self):
        """Checks for keypresses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Checks for keydowns."""
        # Yellowship controls
        if event.key == pygame.K_a:
            self.ship.yellow_moving_left = True
        if event.key == pygame.K_d:
            self.ship.yellow_moving_right = True
        if event.key == pygame.K_w:
            self.ship.yellow_moving_up = True
        if event.key == pygame.K_s:
            self.ship.yellow_moving_down = True
        if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < self.settings.max_bullets:
            self._yellow_fire_bullet()

        # Redship controls
        if event.key == pygame.K_LEFT:
            self.ship.red_moving_left = True
        if event.key == pygame.K_RIGHT:
            self.ship.red_moving_right = True
        if event.key == pygame.K_UP:
            self.ship.red_moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.red_moving_down = True
        if event.key == pygame.K_RCTRL and len(self.red_bullets) < self.settings.max_bullets:
            self._red_fire_bullet()

        if event.key == pygame.K_q:
            pygame.quit()

    def _check_keyup_events(self, event):
        """Checks for keyups."""
        # Yellowship controls
        if event.key == pygame.K_a:
            self.ship.yellow_moving_left = False
        if event.key == pygame.K_d:
            self.ship.yellow_moving_right = False
        if event.key == pygame.K_w:
            self.ship.yellow_moving_up = False
        if event.key == pygame.K_s:
            self.ship.yellow_moving_down = False

        # Redship controls
        if event.key == pygame.K_LEFT:
            self.ship.red_moving_left = False
        if event.key == pygame.K_RIGHT:
            self.ship.red_moving_right = False
        if event.key == pygame.K_UP:
            self.ship.red_moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.red_moving_down = False   

    def _yellow_fire_bullet(self):
        if len(self.yellow_bullets) < self.settings.max_bullets:
            new_bullet = YellowBullet(self)
            self.yellow_bullets.add(new_bullet)
            self.fire_sound.play()

    def _red_fire_bullet(self):
        if len(self.red_bullets) < self.settings.max_bullets:
            new_bullet = RedBullet(self)
            self.red_bullets.add(new_bullet)
            self.fire_sound.play()

    def _update_yellow_bullets(self):
        """Update position of yellow bullets and get rid of old yellow bullets."""
        # Update yellow bullet positions.
        self.yellow_bullets.update()     

        # Get rid of yellow bullets that have disappeared.
        for bullet in self.yellow_bullets.copy():
            if bullet.yellow_bullet_rect.left >= self.screen_width:
                self.yellow_bullets.remove(bullet)
            self._check_yellow_bullet_redship_collisions()  

    def _update_red_bullets(self):
        """Update position of red bullets and get rid of old red bullets."""
        # Update red bullet positions.
        self.red_bullets.update()       

        # Get rid of red bullets that have disappeared.
        for bullet in self.red_bullets.copy():
            if bullet.red_bullet_rect.right <= 0:
                self.red_bullets.remove(bullet)
            self._check_red_bullet_yellowship_collisions()

    def _check_yellow_bullet_redship_collisions(self):
        """Respond to yellow bullet-redship collisions."""
        # Remove any yellow bullets that have collided.

        # Check for any yellow bullets that have hit the redship.
        #  If so, get rid of the yellow bullet.
        for bullet in self.yellow_bullets.copy():
            if bullet.yellow_bullet_rect.right >= self.rect_red.x and bullet.yellow_bullet_rect.colliderect(self.rect_red):
                # Destroy the yellow bullets.
                self.yellow_bullets.remove(bullet)
                self.hit_sound.play()
                self.red_lives -= randint(1, 10)

    def _check_red_bullet_yellowship_collisions(self):
        """Respond to red bullet-yellowship collisions."""
        # Remove any red bullets that have collided.

        # Check for any red bullets that have hit the yellowship.
        #  If so, get rid of the red bullet.
        for bullet in self.red_bullets.copy():
            if bullet.red_bullet_rect.left <= self.rect_yellow.right and bullet.red_bullet_rect.colliderect(self.rect_yellow):
                # Destroy the red bullets.
                self.red_bullets.remove(bullet)
                self.hit_sound.play()
                self.yellow_lives -= randint(1, 10)

    def _handle_gameover_events(self):
        """Handle the gameover events."""
        if self.yellow_lives <= 0:
            self.red_score += 1
            self.red_score_text = self.score_font.render(f"{self.red_score}", 1, "white")
            self.gameover_text = self.gameover_font.render(f"RED WINS!", 1, self.red_color)
            self.gameover_sound.play()
            self.busted = True

        if self.red_lives <= 0:
            self.yellow_score += 1
            self.yellow_score_text = self.score_font.render(f"{self.yellow_score}", 1, "white")
            self.gameover_text = self.gameover_font.render(f"YELLOW WINS!", 1, self.yellow_color)
            self.gameover_sound.play()
            self.busted = True

    def _update_screen(self):
        """Updates the screen display."""
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blit_ships()
        self.ship.blit_border()
        for bullet in self.yellow_bullets.sprites():
            bullet.draw_yellow_bullets()
        for bullet in self.red_bullets.sprites():
            bullet.draw_red_bullets()
        
        if self.yellow_lives <= 0:
            self.yellow_health_text = self.health_font.render(f"Health: 0%", 1, "white")
        elif self.red_lives <= 0:
            self.red_health_text = self.health_font.render(f"Health: 0%", 1, "white")
        else:
            self.yellow_health_text = self.health_font.render(f"Health: {self.yellow_lives}%", 1, "white")
            self.red_health_text = self.health_font.render(f"Health: {self.red_lives}%", 1, "white")
         
        self.screen.blit(self.yellow_health_text, (10, 10))
        self.screen.blit(self.red_health_text, (self.screen_width - self.red_health_text.get_width() - 10, 10))
        self.screen.blit(self.gameover_text, ((self.screen_width - self.gameover_text.get_width())//2, (self.screen_height - self.gameover_text.get_height())//2))
        self.screen.blit(self.yellow_score_text, (self.screen_width//2 - self.red_score_text.get_width() - 30, 10))
        self.screen.blit(self.red_score_text, (self.screen_width//2 + 30, 10))

        pygame.display.update()

if __name__ == "__main__":
    gf = GalaxyFighters()
    gf.run_game()