"""
Perform a linear regression to predict wins as a function of innings played by each player.
"""
import os, sys
import pickle
import shutil
import logging as log


from argparse import ArgumentParser

import joblib

import numpy as np
import h5py
import scipy.sparse
from sklearn import linear_model

from retrosheet import Analysis, HOME, AWAY, utils, StopAnalysis
from retrosheet.handlers import InningsPlayed, Winner, GameTrigger, ActivePlayers

H5_FILENAME = "winlose.h5"
NPZ_FILENAME = "inn_played.npz"
RESULTS_FILENAME = "reg.pkl"

def load_h5(data_dir):
    with h5py.File(os.path.join(data_dir, H5_FILENAME), 'r') as infile:
        y = infile['y'][:]
        activeIDs = infile['activeIDs'][:]
        return y, activeIDs

def check_outdir(outdir, overwrite):
    """
    Create outdir if it doesn't exist, and make sure it's empty if it does.
    """
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    elif len(os.listdir(outdir)) > 0:
        if overwrite:
            shutil.rmtree(outdir)
            os.mkdir(outdir)
        else:
            raise Exception("--data-dir must point to an empty directory if" + \
                            " --create-dataset is passed. Pass --overwrite to continue anyways")
        

def create_dataset(event_files, data_dir, ngames):

    # Main analysis object
    analysis = Analysis(filenames=event_files)

    # Register a handler that keeps track of all players who play in
    # the sample of games we analyze. This is only used to trim the array
    # at the very end
    actives = ActivePlayers()
    analysis.register_handler('all_players', actives)

    # Register a handler that keeps track of the # of innings played by each player
    analysis.register_handler('inn_played', InningsPlayed())

    # Register a handler that keeps track of who's winning
    analysis.register_handler('winner', Winner())
    
    # Register a handler that fires a trigger called 'endofgame' at the end of each game
    analysis.register_handler('trigger', GameTrigger('endofgame'))

    # Define data structures where we will store analysis results
    nplayers = len(utils.playerID_to_idx)
    y = np.zeros(shape=2*ngames)
    # x = scipy.sparse.csr_matrix((2*ngames, nplayers))
    x = np.zeros(shape=(2*ngames, nplayers))

    game_i = 0 # counter of how many games we've processed
    # Index game_i * 2 + AWAY represents the away team of game game_i (AWAY = 0)
    # Index game_i * 2 + HOME represents the home team of game game_i (HOME = 1)
    
    # Define the function that will get called when this trigger fires.
    # This function will be passed the dictionary of handlers that we
    # just registered. In it, we populate the x and y arrays one game
    # at a time.

    def endofgame(handlers):
        nonlocal game_i
        log.info("Processing game {} ({} of {})".format(
            handlers['trigger'].prev_gameID, game_i, ngames
        ))

        # Check if any handlers errored. Only process this game's data if no handlers errored
        err_handlers = [h for h in handlers.values() if h.error]
        if err_handlers:
            log.info("Could not process game {} because of these errored handlers: {}".format(
                handlers['trigger'].current_gameID, err_handlers)
            )
            for handler in err_handlers:
                # In this analysis, we resolve errors by skipping the game
                # So there's no work to do before marking the error resolved.
                # The handler will get reset at the end of the game as usual.
                handler.resolve_error()
        else:
            # Grab the # of innings played by each player on the home and away teams
            inn_played_home = handlers['inn_played'].home.inn_played
            inn_played_away = handlers['inn_played'].away.inn_played

            away_i = game_i * 2 + AWAY
            home_i = game_i * 2 + HOME

            # Place this game's data in sparse array
            x[away_i, :] = utils.to_row(inn_played_away)
            x[home_i, :] = utils.to_row(inn_played_home)

            # TODO future: construct in standard CSR representation
            # see https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html

            # Determine who won and put +1 or -1 into the y vector
            winning_homeaway, winning_team = handlers['winner'].get_winning_team()
            if winning_homeaway == AWAY:
                y[away_i] = +1
                y[home_i] = -1
            else:
                y[away_i] = -1
                y[home_i] = +1

        # Finally, reset all handlers for the next game
        for hname in ['inn_played', 'winner']:
                handlers[hname].reset()

        game_i += 1
        if game_i >= ngames:
            raise StopAnalysis()



    # Register this trigger to the analysis:
    analysis.register_trigger('endofgame', endofgame)

    # Run the analysis we just set up to contruct these arrays
    analysis.run()

    # The final game does not end with 'id' record, so we need to manually
    # fire the trigger to process it:
    # analysis.handlers['trigger'].advance_game("lastgame")
    # analysis.fire_trigger('endofgame')

    # Trim columns of X representing players who didn't play
    # in the sample of games we analyzed, and convert to coo
    # sparse matrix format. We use coo because this page shows
    # coo is faster than dense matrix in lasso regression:
    # https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_dense_vs_sparse_data.html
    activeIDs = np.array([utils.playerID_to_idx[playerID] for playerID in actives.playerIDs])
    activeIDs = sorted(activeIDs)
    # x = x.tocsc()[:, activeIDs].tocoo()
    x = scipy.sparse.coo_matrix(x[:, activeIDs])

    # Save the arrays to disk
    scipy.sparse.save_npz(os.path.join(data_dir, NPZ_FILENAME), x)
    with h5py.File(os.path.join(data_dir, H5_FILENAME), 'w') as outfile:
        outfile.create_dataset('y', data=y)
        outfile.create_dataset('activeIDs', data=activeIDs)

    log.info("Saved datasets")

    return x, y, activeIDs
    
def regression(data_dir=None, x=None, y=None, activeIDs=None):
    # Load data if not passed in
    if x is None:
        x = scipy.sparse.load_npz(os.path.join(data_dir, NPZ_FILENAME)).todense()
    if y is None or activeIDs is None:
        y, activeIDs = load_h5(data_dir)

    # Perform linear regression
    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    import ipdb; ipdb.set_trace()

    # Save regression results to disk
    joblib.dump(reg, RESULTS_FILENAME)

    log.info("Done.")

if __name__ == '__main__':
    parser = ArgumentParser(description="Linearly regress wins on innings played using the MLB retrosheet")
    # parser.add_arugment("--year-from", "--start-year", type=int, required=False, default=2020,
    #                     help="First year to analyze")
    # parser.add_arugment("--year-to", "--end-year", type=int, required=False, default=2020,
    #                     help="Last year to analyze")
    parser.add_argument("--event-files", type=str, nargs='+', required=False, default=None,
                        help="Event file(s) from MLB retrosheet. Required if not using stdin")
    parser.add_argument("--data-dir", type=str, required=False, default='./regressionWARdata',
                        help="directory where data should be stored (if --create-dataset is" + \
                        " passed) and/or read from (if --regression is passed)")
    parser.add_argument("--create-dataset", action='store_true', default=False,
                        help="Parse the MLB retrosheet to create the dataset for regression")
    parser.add_argument("--regression", action='store_true', default=False,
                        help="Perform the regression")
    parser.add_argument("--overwrite", action="store_true", default=False,
                        help="Overwrite the data directory if not empty")
    parser.add_argument("--ngames", type=int, required=True,
                        help="How many games to analyze. Ignore all games after this.")
    parser.add_argument("--log", type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        required=False, default='warning',
                        help='set the level of log messages to see')
    # parser.add_argument("--logfile", type=str, required=False, default=None,
    #                     help="output the log to a file")

    args = parser.parse_args()

    log.getLogger().setLevel(getattr(log, args.log.upper()))

    if not args.create_dataset and not args.regression:
        raise Exception("Must pass either --create-dataset or --regression")

    x, y, activeIDs = None, None, None
    if args.create_dataset:
        check_outdir(args.data_dir, args.overwrite)
        x, y, activeIDs = create_dataset(args.event_files, args.data_dir, args.ngames)

    if args.regression:
        regression(data_dir=args.data_dir, x=x, y=y, activeIDs=activeIDs)
