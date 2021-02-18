"""
Perform a linear regression to predict wins as a function of innings played by each player.
"""
from argparse import ArgumentParser

from retrosheet import Analysis
from retrosheet.handlers import InningsPlayed, Winner, GameTrigger

H5_FILENAME = "data.h5"
NPZ_FILENAME = "inn_played.npz"

def check_outdir(outfile):
    """
    Create outdir if it doesn't exist, and make sure it's empty if it does.
    """
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    elif len(os.listdir(outdir)) > 0:
        raise Exception("--data-dir must point to an empty directory if" + \
                        " --create-dataset is passed. Pass --force to continue anyways")
        

def create_dataset(data_dir, year_from, year_to):
    analysis = Analysis()

    # Register a handler that keeps track of the # of innings played by each player
    analysis.register_handler('inn_played', InningsPlayed())

    # Register a handler that keeps track of who's winning
    analysis.register_handler('winner', Winner())
    
    # Register a handler that fires a trigger called 'endofgame' at the end of each game
    analysis.register_handler('trigger', GameTrigger('endofgame'))

    # Define the function that will get called when this trigger fires
    # Here, we store the winning team and a dict mapping playerID to
    # number of innings played for the home and away teams. This
    # function will be passed the dictionary of handlers that we just
    # registered:

    ngames = 100 # TODO
    nplayers = len(utils.playerID_to_idx)
    
    wins_arr = np.array()
    inn_played_arr = csr_matrix((ngames, nplayers))
    
    def endofgame(handlers):
        inn_played_home = handlers['inn_played'].home.inn_played
        inn_played_away = handlers['inn_played'].away.inn_played
        # TODO: Convert each playerID to an integer code and place in sparse array

        winning_homeaway, winning_team = handlers['winner'].get_winning_team()
        # Create an array that's +1 or -1 for each player in the game based on
        # whether they won or lost


        # Finally, reset all handlers for the next game
        for handler in handlers.values():
            handler.reset()

    # Run the analysis we just set up to contruct these arrays
    analysis.run()

    # TODO: Save the arrays to disk

    
def regression(data_dir):
    pass


if __name__ == '__main__':
    parser = ArgumentParser(description="Linearly regress wins on innings played using the MLB retrosheet")
    parser.add_arugment("--year-from", "--start-year", type=int, required=False, default=2020,
                        help="First year to analyze")
    parser.add_arugment("--year-to", "--end-year", type=int, required=False, default=2020,
                        help="Last year to analyze")
    parser.add_argument("--data-dir", type=str, required=False, default='./regressionWARdata',
                        help="directory where data should be stored (if --create-dataset is" + \
                        " passed) and/or read from (if --regression is passed)")
    parser.add_argument("--create-dataset", type=bool, action='store_true', default=False,
                        help="Parse the MLB retrosheet to create the dataset for regression")
    parser.add_argument("--regression", type=bool, action='store_true', default=False,
                        help="Perform the regression")
    parser.add_argument("--overwrite", type=bool, action="store_true", default=False,
                        help="Overwrite the data directory if not empty")

    args = parser.parse_args()

    if args.create_dataset:
        check_outdir(args.data_dir)
        create_dataset(args.data_dir, args.year_from, args.year_to)

    if args.regression:
        regression(args.data_dir)
