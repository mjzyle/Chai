import controller
import random
import neural_network
import tensorflow as tf
import numpy as np
from copy import deepcopy


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
		self.coverage_total = []
		self.coverage_black = []
		self.coverage_white = []
		self.board_size = 80
		self.board_start = 25
		self.in_check = ''
		self.coverage_score_white = 0
		self.coverage_score_black = 0
		self.piece_score_white = 0
		self.piece_score_black = 0
		self.white_pieces = []
		self.black_pieces = []
		self.last_move_eff = 0

		# Setup cells
		for x in range(0, 8):
			row = []
		
			for y in range(0, 8):
				row.append(Cell())

			self.cells.append(row)

		# Setup coverage maps
		for x in range(0, 8):
			row_total = []
			row_single = []

			for y in range(0, 8):
				row_total.append(['', 0])
				row_single.append(0)

			self.coverage_total.append(row_total)
			self.coverage_black.append(row_single)
			self.coverage_white.append(row_single)


	def __str__(self):
		temp = ''

		for y in range(0, 8):
			for x in range(0, 8):
				temp += str(self.cells[x][y]) + ' '
			temp += '\n'

		return temp
			

class Piece: 
	def __init__(self, color, role, x, y, image):
		self.color = color
		self.role = role
		self.x = x
		self.y = y
		self.moves = 0
		self.image = image

	def __str__(self):
		return self.color + self.role

	def update_position(self, x, y):
		self.x = x
		self.y = y
		self.moves += 1


class Move:
	def __init__(self, from_x, from_y, to_x, to_y, special=None):
		self.start = [from_x, from_y]
		self.end = [to_x, to_y]
		self.special = special

	def __str__(self):
		return 'From ' + str(self.start[0]) + ',' + str(self.start[1]) + ' to ' + str(self.end[0]) + ',' + str(self.end[1]) + ' with special ' + str(self.special)


class Player:
	def __init__(self, color, style='random'):
		self.color = color
		self.style = style
		self.model = neural_network.get_model()

	def make_move(self, board):
		new_board = deepcopy(board)

		# Determine all legal moves
		legal_moves = []
		if self.color == 'W':
			pieces = board.white_pieces
		elif self.color == 'B':
			pieces = board.black_pieces

		for piece in pieces:
			if board.cells[piece[0]][piece[1]].piece is not None and board.cells[piece[0]][piece[1]].piece.color == self.color:
					legal_moves += controller.remove_check_moves(board, controller.get_legal_moves(board, piece[0], piece[1]), self.color)

		# Make move based on player style
		if len(legal_moves) > 0:

			# Choose a random legal move
			if self.style == 'random':
				index = random.randrange(0, len(legal_moves))
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, legal_moves[index]), self.color))
			
			# Attempt to create the largest delta between player coverage scores
			elif self.style == 'offensive_coverage':
				best_move = None
				best_cover_delta = -500

				for move in legal_moves:
					
					# Perform the move on a temporary board
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))
					
					# Calculate delta scores
					if self.color == 'W':
						cover_delta = temp_board.coverage_score_white - temp_board.coverage_score_black
					else:
						cover_delta = temp_board.coverage_score_black - temp_board.coverage_score_white

					if cover_delta > best_cover_delta:
						best_move = move
						best_cover_delta = cover_delta

				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
			
			# Attempt to create the largest delta between player piece scores
			elif self.style == 'offensive_pieces':
				best_move = None
				best_piece_delta = -500

				for move in legal_moves:
					
					# Perform the move on a temporary board
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))
					
					# Calculate delta scores
					if self.color == 'W':
						piece_delta = temp_board.piece_score_white - temp_board.piece_score_black
					else:
						piece_delta = temp_board.piece_score_black - temp_board.piece_score_white

					if piece_delta > best_piece_delta:
						best_move = move
						best_piece_delta = piece_delta

				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
			
			# Attempt to create the smallest delta between player coverage scores
			elif self.style == 'defensive_coverage':
				best_move = None
				best_cover_delta = 500

				for move in legal_moves:
					
					# Perform the move on a temporary board
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))
					
					# Calculate delta scores
					if self.color == 'W':
						cover_delta = temp_board.coverage_score_white - temp_board.coverage_score_black
					else:
						cover_delta = temp_board.coverage_score_black - temp_board.coverage_score_white

					if cover_delta < best_cover_delta:
						best_move = move
						best_cover_delta = cover_delta

				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
			
			# Attempt to create the smallest delta between player piece scores
			elif self.style == 'defensive_pieces':
				best_move = None
				best_piece_delta = 500

				for move in legal_moves:
					
					# Perform the move on a temporary board
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))
					
					# Calculate delta scores
					if self.color == 'W':
						piece_delta = temp_board.piece_score_white - temp_board.piece_score_black
					else:
						piece_delta = temp_board.piece_score_black - temp_board.piece_score_white

					if piece_delta < best_piece_delta:
						best_move = move
						best_piece_delta = piece_delta

				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
			
			####################################################
			# Neural network playmodel
			####################################################
			elif self.style == 'neural_network':
				best_move = None
				best_score = -1

				# Evaluate each possible move
				for move in legal_moves:
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))
					data = {}	
					cover = ''
					brd = ''
					points = {
						'P': 1,
						'R': 2,
						'B': 3,
						'N': 3,
						'Q': 4,
						'K': 9
					}
					
					# Encode board
					for x in range(0, 8):
						for y in range(0, 8):
							if temp_board.cells[x][y].piece is not None:
								brd += str(temp_board.cells[x][y].piece)
							else:
								brd += '--'

					# Encode coverage
					for x in range(0, 8):
						for y in range(0, 8):
							cover += ('-' if temp_board.coverage_total[x][y][0] == '' else temp_board.coverage_total[x][y][0]) + str(temp_board.coverage_total[x][y][1])
            
					# Translate data into model-acceptable form
					if self.color == 'W':
						i = 0
						while i < 128:
							if cover[i] == 'W':
								data['cover' + str(i)] = int(cover[i+1])
							elif cover[i] == 'B':
								data['cover' + str(i)] = int(cover[i+1]) * -1
							else:
								data['cover' + str(i)] = 0

							if brd[i] == 'W':
								data['pieces' + str(i)] = int(points[brd[i+1]])
							elif brd[i] == 'B':
								data['pieces' + str(i)] = int(points[brd[i+1]]) * -1
							else:
								data['pieces' + str(i)] = 0

							i += 2

					elif self.color == 'B':
						i = 126
						while i > -1:
							if cover[i] == 'B':
								data['cover' + str(i)] = int(cover[i+1])
							elif cover[i] == 'W':
								data['cover' + str(i)] = int(cover[i+1]) * -1
							else:
								data['cover' + str(i)] = 0

							if brd[i] == 'B':
								data['pieces' + str(i)] = int(points[brd[i+1]])
							elif brd[i] == 'W':
								data['pieces' + str(i)] = int(points[brd[i+1]]) * -1
							else:
								data['pieces' + str(i)] = 0

							i -= 2

					# Predict likelihood of winning with this move
					arr = np.array([list(data.values())])
					predict = float(self.model.predict(arr))
					
					if predict > best_score:
						best_score = predict
						best_move = move


				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
				new_board.last_move_eff = best_score

			return False, False, new_board

		else:
			return True, False, new_board