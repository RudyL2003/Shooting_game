class GameStats:
    '''Track statistics for Alien Invasion.'''

    def __init__(self,ai_game):
        '''iniitialize statistics'''
        self.settings=ai_game.settings
        self.reset_stats()

        # Start game inn an inactive state.
        self.game_active = False

    def reset_stats(self):
        '''initialize statistic that can change during the game.'''
        self.ships_left = self.settings.ship_limit
        self.score = 0

        # Start alien invasion in an active state.
        self.game_active = True
