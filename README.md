# simple-retrosheet-python
Barebones framework for parsing MLB Retrosheet https://www.retrosheet.org/

I created this to perform a linear regression of wins on innings played simultaneously across all players (and seasons? eventually?). This will be implemented under "examples". Hopefully, this framework will be a useful starting point for other analyses operating on data derived from the Retrosheet. 

In version 1, we will only look at the Event file https://www.retrosheet.org/game.htm containing play-by-play data. A similar structure will work for parsing the Game file https://www.retrosheet.org/game.htm but combining the two in the same analysis will require some thought.

The idea is to create a bunch of Handler objects which read each line of the Event file and keep track of some property, like innings played by each player, or errors by each team's 3rd baseman. A top-level Analysis object keeps track of these handlers, and decides what to do with the data they produce. 
