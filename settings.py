class Settings:
    '''A class to store all the settings for the Alien invasion.'''

    def __init__(self):

        '''initialize the game's settings.'''

        # Screen settings
        self.screen_width=1200
        self.screen_hight=800
        self.bg_color=(225,116,0)
        # Ship settings
        self.ship_speed=3.0
        self.ship_limit=3
        # Bullet settings
        self.bullet_speed=10.0
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60, 60, 60)
        self.bullets_allowed=3
        # Alien settings
        self.alien_speed=1.0
        self.fleet_drop_speed=10
        # How quickly the game speeds up
        self.speedup_scale=1.5

        # How qucikly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        '''Initilize settings that change throughout the game.'''
        self.ship_speed = 3.0
        self.bullet_speed = 10.0
        self.alien_speed = 1.0
        
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction= 1
        
        #Scoring 
        self.alien_points=50 
    def increase_speed(self):
        '''Increase speed settings and alien point values.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        