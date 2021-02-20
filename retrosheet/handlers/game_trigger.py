from .handler import Handler
import logging as log
"""
This Handler just fires a trigger when it encounters an "ID" record, which terminates the previous game
"""

class GameTrigger(Handler):
    def __init__(self, trigger_name, fire_on_first=False):
        """
        Create a Handler that fires a trigger called `trigger_name` each
        time an ID record is encountered.

        @param trigger_name - name of the trigger to fire
        @param fire_on_first - if True, fire on the first ID record in the file.
                               Usually you would not want this because that's the
                               only ID record that doesn't indicate the end of a game.
                                
        """
        super(GameTrigger, self).__init__()
        self.trigger_name = trigger_name
        self.fire_on_first = fire_on_first
        self.prev_gameID = None
        self.current_gameID = None

    def advance_game(self, gameID):
        """
        Begin the next game
        """
        self.prev_gameID = self.current_gameID
        self.current_gameID = gameID
        if self.prev_gameID:
            # Was not first game
            return self.trigger_name

    def handle_id(self, _id):
        return self.advance_game(_id.gameID)

    def reset(self):
        self.error = False
