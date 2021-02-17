# simple-retrosheet-python
Barebones framework for parsing MLB Retrosheet https://www.retrosheet.org/

I created this to perform a linear regression of wins on innings
played simultaneously across all players (and seasons?
eventually?). This will be implemented under "examples". Hopefully,
this framework will be a useful starting point for other analyses
operating on complicated functions of play-by-play data.

The idea is to create a bunch of Handler objects which read each line
of the Event file and keep track of some property, like innings played
by each player, or total # of hits by each team's outfielders with 2
outs. A top-level Analysis object keeps track of these handlers, feeds
data to them, and responds to "triggers" which are requests from a
handler to write out some data or perform some other function
involving the data the Handlers have been keeping track of.

