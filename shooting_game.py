import sys 

from time import sleep

import pygame

from settings import Settings

from game_stats import GameStats

from button import Button

from ship import Ship

from bullet import Bullet

from alien import Alien

from scoreboard import Scoreboard

class AlienInvasion:
    '''Overall class to manage game assests and behaior '''


    def __init__(self):
        ''' Initialize the game, and creat game resources'''
        pygame.init()
        self.settings=Settings()


        self.screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width= self.screen.get_rect().width
        self.settings.screen_height= self.screen.get_rect().height

        
        pygame.display.set_caption('Alien Invasion')

        #Create an instance to store game statistics

        # Create an intance to store game statistics
        #    and create a scoreboard


        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._create_fleet()

        #Make the Play button.
        self.play_button = Button(self,"Play")

        #bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)

        # Start Alien Invasion in an active state
        self.game_activate = True



    def run_game(self):
        '''Start the main loop for the game'''

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()          
            
            
            if self.stats.game_active:
                # Update ships positions
                self.ship.update()
                # Update positions of bullet and get rid of old bullets
                self._update_bullets()             
                # Update aliens positions
                self._update_aliens()

            # Updates the screen and flips it.
            self._update_screen()



    def _update_aliens(self):
        ''' Check if the fleet is at an edge,
        update the postion of all the aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        ''' Respond to the ship being hit by an alien.'''
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -=1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active=False

            pygame.mouse.set_visible(True)


    
            
    def _check_events(self):
        '''respond to keypress and mouse evnts.'''
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                print('somthing')
                sys.exit(0)
            elif event.type==pygame.KEYDOWN:
                 self._check_keydown_events(event)
                    
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self,mouse_pos):
        '''Start a new game when the player clicks Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Creat a  new fleet 
            self._create_fleet()
            self.ship.center_ship()
            # Hide mouse cursor
            pygame.mouse.set_visible(False)

                

    def _check_keydown_events(self,event):
        '''respond to key presses'''
        if event.key ==pygame.K_RIGHT:
        # Move the ship to the right.
            self.ship.moving_right=True          
        elif event.key ==pygame.K_LEFT:
        # Move the ship to the left.
            self.ship.moving_left=True
        elif event.key ==pygame.K_q:
            sys.exit(0)
        elif event.key ==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        '''respond to key releases'''
        if event.key==pygame.K_RIGHT:
        # Stops moving the ship to the right
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
        # Stops moving the ship to the left
            self.ship.moving_left=False


    def _fire_bullet(self):
        '''Creat a new bullet and add it to the bullet group.'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        ''' Update position of the bullets and get rid of old bullets.'''
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullet that have disapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
            print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_aliens_bottom(self):
        ''' Check if any aliens reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        
        
    def _check_bullet_alien_collisions(self):
        '''respond to bullet -alien collisions.'''
        # Remove to bullet and aliens that have collided.
        collisions=pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
    def _create_fleet(self):
         '''Create the fleet of aliens.'''
         #create an alien and finf the number of aliens in a row.
         #spacing between each alien is equal to one alien width.
         alien = Alien(self)
         alien_width, alien_height=alien.rect.size
         alien_width = alien.rect.width
         available_space_x = self.settings.screen_width - (2* alien_width)
         number_aliens_x = available_space_x//(2*alien_width)

         # Determine the number of rows of aliens that fit on the screen.
         ship_height = self.ship.rect.height
         availabel_space_y=(self.settings.screen_height -
                            (3 * alien_height)-ship_height)
         number_rows= availabel_space_y // (2*alien_height)


         #create the full fleet of aliens.
         for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #create an alien and place it in the row.
                self._create_alien(alien_number,row_number)


    def _create_alien(self, alien_number,row_number):
        '''Create an alien and place it in the row.'''
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x=alien_width + 2 * alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''respond appropriatly if any aliens have reached an edge.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''drop the entire fleet and change the directions.'''
        for alien in self.aliens.sprites():
            alien.rect.y +=self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1

    def _update_screen(self):
        ''' Update images on screen and flip to a new screen'''
         #redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()
        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # make the most recently drawn screen visible.
        pygame.display.flip()



        


if __name__=='__main__':
    # make a game instance, and run the game.
    ai=AlienInvasion()
    ai.run_game()

    

