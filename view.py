import controller
import models
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from functools import partial

Window.size = (1200, 800)

class ChessWidget(Widget):
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


class ChessApp(App):
	def build(self):
		c = ChessWidget()
		c.setup()
		return c


ChessApp().run()