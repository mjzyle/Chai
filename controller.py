import models


def setup_board():
    board = models.Board()
    temp = board.cells

    # Setup black pieces
    temp[0][0].piece = models.Piece('B', 'R', 0, 0)
    temp[0][1].piece = models.Piece('B', 'N', 0, 1)
    temp[0][2].piece = models.Piece('B', 'B', 0, 2)
    temp[0][3].piece = models.Piece('B', 'Q', 0, 3)
    temp[0][4].piece = models.Piece('B', 'K', 0, 4)
    temp[0][5].piece = models.Piece('B', 'B', 0, 5)
    temp[0][6].piece = models.Piece('B', 'N', 0, 6)
    temp[0][7].piece = models.Piece('B', 'R', 0, 7)

    for i in range(0, 8):
        temp[1][i].piece = models.Piece('B', 'P', 1, i)

    # Setup white pieces
    temp[7][0].piece = models.Piece('W', 'R', 7, 0)
    temp[7][1].piece = models.Piece('W', 'N', 7, 1)
    temp[7][2].piece = models.Piece('W', 'B', 7, 2)
    temp[7][3].piece = models.Piece('W', 'Q', 7, 3)
    temp[7][4].piece = models.Piece('W', 'K', 7, 4)
    temp[7][5].piece = models.Piece('W', 'B', 7, 5)
    temp[7][6].piece = models.Piece('W', 'N', 7, 6)
    temp[7][7].piece = models.Piece('W', 'R', 7, 7)

    for i in range(0, 8):
        temp[6][i].piece = models.Piece('W', 'P', 6, i)

    board.cells = temp
    return board


def get_legal_moves(board, x, y):
    piece = board.cells[x][y].piece
    legal_moves = []


    # PAWN MOVEMENT RULES
    if piece.role == 'P':
        # Determine the pawn's directionality based on its color (white is descending index, black is ascending index)
        desc = False
        if piece.color == 'W':
            desc = True

        if desc:
            # Determine if the pawn can move one space
            if board.cells[x-1][y].piece is None:
                legal_moves.append(models.Move(x, y, x-1, y))
            
            # Determine if the pawn has made a first move; if not, it can move either one or two spaces
            if not piece.made_first_move and board.cells[x-1][y].piece is None and board.cells[x-2][y].piece is None:
                legal_moves.append(models.Move(x, y, x-2, y))

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
            if board.cells[x+1][y].piece is None:
                legal_moves.append(models.Move(x, y, x+1, y))
            
            # Determine if the pawn has made a first move; if not, it can move either one or two spaces
            if not piece.made_first_move and board.cells[x+1][y].piece is None and board.cells[x+2][y].piece is None:
                legal_moves.append(models.Move(x, y, x+2, y))

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

        for i in range(x-1, -1):
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

        for i in range(y-1, -1):
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
        i = x
        j = y
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x
        j = y
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x
        j = y
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x
        j = y
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j += 1

    # QUEEN MOVEMENT RULES
    elif piece.role == 'Q':
        # Check +/+ axis
        i = x
        j = y
        while i < 8 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j += 1

        # Check -/- axis
        i = x
        j = y
        while i > -1 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i -= 1
            j -= 1

        # Check +/- axis
        i = x
        j = y
        while i < 8 and j > -1:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
                break
            i += 1
            j -= 1

        # Check -/+ axis
        i = x
        j = y
        while i > -1 and j < 8:
            if board.cells[i][j].piece is None:
                legal_moves.append(models.Move(x, y, i, j))
            elif board.cells[i][j].piece.color is not piece.color:
                legal_moves.append(models.Move(x, y, i, j))
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

        for i in range(x-1, -1):
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

        for i in range(y-1, -1):
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
        if not piece.made_first_move:

            # Left rook hasn't yet moved
            if board.cells[x][0].piece is not None and not board.cells[x][0].piece.made_first_move and board.cells[x][1].piece is None and board.cells[x][2].piece is None and board.cells[x][3].piece is None:
                legal_moves.append(models.Move(x, y, x, y-2, models.Move(x, 0, x, y-1)))

            # Right rook hasn't yet moved
            if board.cells[x][0].piece is not None and not board.cells[x][7].piece.made_first_move and board.cells[x][6].piece is None and board.cells[x][5].piece is None:
                legal_moves.append(models.Move(x, y, x, y+2, models.Move(x, 7, x, y+1)))


    # Remove any moves with negative array indices
    i = 0
    while i < len(legal_moves):
        move = legal_moves[i].end

        if move[0] < 0 or move[1] < 0:
            legal_moves.pop(i)
        else:
            i += 1

    # Remove any king moves that would place the king in check
    if piece.role == 'K':
        m = 0
        while m < len(legal_moves):
            opponent_moves = []
            move = legal_moves[m]
            temp_board = perform_move(board, move)

            # Determine all possible moves that the opponent could make in the event that the king makes this move
            for i in range(0, 8):
                for j in range(0, 8):
                    if temp_board.cells[i][j].piece is not None and temp_board.cells[i][j].piece.color is not piece.color:
                        opponent_moves += get_legal_moves(temp_board, i, j)

            # If the opponent can make a legal move that would match the new location of the king, then the king's current move is illegal (remove it)
            for opp_move in opponent_moves:
                if opp_move.end == move.end:
                    legal_moves.pop(m)
                    m -= 1
                    break

            m += 1

    return legal_moves


def perform_move(board, move):
    start = move.start
    end = move.end
    special = move.special
    new_board = board

    piece = new_board.cells[start[0]][start[1]].piece
    new_board.cells[start[0]][start[1]].piece = None
    new_board.cells[end[0]][end[1]].piece = piece

    if special is not None:
        new_board = perform_move(new_board, special)

    return new_board