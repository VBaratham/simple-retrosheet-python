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

# TODO: This should all be specifiable as a json or
# something... object types for each arg... etc.

class ID(EventLine):
    def __init__(self, gameID):
        self.gameID = gameID

class Version(EventLine):
    def __init__(self, version):
        self.version = version

class Start(EventLine):
    def __init__(self, playerID, playername, homeaway, battingorder, position):
        self.playerID = playerID
        self.playername = playername
        self.homeaway = int(homeaway)
        self.battingorder = int(battingorder)
        self.position = int(position)

    def __str__(self):
        return ','.join([
            self.playerID, self.playerName, self.homeaway, self.battingorder, self.position,
        ])

class Sub(EventLine):
    def __init__(self, playerID, playername, homeaway, battingorder, position):
        self.playerID = playerID
        self.playername = playername
        self.homeaway = int(homeaway)
        self.battingorder = int(battingorder)
        self.position = int(position)

    def __str__(self):
        return ','.join([
            self.playerID, self.playerName, self.homeaway, self.battingorder, self.position,
        ])

class Play(EventLine):
    # TODO: Create a separate parser for the "play" subfield
    def __init__(self, inning, homeaway, playerID, count, pitches, event):
        self.inning = int(inning)
        self.homeaway = int(homeaway)
        self.playerID = playerID
        self.count = count
        self.pitches = pitches
        self.event = event

    def __str__(self):
        return ','.join(str(x) for x in [
            self.inning, self.homeaway, self.playerID, self.count, self.pitches, self.event
        ])
    
class Info(EventLine):
    def __init__(self, fieldname, data):
        self.fieldname = fieldname
        self.data = data

class Data(EventLine):
    def __init__(self, *data):
        self.data = data

class Com(EventLine):
    def __init__(self, comment):
        self.comment = comment

    
class_for = {
    'id': ID,
    'version': Version,
    'start': Start,
    'sub': Sub,
    'play': Play,
    'info': Info,
    'data': Data,
    'com': Com,
}
    
def pythonify_line(line):
    """
    Turn one parsed line from the event file into one of the objects defined in this file
    @param line - array where each element is one field from one line of the event file.
                  The first element should be the field name.
    """
    cls = class_for[line[0]]
    return cls(*line[1:])


