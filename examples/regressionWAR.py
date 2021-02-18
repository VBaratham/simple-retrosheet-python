"""
Perform a linear regression to predict wins as a function of innings played by each player.
"""
from retrosheet import Analysis
from retrosheet.handlers import InningsPlayed, Winner, GameTrigger


if __name__ == '__main__':
    analysis = Analysis()

    # Register a handler that keeps track of the # of innings played
    analysis.register_handler('inn_played', InningsPlayed())

    # Register a handler that keeps track of who's winning
    analysis.register_handler('winner', Winner())
    
    # Register a handler that fires a trigger called 'endofgame' at the end of each game
    analysis.register_handler('trigger', GameTrigger('endofgame'))

    # Define the function that will get called when this trigger fires
    # Here, we store the winning team and a dict mapping playerID to
    # number of innings played for the home and away teams. 
    # This function will be passed the dictionary of handlers that we just registered
    winners_arr = np.array() # What size? Should we do this in blocks of 10000 games or something?
    def endofgame(handlers):
        winning_homeaway, winning_team = handlers['winner'].get_winning_team()

        # convert winning_team to an integer code, store in winners_arr



        # Finally, reset all handlers for the next game
        for handler in handlers.values():
            handler.reset()
