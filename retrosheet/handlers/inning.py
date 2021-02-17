from .handler import Handler
"""
Handler which keeps track of the current inning
"""

class Inning(Handler):
    def __init__(self):
        self.inning = 1
        self.outs = 0

    def handle_id(self):
        self.inning = 1
        self.outs = 0

    def _record_out(self, nouts=1):
        self.outs = (self.outs + nouts) % 3

        # This line is not really necessary because each play reports the inning
        # But we'll keep track of the inning ourselves to make sure we're counting
        # outs correctly
        if nouts > 0:
            self.inning += (0 if self.outs else 1) # if outs wrapped back to 0, self.inning++

    @property
    def inning_as_float(self):
        return self.__float__()

    def __float__(self):
        return self.inning + (float(self.outs) / 3.0)

    def handle_play(self, play):
        if self.inning != play.inning:
            raise Exception("lost track of # outs or inning. Current play: {}".format(play))

        # Call self._record_out() for each out on the play

        # TODO: replace this all w/ a regex

        # FLYOUT OR GROUNDOUT
        if play.event[0].isdigit():
            # If there is an opening parenthesis, it was a double play
            # If there are two, it was a triple play
            self._record_out(1 + play.event.count('('))

        # STRIKEOUT
        elif play.event[0] == 'K':
            self._record_out()

        # CAUGHT STEALING
        elif play.event.startswith('CS'):
            self.record_out()

        # PICKOFF
        elif play.event.startswith('PO'):
            # A runner is picked off iff there was no error on the pickoff attempt
            if play.event.find('E') == -1:
                self._record_out()
                
        # FC for fielder's choice would be accompanied by X if an out was made
        # We take care of those below
    
        # Record an out for each runner caught advancing, indicated by X
        self._record_out(play.event.count('X'))

