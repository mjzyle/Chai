class Cell:
    def __init__(self):
        self.piece = None

    def __str__(self):
        if self.piece is None:
            return '--'
        else:
            return str(self.piece)


class Board:
    def __init__(self):
        self.cells = []

        for x in range(0, 8):
            row = []
        
            for y in range(0, 8):
                row.append(Cell())

            self.cells.append(row)

    def __str__(self):
        temp = ''

        for x in range(0, 8):
            for y in range(0, 8):
                temp += str(self.cells[x][y]) + ' '
            temp += '\n'

        return temp
            

class Piece: 
    def __init__(self, color, role, x, y):
        self.color = color
        self.role = role
        self.x = x
        self.y = y
        self.made_first_move = False

    def __str__(self):
        return self.color + self.role

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.made_first_move = True


class Move:
    def __init__(self, from_x, from_y, to_x, to_y, special=None):
        self.start = [from_x, from_y]
        self.end = [to_x, to_y]
        self.special = special

    def __str__(self):
        return 'From ' + str(self.start[0]) + ',' + str(self.start[1]) + ' to ' + str(self.end[0]) + ',' + str(self.end[1])