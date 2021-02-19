from retrosheet import HOME, AWAY
from .handler import Handler
"""
Handler to determine who won the game by comparing the winning pitcher to the rosters
"""
class Winner(Handler):
    def __init__(self):
        # List of pitchers for the home and away teams
        self.pitcherIDs = [set(), set()]

        # Visiting and home team names, to be found from info records
        self.visteam = None
        self.hometeam = None

        # Winning pitcher, also to be found from info records
        self.wp = None

    def handle_start(self, start):
        if start.position == 1:
            self.pitcherIDs[start.homeaway].add(start.playerID)

    def handle_sub(self, sub):
        self.handle_start(sub)

    def handle_info(self, info):
        if info.fieldname == 'visteam':
            self.visteam = info.data
        elif info.fieldname == 'hometeam':
            self.hometeam = info.data
        elif info.fieldname == 'wp':
            self.wp = info.data

    def get_winning_team(self):
        """
        Compute the winning team by comparing the winning pitcher against the two rosters

        First return value is 0 or 1 indicating away/home team won
        Second return value is that team's name
        """
        assert self.visteam, "Must encounter info 'visteam' before computing winning team"
        assert self.hometeam, "Must encounter info 'hometeam' before computing winning team"
        assert self.wp, "Must encounter info 'wp' before computing winning team"

        if self.wp in self.pitcherIDs[HOME]:
            assert self.wp not in self.pitcherIDs[AWAY], "Winning pitcher can't be on both teams"
            return HOME, self.hometeam
        else:
            assert self.wp in self.pitcherIDs[AWAY], "Winning pitcher has to be on the other team"
            return AWAY, self.awayteam
