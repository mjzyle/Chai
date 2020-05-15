import controller
import models
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.graphics.svg import Svg

b = controller.setup_board()
print(b)

b = controller.perform_move(b, models.Move(1, 3, 3, 3))
print(b)

class ChessWidget(Widget):
	board_size = 80
	board_start = 25
	board_end = 25

	def draw_board(self):
		with self.canvas:
			for i in range(0, 8):
				for j in range(0, 8):
					if (i + j) % 2 == 0:
						Color(0, 0, 0)
					else:
						Color(1, 1, 1)

					Rectangle(pos=(self.board_start + i*self.board_size, self.board_start + j*self.board_size), size=(self.board_size, self.board_size))
					#Svg(pos=(self.board_start + i*self.board_size, self.board_start + j*self.board_size), size=(self.board_size, self.board_size), source=('pieces/black_queen.svg'))


class ChessApp(App):
	def build(self):
		c = ChessWidget()
		c.draw_board()
		return c


ChessApp().run()