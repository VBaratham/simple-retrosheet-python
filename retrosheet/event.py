"""
Simple structs for Pythonifying the Event file from the MLB retrosheet
"""
import logging as log

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
        return ','.join(str(s) for s in [
            self.playerID, self.playername, self.homeaway, self.battingorder, self.position,
        ])

class Sub(EventLine):
    def __init__(self, playerID, playername, homeaway, battingorder, position):
        self.playerID = playerID
        self.playername = playername
        self.homeaway = int(homeaway)
        self.battingorder = int(battingorder)
        self.position = int(position)

    def __str__(self):
        return ','.join(str(s) for s in [
            self.playerID, self.playername, self.homeaway, self.battingorder, self.position,
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

class Padj(EventLine):
    # This allegedly only happened on 9/28/1995 (https://www.retrosheet.org/eventfile.htm)
    # But I'm seeing it in CIN201905040 from 2019
    def __init__(self, playerID, hand):
        self.playerID = playerID
        self.hand = hand

class Badj(EventLine):
    def __init__(self, playerID, hand):
        self.playerID = playerID
        self.hand = hand

class Radj(EventLine):
    def __init__(self, playerID, base):
        self.playerID = playerID
        self.base = base

    
class_for = {
    'id': ID,
    'version': Version,
    'start': Start,
    'sub': Sub,
    'play': Play,
    'info': Info,
    'data': Data,
    'com': Com,
    'padj': Padj,
    'badj': Badj,
    'radj': Radj,
}
    
def pythonify_line(line):
    """
    Turn one parsed line from the event file into one of the objects defined here.
    If the line is not recognized, return None and log an error
    @param line - array where each element is one field from one line of the event file.
                  The first element should be the field name.
    """
    fieldname = line[0]
    if fieldname not in class_for:
        log.error("Unrecognized fieldname in line: {}".format(line))
        return None
    cls = class_for[line[0]]
    return cls(*line[1:])


