from .handler import Handler
"""
Handler which keeps track of the current inning
"""

class Inning(Handler):
    def __init__(self):
        self.inning = 1
        self.outs = 0

    def _reset(self):
        self.inning = 1
        self.outs = 0

    def _record_out(self):
        self.outs = (self.outs + 1) % 3

        # This line is not really necessary because each play reports the inning
        # But we'll keep track of the inning ourselves to make sure we're counting
        # outs correctly
        self.inning += (0 if self.outs else 1) # if outs wrapped back to 0, self.inning++

    def as_float(self):
        return self.inning + (float(self.outs) / 3.0)

    def handle_play(self, play):
        if self.inning != play.inning:
            raise Exception("lost track of # outs or inning. Current play: {}".format(play))

        # TODO: look for "X" in the play record, call self.record_out()
