from .inning import Inning
from retrosheet import HOME, AWAY

"""
Handler which counts the number of innings each player played
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
        self.innings_played = {}
        

class InningsPlayed(Inning):
    def __init__(self):
        super(InningsPlayed, self).__init__()
        
        # # map each playerID to the inning (float) they entered
        # # when a player is removed from the game, they should be removed from this dict
        # self.when_entered = {}

        self.home = InningsPlayedStruct()
        self.away = InningsPlayedStruct()

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
        data.innings_played[outgoing] = self.inning_as_float() - data.when_entered[outgoing]

        # Put the incoming player into the list of active players
        data.playerIDs[sub.battingorder] = sub.playerID
        # and record when he entered
        data.when_entered[sub.playerID] = self.inning_as_float()
        
    def handle_id(self, _id):
        """ New game """
        for data in (self.home, self.away):
            for playerID in data.playerIDs:
                if playerID: # index 0 (designated hitter) will be empty for NL 
                    pass

    # Need to think about how to wrap up a game without resetting the structs, then reset them before the next game starts 
