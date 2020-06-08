###### 05.06.2020
Originally I had intended to generate test data consisting of encoded board layouts, which would be the primary engine for determining probabilistic victory outcomes given a certain board arrangement. However, quick research online showed that the number of possible chessboard layouts increases exponentially, reaching a theoretical limit similar to the number of atoms in the known universe... so after about a day's worth of process running and ~1600 games played, it was back to the drawing board (though I think that data may still prove useful later on).

My current plan is to devise different playing strategies based on algorithmic determinations given the current gameplay data (board layout, coverage, pieces present, turn number, etc). The plan is that, down the line, machine learning will use gameplay data to determine the best scenarios in which to apply these various playstyles.

I am currently working on an offensive playstyle, which attempts to create a the largest possible gulf between the players' piece scores and coverage scores (with the playing AI obviously being the larger valued of the two). Changing both players from random to offensive playstyles has increased single game run time (from ~1 to ~3 minutes).

I've decided to split the 'offensive' playstyle into 'offensive_pieces' and 'offensive_coverage' styles and test them against one another, just to see how the outcomes differ. 

Gameplay is significantly slower in my current test - the recursion and loops need to be optimized.


###### 06.06.2020
Yesterday's tests showed that all pairings ended in a draw with an endless move loop except for offensive_piece vs. offensive_piece.

At the moment we have four distinct playstyles (5 counting the random move style). What I need now is a metric or set of metrics to quantify which style is most useful in a given situation for the current player.

First I am going to try using four metrics to choose which play style to select in a given turn: (a) player piece score, (b) player coverage score, (c) opponent piece score, and (d) opponent cover score. For initial data collection I will randomly switch playstyle for each player during each turn. The dataset for each player will consist only of data from games in which that player won. If I collect this training data for the white player and then have that player play against a black player making random moves, I expect to observe a significant increase in the white player win rate.

Running a test run with 40 simulated games (max turns before stalemate: 500). First three games are all draws. I'm wondering if it would be better to split the coverage into 16-cell units (rather than the full 36 board spaces) to capture more useful data. Considering the maximum coverage score on a given cell is 10 (8 adjacent pieces + 2 non-adjacent knights), for one of either players, plus an additional balanced value of 0, there are (2 * 10 + 1)*n possible coverage maps (actually slightly less since there will never be cases of full or zero coverage), where n is the number of desired cells (36 by default, or 16 if we reduce). Therefore, for 36 cells we would expect 756 possible coverage layouts barring any rule restrictions on where pieces can be placed.

Looking at the original valid data pull of 1208 games, there are 444055 unique coverage layouts out of 457641 datapoints.

Running 40 test games took a little over 2 hours (split across four different processes). 40 runs yielded 12 wins (30% of total data is usable), 8 black (20%) and 4 white (10%).


###### 07.06 2020
I think I'm approaching the data collection stage incorrectly. 

I'm shifting my focus to optimizing some of my processes. First I am setting up an identical Linux virtual environment and writing a C script which uses OpenMP to multithread my main simulation method.

Running another test of 40 randomized style selection games having made a change to optimize processing. Instead of checking all 64 spaces on the board, I now keep track of indices where each piece is located, meaning the algorithm only needs to check at most 16 spaces per move. This is being executed in conjunction with my multithreading C program.

With optimizations this new run of 40 actually took ~10 minutes longer than yesterday's run. I'm not sure why that would be. I think the best bet for generating an initial amount of data in a reasonable amount of time is to decrease the number of moves until a draw based on the general number of moves needed for a player to win.

Running a quick analysis of 25 win matches (out of 80 aggregated from both yesterday and today), the statistics related to the number of moves across each game are:

    mean: 76 moves (rounded up from 75.32)
    median: 58 moves
    min: 17 moves
    max: 366
    range: 349

Therefore, I will run another simulation with matches capped at 80 to see how that goes. I am also bumping the total simulations up to 100. 

New run seems to be going faster - after about an hour we've already processed 27 simulations. Going to be running additional tasks which may slow down the execution from here on out.