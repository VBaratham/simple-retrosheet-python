import csv
import logging as log

import numpy as np

playerID_to_idx = {}
log.info("Loading playerIDs.csv...")
with open('playerIDs.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    i = 0
    for person in reader:
        if person['Play debut']:
            playerID_to_idx[person['ID']] = i
            i += 1
log.info("Done.")

def to_row(inn_played):
    """
    Given a playerID to innings played dict, return a row of the X matrix
    """
    row = np.zeros(shape=len(playerID_to_idx))
    for playerID, ip in inn_played.items():
        if playerID:
            row[playerID_to_idx[playerID]] = ip
    return row


