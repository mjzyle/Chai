import models
import controller

white = models.Player('W')
black = models.Player('B')
board = controller.setup_board()
boards = []
board.append(board)

current_player = 'W'
in_progress = False
winner = None
turn = 1
playing = True
checkmate = False

while playing:
    ###########################################
    ## WHITE TURN
    ###########################################
    current_player = 'W'
    in_progress = True
    
    # Wait for white player to make move
    while in_progress:
        in_progress, board = white.make_move(board)

    boards.append(board)

    # Check if white player has won
    if checkmate:
        winner = 'White'
        playing = False
        break

    ###########################################
    ## BLACK TURN
    ###########################################
    current_player = 'B'
    in_progress = True

    # Wait for black player to make move
    while in_progress:
        in_progress, board = black.make_move(board)

    boards.append(board)

    # Check if black player has won
    if checkmate:
        winner = 'Black'
        playing = False
        break

    # Proceed to next turn
    turn += 1

print(winner + ' wins!')