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
tripleplay_regex = re.compile("(?:\d+\(\d\)\d+\(\d\)\d+)|(?:\d+\(B\)\d+\(\d\)\d+\)\d\))")

# {baserunner: B123} "X" {base advancing to: 123H} not followed by {error: "(*E*)"}
caughtadvancing_noerror_regex = re.compile("[B\d]X[H\d](?!\(\d*E\d*\))") 

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

        if play.event.startswith('K+'):
            # Strikeout + other event
            first_play, event = play.event.split('+')
            if "B-" not in play.event:
                self.tot_outs += 1
        elif play.event.startswith('W+'):
            first_play, event = play.event.split('+')
        else:
            event = play.event
            
        if (self.inning != play.inning) or (self.at_bat != play.homeaway):
            raise Exception("Lost track of # outs or inning. We think the inning is: {} with {} out, at bat = {}. Current play (not processed yet): {}".format(self.inning, self.out, self.at_bat, play))

        # TODO: replace this all w/ a regex

        # FLYOUT OR GROUNDOUT
        if event[0].isdigit():
            basic_play = event.split('/')[0]
            if "E" not in basic_play:
                if tripleplay_regex.match(basic_play):
                    self.tot_outs += 3
                elif doubleplay_regex.match(basic_play):
                    self.tot_outs += 2
                else:
                    self.tot_outs += 1
                

        # I think the best way to do this would be to split the play
        # on '+' and parse each separately (recursively?) (split the
        # entire play, not just the basic play before '/', because the
        # stuff after '/' applies only to the 2nd event)
        

        # STRIKEOUT
        elif event[0] == 'K':
            if "B-" not in play.event and "BX" not in event:
                # "B-" is Batter reached (i.e. passed ball)
                # "BX" is Batter out advancing, which is counted below
                self.tot_outs += 1

        # CAUGHT STEALING
        elif event.startswith('CS'):
            # A runner is caught stealing iff there was no error on the pickoff attempt
            if event.find('E') == -1:
                self.tot_outs += 1

        # PICKOFF
        # A runner is picked off iff there was no error on the pickoff attempt
        elif event.startswith('PO'):
            if event.find('E') == -1:
                self.tot_outs += 1
                
        # FC for fielder's choice would be accompanied by X if an out was made
        # We take care of those below
    
        # Record an out for each runner caught advancing, indicated by
        # X in the "advance" part of the event string, which starts
        # after "."
        if '.' in event:
            advances = event.split('.')[-1]
            out_advancing = len(caughtadvancing_noerror_regex.findall(advances))
            print(out_advancing)
            self.tot_outs += out_advancing

        print("Inning {}, {} out, at bat = {}".format(self.inning, self.out, self.at_bat))

