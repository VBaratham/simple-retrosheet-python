"""
Simple structs for Pythonifying the Event file from the MLB retrosheet
"""

__author__ = "Vyassa Baratham"

# TODO: home/away as named enum

class EventLine(object):
    """
    Base class for a line from the event file
    """
    pass

class ID(EventLine):
    def __init__(self, ID, gameID):
        self.ID = ID
        self.gameID = gameID

class Start(EventLine):
    def __init__(self, playerID, playername, homeaway, battingorder, position):
        self.playerID = playerID
        self.playername = playername
        self.homeaway = homeaway
        self.battingorder = battingorder
        self.position = position

class Sub(Start):
    """ 'sub' and 'start' lines have the exact same format """
    pass

class Play(EventLine):
    # TODO: Create a separate parser for the "play" subfield
    def __init__(self, inning, homeaway, playerID, count, pitches, play):
        self.inning = inning
        self.homeaway = homeaway
        self.playerID = playerID
        self.count = count
        self.pitches = pitches
        self.play = play

class Info(EventLine):
    def __init__(self, fieldname, data):
        self.fieldname = fieldname
        self.data = data

class Com(EventLine):
    def __init__(self, comment):
        self.comment = comment

    
class_for = {
    'id': ID,
    'start': Start,
    'sub': Sub,
    'play': Play,
    'info': Info,
    'com': Com,
}
    
def pythonify_line(line):
    """
    Turn one parsed line from the event file into one of the objects defined in this file
    @param line - array where each element is one field from one line of the event file
    """
    cls = class_for(line[0])
    return cls.from_arr(*line[1:])


