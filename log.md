###### 05.06.2020
Originally I had intended to generate test data consisting of encoded board layouts, which would be the primary engine for determining probabilistic victory outcomes given a certain board arrangement. However, quick research online showed that the number of possible chessboard layouts increases exponentially, reaching a theoretical limit similar to the number of atoms in the known universe... so after about a day's worth of process running and ~1600 games played, it was back to the drawing board (though I think that data may still prove useful later on).

My current plan is to devise different playing strategies based on algorithmic determinations given the current gameplay data (board layout, coverage, pieces present, turn number, etc). The plan is that, down the line, machine learning will use gameplay data to determine the best scenarios in which to apply these various playstyles.

I am currently working on an offensive playstyle, which attempts to create a the largest possible gulf between the players' piece scores and coverage scores (with the playing AI obviously being the larger valued of the two). Changing both players from random to offensive playstyles has increased single game run time (from ~1 to ~3 minutes).

I've decided to split the 'offensive' playstyle into 'offensive_pieces' and 'offensive_coverage' styles and test them against one another, just to see how the outcomes differ. 

Gameplay is significantly slower in my current test - the recursion and loops need to be optimized.


###### 06.06.2020
Yesterday's tests showed that all pairings ended in a draw with an endless move loop except for offensive_piece vs. offensive_piece.