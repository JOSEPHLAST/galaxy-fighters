class Settings:
    """Contains the game settings and parameters."""
    def __init__(self):
        # Screen settings
        self.screen_dimensions = 850, 600

        # Ship settings
        self.ship_dimensions = 40, 40
        self.ship_speed = 1
        self.lives = 100, 100

        # Border settings
        self.border_dimensions = 10, self.screen_dimensions[1]
        self.border_color = (0, 0, 0)

        # Bullet settings
        self.bullet_dimensions = 7, 4
        self.bullet_speed = 3
        self.max_bullets = 3
        self.bullet_colors = (255, 255, 0), (255, 0, 0)
        
        # Players scores
        self.players_scores = 0, 0