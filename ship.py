import pygame
class Ship:
    '''A class to manage the ship'''
    def __init__(self,ai_game):
        '''initialize the ship and set its starting position''' 
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings

        # load the ship image and gets its rect.
        self.image=pygame.image.load('images/ship.BMP')
        self.rect =self.image.get_rect()
        # start each new ship at the bottom center of the screen. 
        self.rect.midbottom=self.screen_rect.midbottom
        # Store a decimal value for the ships horizontal position 
        self.x=float(self.rect.x)
        # Movement flag
        self.moving_right= False
        # Movement flag 2
        self.moving_left= False

    def update(self):
        '''update the ship's position based on the movement flag.'''
        # Update the ships x value, not the rect 
        if self.moving_right and (not self.moving_left) and (self.rect.right<self.screen_rect.right):
            self.x +=self.settings.ship_speed
        elif self.moving_left and (not self.moving_right) and (self.rect.left>0):
            self.x -=self.settings.ship_speed

        # Update rect objects from self.x
        self.rect.x=self.x

    def blitme(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        '''center the ship on the screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
