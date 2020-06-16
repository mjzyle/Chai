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


###### 08.06.2020
Data from last night's run of 200 simulations:
    
    Start: 2020-06-07 22:08:02.422028
    End: 2020-06-08 06:19:42.605226

Actually took less time and not more - yesterday's observation may have been due to some misstep on my part.

Across four simulation runs there are a total of 67 valid games (i.e. games where one of the two players wins). This will by my initial training set for classifying playstyles based on board coverage and piece scores.

My initial thought in looking at the wins data is this: for each turn I give each player three numerical scores based on (a) their board coverage, (b) the number of pieces they still have on the board, and (c) the total "score" of their pieces (with more valuable pieces being scored higher). I could create a single metric based on a weighted sum of these three values:

    M = w_cover * cover + w_piece_score * piece_score + w_piece_count * piece_count

where w represents the weights. The value of M will dictate which playstyle the algorithm should use (offensive or defensive). I could further train the model to modify these weights based on which scores it determines to be most integral in increasing the win likelihood.

Another idea I am considering comes from the fact that this algebraic metric approach reminds me of a linear programming problem. What if I model a simple LP attempting to maximize this metric, and then with binary values representing which playstyle is selected?

Doing some browsing online shows that my first thought is most in line with a neural network (not necessarily a ML classification problem like I was originally thinking).

The new question I am considering with a neural network is: how do I determine what a successful/'actual' outcome is in order to calculate the mean square error as my cost function? I think this route would need to use a single one of my play styles and use the network to select from each individual move. For example, suppose we are playing offensively. If a move increases the delta between the moving player's coverage and the opponent's coverage, that is a good move. If it reduces this delta, it's a bad move and the cost function will show that. Rather than selecting a playstyle (which then determines a move), we select a move directly.

What if our neural network produces a percentage ranking of how beneficial a move would be? We could then compare this ranking for all moves and chose the best one. The ranking of each move could depend on these data factors (such as coverage, the number of pieces the opponent/player have, potential moves that this would open for the opponent, etc.). 

I am going to implement a new prototype based on this structure. Each potential move will be judged based on a neural network using five metrics:

    a) Does the move increase the player's board coverage delta over the opponent? (increasing board positioning)
    b) Does the move increase the player's piece score delta over the opponent? (capturing opponent pieces)
    c) Does the move increase friendly coverage surrounding the player's king? (increase player defenses)
    d) Does the move decrease opponent coverage surrounding the opponent's king? (reduce opponent defenses)
    e) Does the move open up an opportunity for the opponent to immediately make a move which undoes or exceeds any of these effects (a through d)?

This metric will be calculated for each move, and the move with the highest metric will be performed.

The cost function will be applied and weights/biases adjusted through backpropogation at the end of each game. The cost function will be an algebraic representation of the following to judge whether the moves were successful or not:

    a) Did the player win the game?
    b) What proportion of player moves in the game were "good moves" in comparision to the opponent? A "good move" is one where the opponent's immediate responding move had a lower effectiveness score (see above).


###### 09.06.2020
I've been playing with the design for the neural network, experimenting with TensorFlow. I've decided that the simplest option is to have a binary classification problem. My thinking is: the network receives as inputs data related to the board coverage and piece layout. It then predicts whether this layout will lead to a win or a loss. The gameplay algorithm will generate these predictions for every possible move it can make in a given turn, and from there make a choice on how to proceed.

The data is already collected. I did some cleanup so from here on out it should be easier to organize training data.


###### 12.06.2020
I've managed to implement model-based predictions into the current gameplay loop. However, there is a need to validate the data encoding/decoding to ensure results are consistent for both black and white pieces. My next focus is on reorganizing the code as a whole.


###### 14.06.2020
Reorganized code into separate model/controller files based on gameplay, AI, and data processing functions.

I took a look at how I'm recording the training daya and realized I can record each board layout as both a win and a loss (provided the orientations are flipped). I changed the code to do just that. I'm currently running a 10-game test using this new training set of ~12,000 datapoints. My hypothesis is that the board score (metric between 0.0 and 1.0) should hover around 0.5 early in the game, then gravitate towards either 1.0 or 0.0 depending on the likelihood of winning or losing.

A good next step is optimizing the neural network to save after training. That way it only needs to be trained once for each batch of simulations. Currently it is retraining for each player, for each game.

Ended the simulation to make a quick change in the C script. The program now trains and saves the model once before all simulations begin, then loads the model for each individual sim. Kicked off the same 10-game test again.

Just a thought - what if I were to record draws as losses and use those datapoints in training?


###### 15.06.2020
Approximate runtime details for yesterday's 201 game simulation (taken from 1 thread of 4, not including model training time):
    
    Start: 2020-06-14 14:11:13.102297
    End: 2020-06-15 03:07:29.432949

Gameplay results:

    Total games: 201
    White wins: 11 (5.47%)
    Black wins: 36 (17.91%)

Today's plan is to run two tests. First will be to rerun yesterday's simulation exactly with the added data, to see if the algorithm is actually learning. What we should observe is that the percentage of white wins should increase with more board data added.

The second test will be doing the same, only including draw games as universal losses. We are looking for a similar outcome.

In the interest of time, I will run 100 simulations of each, beginning with the non-draw data.

While the first test is running, fixed a small bug that was producing extra simulations (after dividing into threads the boundary sims were actually overwriting). Simulations from here on out should cap at the end value.

Test 1 results (100 sims, new data added, wins only):

    (Timing data from final completed thread)
    Start: 2020-06-15 10:17:01.350281
    End: 2020-06-15 17:19:17.890493
    Total games: 101
    White wins: 3 (0.0297029702970297)
    Black wins: 19 (0.18811881188118812)

The network was actually less effective (winning just shy of 3% of games) with more data... 

Running test 2 with the exact same dataset, only counting draws as losses. Draws are counted as two losses (once for the white and once for the black loss).

The data aggregation step is taking longer than expected (due to the massive amount of new datafiles from draw games). Leaving the data to compile overnight.
