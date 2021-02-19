from retrosheet import HOME, AWAY
from .inning import Inning

"""
Handler to count the number of innings each player played
"""

class InningsPlayedStruct(object):
    """
    This struct stores the data we need to track for each team 
    in order to count innings played for each player
    """
    def __init__(self):
        # player ID of each player currently in the game, in batting order
        self.playerIDs = [''] * 10

        # inning each of those players joined the game
        self.when_entered = [0] * 10

        # when a player leaves the game or the game ends, their # innings played is stored here
        self.inn_played = {}
        

class InningsPlayed(Inning):
    def __init__(self):
        super(InningsPlayed, self).__init__()
        
        self.home = InningsPlayedStruct()
        self.away = InningsPlayedStruct()

    # Rename this function for readability. Calling float(self) to get
    # the current inning is pretty opaque - self.inning_as_float makes
    # a bit more sense.
    @property
    def inning_as_float(self):
        return self.__float__()

    def handle_start(self, start):
        self.playerIDs_home[start.battingorder] = start.playerID

    def handle_sub(self, sub):
        if sub.homeaway == AWAY:
            data = self.away
        elif sub.homeaway == HOME:
            data = self.home
        else:
            raise Exception("Unrecognized home/away in substituion. Current sub: {}".format(sub))

        # Find the outgoing player based on batting order
        outgoing = data.playerIDs[sub.battingorder]
        # and count his innings played
        data.inn_played[outgoing] = self.inning_as_float() - data.when_entered[outgoing]

        # Put the incoming player into the list of active players
        data.playerIDs[sub.battingorder] = sub.playerID
        # and record when he entered
        data.when_entered[sub.playerID] = self.inning_as_float()
        
    def handle_id(self, _id):
        """ New game """
        for data in (self.home, self.away):
            for playerID in data.playerIDs:
                if playerID: # index 0 (designated hitter) will be empty for NL. Also all will be empty before the first game
                    data.inn_played[playerID] = self.inning_as_float - data.when_entered[playerID]
                    
    def get_all_innings_played(self):
        return {**self.home.inn_played, **self.away.inn_played}
