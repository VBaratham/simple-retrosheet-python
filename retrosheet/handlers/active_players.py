from .handler import Handler
"""
Handler to keep a list of all players who were active in at least
one game in the sample we analyze
"""

class ActivePlayers(Handler):
    def __init__(self):
        playerIDs = set()

    def handle_start(self, start):
        self.playerIDs.add(start.playerID)
        
    def handle_sub(self, sub):
        self.playerIDs.add(sub.playerID)
    
