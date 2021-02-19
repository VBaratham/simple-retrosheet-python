import re

from retrosheet import HOME, AWAY
from .handler import Handler
"""
Handler to keep track of the current inning
"""

# Grounded double plays take the form $(%)$, triple plays $(%)$(%)$
# Lined double plays take the form $(B)$(%), triple plays $(B)$(%)$(%)
# Where "$" represents 1 or more fielders and "%" represents a runner (all digits)
doubleplay_regex = re.compile("(?:\d+\(\d\)\d+)|(?:\d+\(B\)\d+\(\d\))")
tripleplay_regex = re.compile("XXXXXXXXXX")

class Inning(Handler):
    def __init__(self):
        self.tot_outs = 0

    def handle_id(self):
        self.tot_outs = 0

    @property
    def inning(self):
        return (self.tot_outs // 6) + 1

    @property
    def out(self):
        return (self.tot_outs % 3)

    @property
    def at_bat(self):
        return (self.tot_outs % 6) // 3

    def __float__(self):
        return self.inning + (float(self.tot_outs) / 3.0)

    def handle_play(self, play):
        if (self.inning != play.inning) or (self.at_bat != play.homeaway):
            raise Exception("Lost track of # outs or inning. We think the inning is: {} with {} out, at bat = {}. Current play (not processed yet): {}".format(self.inning, self.out, self.at_bat, play))

        # TODO: replace this all w/ a regex

        # FLYOUT OR GROUNDOUT
        if play.event[0].isdigit():
            basic_play = play.event.split('/')[0]
            if tripleplay_regex.match(basic_play):
                self.tot_outs += 3
            elif doubleplay_regex.match(basic_play):
                self.tot_outs += 2
            else:
                self.tot_outs += 1
                


        # STRIKEOUT
        elif play.event[0] == 'K':
            if "B-" not in play.event: # Batter reached (i.e. passed ball)
                self.tot_outs += 1

        # CAUGHT STEALING
        elif play.event.startswith('CS'):
            # A runner is caught stealing iff there was no error on the pickoff attempt
            if play.event.find('E') == -1:
                self.tot_outs += 1

        # PICKOFF
            # A runner is picked off iff there was no error on the pickoff attempt
        elif play.event.startswith('PO'):
            if play.event.find('E') == -1:
                self.tot_outs += 1
                
        # FC for fielder's choice would be accompanied by X if an out was made
        # We take care of those below
    
        # Record an out for each runner caught advancing, indicated by
        # X in the "advance" part of the event string, which starts
        # after "."
        if '.' in play.event:
            self.tot_outs += play.event.split('.')[-1].count('X')

        print("Inning {}, {} out, at bat = {}".format(self.inning, self.out, self.at_bat))

