import gameplay_models as models
import math
import pandas as pd
import datetime as dt
import os
import random
from copy import deepcopy


# Return a board initialized for gameplay
def setup_board():
    board = models.Board()
    temp = board.cells

    # Setup black pieces
    temp[7][0].piece = models.Piece('B', 'R', 0, 0, 'pieces/black_rook.png')
    temp[7][1].piece = models.Piece('B', 'N', 0, 1, 'pieces/black_knight.png')
    temp[7][2].piece = models.Piece('B', 'B', 0, 2, 'pieces/black_bishop.png')
    temp[7][3].piece = models.Piece('B', 'Q', 0, 3, 'pieces/black_queen.png')
    temp[7][4].piece = models.Piece('B', 'K', 0, 4, 'pieces/black_king.png')
    temp[7][5].piece = models.Piece('B', 'B', 0, 5, 'pieces/black_bishop.png')
    temp[7][6].piece = models.Piece('B', 'N', 0, 6, 'pieces/black_knight.png')
    temp[7][7].piece = models.Piece('B', 'R', 0, 7, 'pieces/black_rook.png')

    for i in range(0, 8):
        temp[6][i].piece = models.Piece('B', 'P', 1, i, 'pieces/black_pawn.png')

    # Setup white pieces
    temp[0][0].piece = models.Piece('W', 'R', 7, 0, 'pieces/white_rook.png')
    temp[0][1].piece = models.Piece('W', 'N', 7, 1, 'pieces/white_knight.png')
    temp[0][2].piece = models.Piece('W', 'B', 7, 2, 'pieces/white_bishop.png')
    temp[0][3].piece = models.Piece('W', 'Q', 7, 3, 'pieces/white_queen.png')
    temp[0][4].piece = models.Piece('W', 'K', 7, 4, 'pieces/white_king.png')
    temp[0][5].piece = models.Piece('W', 'B', 7, 5, 'pieces/white_bishop.png')
    temp[0][6].piece = models.Piece('W', 'N', 7, 6, 'pieces/white_knight.png')
    temp[0][7].piece = models.Piece('W', 'R', 7, 7, 'pieces/white_rook.png')

    for i in range(0, 8):
        temp[1][i].piece = models.Piece('W', 'P', 6, i, 'pieces/white_pawn.png')

    # Setup lists to track where pieces are located on the board (to remove need to check every cell)
    for x in range(0, 2):
        for y in range(0, 8):
            board.white_pieces.append([x, y])
            board.black_pieces.append([7-x, y])

    board.cells = temp

    return update_coverage(board)


# Determine legal moves
def get_legal_moves(board, x, y): 
    piece = board.cells[x][y].piece
    legal_moves = []


    # PAWN MOVEMENT RULES
    if piece.role == 'P':
        # Determine the pawn's directionality based on its color (white is descending index, black is ascending index)
        desc = False
        if piece.color == 'B':
            desc = True

        if desc:
            # Determine if the pawn can move one space
            try:
                if board.cells[x-1][y].piece is None:
                    legal_moves.append(models.Move(x, y, x-1, y))
            except IndexError:
                pass
            
            # Determine if the pawn has made a first move; if not, it can move either one or two spaces
            try:
                if piece.moves == 0 and board.cells[x-1][y].piece is None and board.cells[x-2][y].piece is None:
                    legal_moves.append(models.Move(x, y, x-2, y))
            except IndexError:
                pass

            # Determine if the pawn can capture any diagonal opponent pieces
            try:
                if board.cells[x-1][y-1].piece is not None and board.cells[x-1][y-1].piece.color is not piece.color:
                    legal_moves.append(models.Move(x, y, x-1, y-1))
            except IndexError:
                pass

            try:
                if board.cells[x-1][y+1].piece is not None and board.cells[x-1][y+1].piece.color is not piece.color:
                    legal_moves.append(models.Move(x, y, x-1, y+1))
            except IndexError:
                pass

        else:
            # Determine if the pawn can move one space
            try:
                if board.cells[x+1][y].piece is None:
                    legal_moves.append(models.Move(x, y, x+1, y))
            except IndexError:
                pass
            
            # Determine if the pawn has made a first move; if not, it can move either one or two spaces
            try:
                if piece.moves == 0 and board.cells[x+1][y].piece is None and board.cells[x+2][y].piece is None:
                    legal_moves.append(models.Move(x, y, x+2, y))
            except IndexError:
                pass

            # Determine if the pawn can capture any diagonal opponent pieces
            try:
                if board.cells[x+1][y-1].piece is not None and board.cells[x+1][y-1].piece.color is not piece.color:
                    legal_moves.append(models.Move(x, y, x+1, y-1))
            except IndexError:
                pass

            try:
                if board.cells[x+1][y+1].piece is not None and board.cells[x+1][y+1].piece.color is not piece.color:
                    legal_moves.append(models.Move(x, y, x+1, y+1))
            except IndexError:
                pass

    # ROOK MOVEMENT RULES
    elif piece.role == 'R':
        # Determine moves possible along x-axis
        for i in range(x+1, 8):
            if board.cells[i][y].piece is None:
                legal_moves.append(models.Move(x, y, i, y))
            elif board.cells[i][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, y))
                break
            elif board.cells[i][y].piece.color is piece.color:
                break

        for i in reversed(range(0, x)):
            if board.cells[i][y].piece is None:
                legal_moves.append(models.Move(x, y, i, y))
            elif board.cells[i][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, y))
                break
            elif board.cells[i][y].piece.color is piece.color:
                break

        # Determine moves possible along y-axis
        for i in range(y+1, 8):
            if board.cells[x][i].piece is None:
                legal_moves.append(models.Move(x, y, x, i))
            elif board.cells[x][i].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, i))
                break
            elif board.cells[x][i].piece.color is piece.color:
                break

        for i in reversed(range(0, y)):
            if board.cells[x][i].piece is None:
                legal_moves.append(models.Move(x, y, x, i))
            elif board.cells[x][i].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, i))
                break
            elif board.cells[x][i].piece.color is piece.color:
                break

    # KNIGHT MOVEMENT RULES
    elif piece.role == 'N':
        try:
            if board.cells[x+1][y+2].piece is None or board.cells[x+1][y+2].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+1, y+2))
        except IndexError:
            pass

        try:
            if board.cells[x+2][y+1].piece is None or board.cells[x+2][y+1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+2, y+1))
        except IndexError:
            pass

        try:
            if board.cells[x-1][y-2].piece is None or board.cells[x-1][y-2].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-1, y-2))
        except IndexError:
            pass

        try:
            if board.cells[x-2][y-1].piece is None or board.cells[x-2][y-1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-2, y-1))
        except IndexError:
            pass

        try:
            if board.cells[x-2][y+1].piece is None or board.cells[x-2][y+1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-2, y+1))
        except IndexError:
            pass

        try:
            if board.cells[x+2][y-1].piece is None or board.cells[x+2][y-1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+2, y-1))
        except IndexError:
            pass

        try:
            if board.cells[x-1][y+2].piece is None or board.cells[x-1][y+2].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-1, y+2))
        except IndexError:
            pass

        try:
            if board.cells[x+1][y-2].piece is None or board.cells[x+1][y-2].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+1, y-2))
        except IndexError:
            pass

    # BISHOP MOVEMENT RULES
    elif piece.role == 'B':
        # Check +/+ axis
        i = x + 1
        j = y + 1
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x - 1
        j = y - 1
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x + 1
        j = y - 1
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x - 1
        j = y + 1
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i -= 1
            j += 1

    # QUEEN MOVEMENT RULES
    elif piece.role == 'Q':
        # Check +/+ axis
        i = x + 1
        j = y + 1
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x - 1
        j = y - 1
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x + 1
        j = y - 1
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x - 1
        j = y + 1
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            else:
                break
            i -= 1
            j += 1

        # Determine moves possible along x-axis
        for i in range(x+1, 8):
            if board.cells[i][y].piece is None:
                legal_moves.append(models.Move(x, y, i, y))
            elif board.cells[i][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, y))
                break
            elif board.cells[i][y].piece.color is piece.color:
                break

        for i in reversed(range(0, x)):
            if board.cells[i][y].piece is None:
                legal_moves.append(models.Move(x, y, i, y))
            elif board.cells[i][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, y))
                break
            elif board.cells[i][y].piece.color is piece.color:
                break

        # Determine moves possible along y-axis
        for i in range(y+1, 8):
            if board.cells[x][i].piece is None:
                legal_moves.append(models.Move(x, y, x, i))
            elif board.cells[x][i].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, i))
                break
            elif board.cells[x][i].piece.color is piece.color:
                break

        for i in reversed(range(0, y)):
            if board.cells[x][i].piece is None:
                legal_moves.append(models.Move(x, y, x, i))
            elif board.cells[x][i].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, i))
                break
            elif board.cells[x][i].piece.color is piece.color:
                break

    # KING MOVEMENT RULES
    elif piece.role == 'K':
        try:
            if board.cells[x+1][y].piece is None or board.cells[x+1][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+1, y))
        except IndexError:
            pass

        try:
            if board.cells[x+1][y+1].piece is None or board.cells[x+1][y+1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+1, y+1))
        except IndexError:
            pass

        try:
            if board.cells[x][y+1].piece is None or board.cells[x][y+1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, y+1))
        except IndexError:
            pass

        try:
            if board.cells[x-1][y].piece is None or board.cells[x-1][y].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-1, y))
        except IndexError:
            pass

        try:
            if board.cells[x-1][y-1].piece is None or board.cells[x-1][y-1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-1, y-1))
        except IndexError:
            pass

        try:
            if board.cells[x][y-1].piece is None or board.cells[x][y-1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x, y-1))
        except IndexError:
            pass

        try:
            if board.cells[x+1][y-1].piece is None or board.cells[x+1][y-1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x+1, y-1))
        except IndexError:
            pass

        try:
            if board.cells[x-1][y+1].piece is None or board.cells[x-1][y+1].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, x-1, y+1))
        except IndexError:
            pass

        # Check for castle
        # King hasn't yet moved
        if piece.moves == 0:
            # Left rook hasn't yet moved
            if board.cells[x][0].piece is not None and (board.cells[x][0].piece.moves == 0) and board.cells[x][1].piece is None and board.cells[x][2].piece is None and board.cells[x][3].piece is None:
                legal_moves.append(models.Move(x, y, x, y-2, models.Move(x, 0, x, y-1)))

            # Right rook hasn't yet moved
            if board.cells[x][7].piece is not None and (board.cells[x][7].piece.moves == 0) and board.cells[x][6].piece is None and board.cells[x][5].piece is None:
                legal_moves.append(models.Move(x, y, x, y+2, models.Move(x, 7, x, y+1)))


    # Remove any moves with negative array indices or indices > 7
    i = 0
    while i < len(legal_moves):
        move = legal_moves[i].end

        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            legal_moves.pop(i)
        else:
            i += 1


    return legal_moves


# Determine which pieces cover other spaces on the board
def get_cover_moves(board, x, y):
    piece = board.cells[x][y].piece
    cover_moves = []

    # PAWN MOVEMENT RULES
    if piece.role == 'P':
        # Determine the pawn's directionality based on its color (white is descending index, black is ascending index)
        desc = False
        if piece.color == 'B':
            desc = True

        if desc:
            try:
                cover_moves.append(models.Move(x, y, x-1, y-1))
            except IndexError:
                pass
                
            try:
                cover_moves.append(models.Move(x, y, x-1, y+1))
            except IndexError:
                pass

        else:
            try:
                cover_moves.append(models.Move(x, y, x+1, y-1))
            except IndexError:
                pass
                
            try:
                cover_moves.append(models.Move(x, y, x+1, y+1))
            except IndexError:
                pass

    # ROOK MOVEMENT RULES
    elif piece.role == 'R':
        # Determine moves possible along x-axis
        for i in range(x+1, 8):
            if board.cells[i][y].piece is None:
                cover_moves.append(models.Move(x, y, i, y))
            else:
                cover_moves.append(models.Move(x, y, i, y))
                break

        for i in reversed(range(0, x)):
            if board.cells[i][y].piece is None:
                cover_moves.append(models.Move(x, y, i, y))
            else:
                cover_moves.append(models.Move(x, y, i, y))
                break

        # Determine moves possible along y-axis
        for i in range(y+1, 8):
            if board.cells[x][i].piece is None:
                cover_moves.append(models.Move(x, y, x, i))
            else:
                cover_moves.append(models.Move(x, y, x, i))
                break

        for i in reversed(range(0, y)):
            if board.cells[x][i].piece is None:
                cover_moves.append(models.Move(x, y, x, i))
            else:
                cover_moves.append(models.Move(x, y, x, i))
                break

    # KNIGHT MOVEMENT RULES
    elif piece.role == 'N':
        try:
            cover_moves.append(models.Move(x, y, x+1, y+2))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x+2, y+1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-1, y-2))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-2, y-1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-2, y+1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x+2, y-1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-1, y+2))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x+1, y-2))
        except IndexError:
            pass

    # BISHOP MOVEMENT RULES
    elif piece.role == 'B':
        # Check +/+ axis
        i = x + 1
        j = y + 1
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x - 1
        j = y - 1
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x + 1
        j = y - 1
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x - 1
        j = y + 1
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j += 1

    # QUEEN MOVEMENT RULES
    elif piece.role == 'Q':
        # Check +/+ axis
        i = x + 1
        j = y + 1
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x - 1
        j = y - 1
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x + 1
        j = y - 1
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x - 1
        j = y + 1
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                cover_moves.append(models.Move(x, y, i, j))
            else:
                cover_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j += 1

        # Determine moves possible along x-axis
        for i in range(x+1, 8):
            if board.cells[i][y].piece is None:
                cover_moves.append(models.Move(x, y, i, y))
            else:
                cover_moves.append(models.Move(x, y, i, y))
                break

        for i in reversed(range(0, x)):
            if board.cells[i][y].piece is None:
                cover_moves.append(models.Move(x, y, i, y))
            else:
                cover_moves.append(models.Move(x, y, i, y))
                break

        # Determine moves possible along y-axis
        for i in range(y+1, 8):
            if board.cells[x][i].piece is None:
                cover_moves.append(models.Move(x, y, x, i))
            else:
                cover_moves.append(models.Move(x, y, x, i))
                break

        for i in reversed(range(0, y)):
            if board.cells[x][i].piece is None:
                cover_moves.append(models.Move(x, y, x, i))
            else:
                cover_moves.append(models.Move(x, y, x, i))
                break

    # KING MOVEMENT RULES
    elif piece.role == 'K':
        try:
            cover_moves.append(models.Move(x, y, x+1, y))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x+1, y+1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x, y+1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-1, y))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-1, y-1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x, y-1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x+1, y-1))
        except IndexError:
            pass

        try:
            cover_moves.append(models.Move(x, y, x-1, y+1))
        except IndexError:
            pass


    # Remove any moves with negative array indices or indices > 7
    i = 0
    while i < len(cover_moves):
        move = cover_moves[i].end

        if move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7:
            cover_moves.pop(i)
        else:
            i += 1


    return cover_moves


# Takes as input a list of legal moves and removes any moves which would place the player in check
def remove_check_moves(board, moves, player_color):
    legal_moves = moves

    # Remove any moves that would place the king in check
    m = 0
    while m < len(legal_moves):
        move = legal_moves[m]
        temp_board = deepcopy(board)
        temp_board = perform_move(player_color, temp_board, move)

        # Determine all possible moves that the opponent could make in the event that the king makes this move
        opponent_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                if temp_board.cells[i][j].piece is not None and temp_board.cells[i][j].piece.color is not player_color:
                    opponent_moves += get_legal_moves(temp_board, i, j)

        # If the opponent can make a legal move that would match the new location of the king, then the king's current move is illegal (remove it)
        for opp_move in opponent_moves:
            if temp_board.cells[opp_move.end[0]][opp_move.end[1]].piece is not None and temp_board.cells[opp_move.end[0]][opp_move.end[1]].piece.role == 'K' and temp_board.cells[opp_move.end[0]][opp_move.end[1]].piece.color == player_color:
                legal_moves.pop(m)
                m -= 1
                break

        m += 1

    return legal_moves


# Determine if a move has placed a player in check
def determine_check(board, last_player_color):
    new_board = board

    if last_player_color == 'B':
        pieces = board.black_pieces
    elif last_player_color == 'W':
        pieces = board.white_pieces

    for piece in pieces:

        # Determine piece coverage moves
        moves = get_cover_moves(new_board, piece[0], piece[1])

        for move in moves:
            if new_board.cells[move.end[0]][move.end[1]].piece is not None and new_board.cells[move.end[0]][move.end[1]].piece.color != last_player_color and new_board.cells[move.end[0]][move.end[1]].piece.role == 'K':
                if last_player_color == 'W':
                    new_board.in_check = 'B'
                else:
                    new_board.in_check = 'W'
                break
            else:
                new_board.in_check = ''

        if new_board.in_check != '':
            break

    return new_board


# Update board coverage maps
def update_coverage(board):
    new_board = board
    cells = board.cells
    black_moves = []
    white_moves = []

    points = {
        'P': 1,
        'K': 1,
        'R': 2,
        'B': 3,
        'N': 3,
        'Q': 4
    }

    # Reset previous coverage maps
    for x in range(0, 8):
        for y in range(0, 8):
            new_board.coverage_total[x][y] = 0
            new_board.coverage_black[x][y] = 0
            new_board.coverage_total[x][y] = 0

    # Determine all possible moves this piece can perform based on the board layout
    for x in range(0, 8):
        for y in range(0, 8):
            if cells[x][y].piece is not None:
                if cells[x][y].piece.color == 'B':
                    black_moves += remove_check_moves(board, get_cover_moves(board, x, y), 'B')
                else:
                    white_moves += remove_check_moves(board, get_cover_moves(board, x, y), 'W')

    # Calculate coverage scores for each cell based on moves that end at that cell
    for x in range(0, 8):
        for y in range(0, 8):
            data = ['', 0]

            # Add black moves that cover this cell
            for move in black_moves:
                if move.end == [x, y]:
                    if data[1] == 0:
                        data[0] = 'B'
                        data[1] += 1
                    elif data[0] == 'W':
                        data[1] -= 1
                    elif data[0] == 'B':
                        data[1] += 1
                    else:
                        print('ERROR')

                    if data[1] == 0:
                        data[0] = ''

                    new_board.coverage_black[x][y] += 1

            # Add white moves that cover this cell
            for move in white_moves:
                if move.end == [x, y]:
                    if data[1] == 0:
                        data[0] = 'W'
                        data[1] += 1
                    elif data[0] == 'B':
                        data[1] -= 1
                    elif data[0] == 'W':
                        data[1] += 1
                    else:
                        print('ERROR')

                    if data[1] == 0:
                        data[0] = ''

                    new_board.coverage_white[x][y] += 1
             
            new_board.coverage_total[x][y] = data

    # Get total coverage scores
    new_board.coverage_score_white = 0
    new_board.coverage_score_black = 0

    for x in range(0, 8):
        for y in range(0, 8):
            if board.coverage_total[x][y][0] == 'W':
                new_board.coverage_score_white += board.coverage_total[x][y][1]
            elif board.coverage_total[x][y][0] == 'B':
                new_board.coverage_score_black += board.coverage_total[x][y][1]

    # Get total piece scores
    new_board.piece_score_white = 0
    new_board.piece_score_black = 0

    for x in range(0, 8):
        for y in range(0, 8):
            if new_board.cells[x][y].piece is not None:
                if new_board.cells[x][y].piece.color == 'W':
                    new_board.piece_score_white += points[new_board.cells[x][y].piece.role]
                elif new_board.cells[x][y].piece.color == 'B':
                    new_board.piece_score_black += points[new_board.cells[x][y].piece.role]

    return new_board


# Perform a move on the board
def perform_move(color, board, move):
    start = move.start
    end = move.end
    special = move.special

    new_board = board

    piece = new_board.cells[start[0]][start[1]].piece 
    piece.moves += 1

    # If the move captures a piece, remove it from the opponent list
    if new_board.cells[end[0]][end[1]].piece is not None and new_board.cells[end[0]][end[1]].piece.color != color:
        try:
            if color == 'B':
                new_board.white_pieces.remove(end)
            elif color == 'W':
                new_board.black_pieces.remove(end)
        except ValueError:
            print(color + " " + str(end))

    # Update the move component in the player list
    if color == 'W':
        new_board.white_pieces[new_board.white_pieces.index(start)] = end
    elif color == 'B':
        new_board.black_pieces[new_board.black_pieces.index(start)] = end

    # Perform the move by updating the board cells
    new_board.cells[start[0]][start[1]].piece = None
    new_board.cells[end[0]][end[1]].piece = piece

    # In the event that a pawn reaches the opponent's side of the board, swap with a queen
    if piece.role == 'P':
        if piece.color == 'W':
            if end[0] == 7:
                new_board.cells[end[0]][end[1]].piece = models.Piece('W', 'Q', end[0], end[1], 'pieces/white_queen.png')
        else:
            if end[0] == 0:
                new_board.cells[end[0]][end[1]].piece = models.Piece('B', 'Q', end[0], end[1], 'pieces/black_queen.png')

    if special is not None:
        new_board = perform_move(color, new_board, special)

    return new_board


# Write board data to a dataframe
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


# Play a single game through to completion
def play_game(data_file, time_file, game, timeout):
    white = models.Player('W')
    black = models.Player('B')
    board = setup_board()
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
        3: 'defensive_pieces',
        4: 'random'
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
        black.style = playstyles[random.randrange(0, 5)]

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


        ###########################################
        ## CYCLE TURN
        ###########################################
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


# Run a series of games
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
    
    for i in range(start, end):
        print('Playing game ' + str(i))
        winner, turns = play_game('raw_data/game_' + str(root_start+i) + '.csv', 'raw_data/timing/game_' + str(root_start+i) + '_timing.csv', i, 500)
