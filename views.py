import gameplay_controller as controller
import gameplay_models as models
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from functools import partial
import pandas as pd
import math
from kivy.uix.label import Label


Window.size = (1200, 800)


class PlayWidget(Widget):
    b = controller.setup_board()
    images = []
    coverage_total = []
    coverage_black = []
    coverage_white = []
    current_move = None

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Rectangle(size=(self.width, self.height))

            # Draw tiles
            for y in range(0, 8):
                for x in range(0, 8):
                    b = Button(
                        pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                        size=(self.b.board_size, self.b.board_size),
                        background_color=(60/255, 33/255, 6/255, 0.6) if (x + y) % 2 == 0 else (238/255, 166/255, 93/255, 0.6)
                    )
                    b.bind(on_press=partial(self.callback, x, y))
                    self.add_widget(b)

            # Draw pieces
            for x in range(0, 8):
                for y in range(0, 8):
                    if self.b.cells[x][y].piece is not None:
                        Color(1, 1, 1, 1)
                        self.images[y][x] = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=self.b.cells[x][y].piece.image
                        )
                    else:
                        Color(0, 0, 0, 0)
                        self.images[y][x] = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=''
                        )

            # Draw coverage maps
            for x in range(0, 8):
                for y in range(0, 8):
                    # Draw total map
                    if self.b.coverage_total[x][y][0] == 'B':
                        Color(0.1*self.b.coverage_black[x][y], 0, 0, 0.8)
                        self.coverage_black[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 450)
                        )
                    elif self.b.coverage_total[x][y][0] == 'W':
                        Color(0, 0.1*self.b.coverage_white[x][y], 0, 0.8)
                        self.coverage_white[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 450)
                        )

                    # Draw black map (red)
                    if self.b.coverage_total[x][y][0] == 'B':
                        Color(0.1*self.b.coverage_total[x][y][1], 0, 0, 0.8)
                        self.coverage_black[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 225)
                        )

                    # Draw white map (green)
                    if self.b.coverage_total[x][y][0] == 'W':
                        Color(0, 0.1*self.b.coverage_total[x][y][1], 0, 0.8)
                        self.coverage_white[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x)
                        )


    def callback(self, x, y, event):
        # If no move is in progress, the player has selected this piece to move; display allowable moves
        if self.current_move is None: 

            # If player has selected a valid piece, start the move
            self.current_move = models.Move(x, y, -1, -1)
            print('Starting move from ' + str(x) + ',' + str(y))

            # If the piece is not valid, throw an error
            ## ADD HERE

        # A move determination is in progress
        else:
            # Player has selected another one of their own pieces; start a new move
            if self.b.cells[x][y].piece is None or self.b.cells[x][y].piece.color != self.b.cells[self.current_move.start[0]][self.current_move.start[1]].piece.color:
                self.current_move.end = [x, y]
                print('Attempting move to ' + str(x) + ',' + str(y))
                legal_moves = controller.get_legal_moves(self.b, self.current_move.start[0], self.current_move.start[1])
                legal_moves = controller.remove_check_moves(self.b, legal_moves, self.b.cells[self.current_move.start[0]][self.current_move.start[1]].piece.color)
                for move in legal_moves:
                    if self.current_move.end == move.end:
                        self.current_move.special = move.special
                        self.b = controller.perform_move(self.b, self.current_move)
                        print('Move allowed!')
                        
                        if self.b.in_check != '':
                            print('Player ' + self.b.in_check + ' is in check!')

                        break
                self.current_move = None

            # Player has selected an open or opponent-occupied space; process potential moves
            else:
                self.current_move.start = [x, y]
                print('Starting new move from ' + str(x) + ',' + str(y))

        self.draw()


    def setup(self):
        # Setup board tiles
        with self.canvas:
            for y in range(0, 8):
                for x in range(0, 8):
                    b = Button(
                        pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                        size=(self.b.board_size, self.b.board_size),
                        background_color=(60/255, 33/255, 6/255, 0.6) if (x + y) % 2 == 0 else (238/255, 166/255, 93/255, 0.6)
                    )
                    b.bind(on_press=partial(self.callback, x, y))
                    self.add_widget(b)

        # Setup image tiles to display pieces on each square
        with self.canvas:
            for y in range(0, 8):
                temp = []
                for x in range(0, 8):
                    if self.b.cells[x][y].piece is not None:
                        Color(1, 1, 1, 1)
                        r = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=self.b.cells[x][y].piece.image
                        )
                    else:
                        Color(0, 0, 0, 0)
                        r = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=''
                        )
                    temp.append(r)
                self.images.append(temp)

        # Setup coverage map utilities
        with self.canvas:
            for y in range(0, 8):
                temp_black = []
                temp_white = []
                temp_total = []
                for x in range(0, 8):
                    Color(0, 0, 0, 0.8)
                    r_white = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x)
                    )
                    r_black = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x + 225)	
                    )
                    r_total = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x + 450)	
                    )
                    temp_black.append(r_black)
                    temp_white.append(r_white)
                    temp_total.append(r_total)
                self.coverage_black.append(temp_black)
                self.coverage_white.append(temp_white)
                self.coverage_total.append(temp_total)

        self.draw()


class PlayApp(App):
    def build(self):
        c = PlayWidget()
        c.setup()
        return c


class ReviewWidget(Widget):
    b = controller.setup_board()
    images = []
    image_files = {
        'WR': 'pieces/white_rook.png',
        'WN': 'pieces/white_knight.png',
        'WB': 'pieces/white_bishop.png',
        'WQ': 'pieces/white_queen.png',
        'WK': 'pieces/white_king.png',
        'WP': 'pieces/white_pawn.png',
        'BR': 'pieces/black_rook.png',
        'BN': 'pieces/black_knight.png',
        'BB': 'pieces/black_bishop.png',
        'BQ': 'pieces/black_queen.png',
        'BK': 'pieces/black_king.png',
        'BP': 'pieces/black_pawn.png',
        '--': ''
    }
    coverage_total = []
    coverage_black = []
    coverage_white = []
    current_board = 0
    check_prompt = ''
    data = pd.read_csv('raw_data/game_1.csv').drop(columns='Unnamed: 0')


    def __init__(self, **kwargs):
        super(ReviewWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_board = max(0, self.current_board-1)
            self.draw()
        elif keycode[1] == 'right':
            self.current_board = min(len(self.data)-1, self.current_board+1)
            self.draw()

        return True


    def draw(self):
        self.canvas.clear()

        # Change board data before drawing
        board_data = self.data.loc[self.current_board]
        for y in range(0, 8):
            for x in range(0, 8):
                key_start = 2*y + 16*x
                key_end = 2*y + 16*x + 2
                key = board_data['Ending Board'][key_start:key_end]
                
                if key != '--':
                    self.b.cells[x][y].piece = models.Piece(key[0], key[1], x, y, self.image_files[key])
                    if key[0] == 'W':
                        self.b.white_pieces.append([x, y])
                    elif key[0] == 'B':
                        self.b.black_pieces.append([x, y])
                else:
                    self.b.cells[x][y].piece = None

        # Update coverage with new board
        self.b = controller.update_coverage(self.b)
        self.b.in_check = board_data['In Check']

        # Update check indication tooltip
        if self.b.in_check == 'B':
            self.check_prompt = 'Black is in check'
        elif self.b.in_check == 'W':
            self.check_prompt = 'White is in check' 
        else:
            self.check_prompt = ''

        # RENDER
        with self.canvas:
            # Draw board tiles
            for y in range(0, 8):
                for x in range(0, 8):
                    if (x + y) % 2 == 0:
                        Color(60/255, 33/255, 6/255, 0.6)
                    else:
                        Color(238/255, 166/255, 93/255, 0.6)
                    
                    r = Rectangle(
                        pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                        size=(self.b.board_size, self.b.board_size)
                    )

            # Draw pieces
            for x in range(0, 8):
                for y in range(0, 8):
                    if self.b.cells[x][y].piece is not None:
                        Color(1, 1, 1, 1)
                        self.images[y][x] = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=self.b.cells[x][y].piece.image
                        )
                    else:
                        Color(0, 0, 0, 0)
                        self.images[y][x] = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=''
                        )

            # Draw coverage maps
            for x in range(0, 8):
                for y in range(0, 8):
                    # Draw total map
                    if self.b.coverage_total[x][y][0] == 'B':
                        Color(0.1*self.b.coverage_black[x][y], 0, 0, 0.8)
                        self.coverage_black[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 450)
                        )
                    elif self.b.coverage_total[x][y][0] == 'W':
                        Color(0, 0.1*self.b.coverage_white[x][y], 0, 0.8)
                        self.coverage_white[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 450)
                        )

                    # Draw black map (red)
                    if self.b.coverage_total[x][y][0] == 'B':
                        Color(0.1*self.b.coverage_total[x][y][1], 0, 0, 0.8)
                        self.coverage_black[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x + 225)
                        )

                    # Draw white map (green)
                    if self.b.coverage_total[x][y][0] == 'W':
                        Color(0, 0.1*self.b.coverage_total[x][y][1], 0, 0.8)
                        self.coverage_white[x][y] = Rectangle(
                            size=(25, 25),
                            pos=(700+25*y, self.b.board_start + 25*x)
                        )

            # Draw tooltip
            l = Label(
                text=str(self.current_board+1),
                pos=(100, 700)
            )
            l = Label(
                text=self.check_prompt,
                pos=(200, 700)
            )


    def setup(self):
        # Setup image tiles to display pieces on each square
        with self.canvas:
            for y in range(0, 8):
                temp = []
                for x in range(0, 8):
                    if self.b.cells[x][y].piece is not None:
                        Color(1, 1, 1, 1)
                        r = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=self.b.cells[x][y].piece.image
                        )
                    else:
                        Color(0, 0, 0, 0)
                        r = Rectangle(
                            pos=(self.b.board_start + y*self.b.board_size, self.b.board_start + x*self.b.board_size),
                            size=(self.b.board_size, self.b.board_size),
                            source=''
                        )
                    temp.append(r)
                self.images.append(temp)

        # Setup coverage map utilities
        with self.canvas:
            for y in range(0, 8):
                temp_black = []
                temp_white = []
                temp_total = []
                for x in range(0, 8):
                    Color(0, 0, 0, 0.8)
                    r_white = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x)
                    )
                    r_black = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x + 225)	
                    )
                    r_total = Rectangle(
                        size=(25, 25),
                        pos=(700+25*y, self.b.board_start + 25*x + 450)	
                    )
                    temp_black.append(r_black)
                    temp_white.append(r_white)
                    temp_total.append(r_total)
                self.coverage_black.append(temp_black)
                self.coverage_white.append(temp_white)
                self.coverage_total.append(temp_total)

        self.draw()


class ReviewApp(App):
    def build(self):
        c = ReviewWidget()
        c.setup()
        return c


def play():
    PlayApp().run()


def review():
    ReviewApp().run()