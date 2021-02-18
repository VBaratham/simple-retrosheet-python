import csv

playerID_to_idx = {}
print("Loading playerIDs.csv...")
with open('playerIDs.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    i = 0
    for person in reader:
        if person['Play debut']:
            playerID_to_idx[person[ID]] = i
            i += 1
print("Done.")

def playerIDs_to_idx(playerIDs):
    """
    Compute index (array positions) for the given list of playerIDs
    """
    
