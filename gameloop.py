#!/usr/bin/python

import models
import controller
import pandas as pd
import datetime as dt
from copy import deepcopy
import random
import threading
import math
import sys
import os


def write_board_data(turn, current_player, board_start, board_end):
    board_start_enc = ''
    board_end_enc = ''
    coverage_start = ''
    coverage_end = ''

    # Encode board layouts before and after move is made
    for x in range(0, 8):
        for y in range(0, 8):
            if board_start.cells[x][y].piece is not None:
                board_start_enc += str(board_start.cells[x][y].piece)
            else:
                board_start_enc += '--'
            
            if board_end.cells[x][y].piece is not None:
                board_end_enc += str(board_end.cells[x][y].piece)
            else:
                board_end_enc += '--'

    # Encode board coverage before and after move is made
    for x in range(0, 8):
        for y in range(0, 8):
            coverage_start += ('-' if board_start.coverage_total[x][y][0] == '' else board_start.coverage_total[x][y][0]) + str(board_start.coverage_total[x][y][1])
            coverage_end += ('-' if board_end.coverage_total[x][y][0] == '' else board_end.coverage_total[x][y][0]) + str(board_end.coverage_total[x][y][1])

    data = {
        'Time': dt.datetime.now(),
        'Turn' : turn,
        'Moving Player': current_player.color,
        'Starting Board': board_start_enc, 
        'Ending Board': board_end_enc,
        'In Check' : board_end.in_check,
        'Starting Coverage' : coverage_start,
        'Ending Coverage' : coverage_end,
        'White Coverage Score': board_end.coverage_score_white,
        'Black Coverage Score': board_end.coverage_score_black,
        'White Piece Score' : board_end.piece_score_white,
        'Black Piece Score' : board_end.piece_score_black,
        'Style': current_player.style,
        'Black Pieces': len(board_end.black_pieces),
        'White Pieces': len(board_end.white_pieces),
        'Move Effectiveness Score' : board_end.last_move_eff
    }

    return data


def play_game(data_file, time_file, game, timeout):
    white = models.Player('W')
    black = models.Player('B')
    board = controller.setup_board()
    boards = pd.DataFrame()
    timing_data = pd.DataFrame()

    current_player = 'W'
    in_progress = False
    winner = 'Draw'
    turn = 1
    playing = True
    checkmate = False

    playstyles = {
        0: 'offensive_coverage',
        1: 'offensive_pieces',
        2: 'defensive_coverage',
        3: 'defensive_pieces'
    }

    turn_start = None
    turn_end = None

    while playing:
        turn_start = dt.datetime.now()

        ###########################################
        ## WHITE TURN
        ###########################################
        current_player = 'W'
        in_progress = True
        last_board = deepcopy(board)
        white.style = 'neural_network'
        
        # Wait for white player to make move
        while in_progress:
            checkmate, in_progress, board = white.make_move(board)

        boards = boards.append(write_board_data(turn, white, last_board, board), ignore_index=True)

        # Check if black player has won (no moves possible for white)
        if checkmate:
            if board.in_check != '':
                winner = 'Black'
            playing = False
            break


        ###########################################
        ## BLACK TURN
        ###########################################
        current_player = 'B'
        in_progress = True
        last_board = deepcopy(board)
        black.style = 'neural_network'

        # Wait for black player to make move
        while in_progress:
            checkmate, in_progress, board = black.make_move(board)

        boards = boards.append(write_board_data(turn, black, last_board, board), ignore_index=True)

        # Check if white player has won (no moves possible for black)
        if checkmate:
            if board.in_check != '':
                winner = 'White'
            playing = False
            break

        # Determine if play has reached a draw (only king pieces are left)
        black_pieces = 0
        white_pieces = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if board.cells[x][y].piece is not None:
                    if board.cells[x][y].piece.color == 'W':
                        white_pieces += 1
                    else:
                        black_pieces += 1
                if black_pieces > 1 or white_pieces > 1:
                    break
            if black_pieces > 1 or white_pieces > 1:
                    break

        if black_pieces == 1 and white_pieces == 1:
            playing = False

        # Record turn timing data
        turn_end = dt.datetime.now()
        print("    Game " + str(game) + ": Turn " + str(turn) + ": Time " + str(turn_end - turn_start) + ' (' + white.style + ' vs ' + black.style + ')')

        timing_data = timing_data.append({
            'Game' : game,
            'Turn' : turn,
            'Time' : turn_end - turn_start,
            'White Style' : white.style,
            'Black Style' : black.style,
            'White Pieces' : len(board.white_pieces),
            'Black Pieces' : len(board.black_pieces)
        }, ignore_index=True)

        # Proceed to next turn
        turn += 1

        # Automatic stalemate after n turns or when only two kings are left standing
        if turn > timeout:
            playing = False
            break

    boards['Winner'] = winner
    boards['Turns'] = turn
    boards.to_csv(data_file)
    timing_data.to_csv(time_file)

    print('Winner: ' + winner)
    print('Turns: ' + str(turn))
    print(board)

    return winner, turn


def run_games(start, end):
    # Determine where to start numbering new runs (relative to current number of total data points for future training)
    root_start = 0
    files = os.listdir('raw_data/training')

    i = 0
    while i < len(files):
        if files[i][-4:] != '.csv':
            files.pop(i)
        else:
            i += 1

    root_start = len(files)
    
    for i in range(start, end+1):
        print('Playing game ' + str(i))
        winner, turns = play_game('raw_data/game_' + str(root_start+i) + '.csv', 'raw_data/timing/game_' + str(root_start+i) + '_timing.csv', i, 500)


game_start = int(sys.argv[1])
game_end = int(sys.argv[2])

start = dt.datetime.now()
run_games(game_start, game_end)
end = dt.datetime.now()

print('Start: ' + str(start))
print('End: ' + str(end))