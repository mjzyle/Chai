import controller
import random
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
				best_score = 0.0

				weight_coverage = 5
				weight_pieces = 5
				weight_king_self = 5
				weight_king_opp = 5
				#weight_opp_response = 5

				bias_coverage = 5
				bias_pieces = 5
				bias_king_self = 5
				bias_king_opp = 5
				#bias_opp_response = 5

				for move in legal_moves:
					temp_board = deepcopy(new_board)
					temp_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, temp_board, move), self.color))

					# Determine coverage value
					if self.color == 'W':
						value_coverage = controller.sigmoid(temp_board.coverage_score_white - temp_board.coverage_score_black)
					elif self.color == 'B':
						value_coverage = controller.sigmoid(temp_board.coverage_score_black - temp_board.coverage_score_white)

					# Determine pieces value
					if self.color == 'W':
						value_pieces = controller.sigmoid(temp_board.piece_score_white - temp_board.piece_score_black)
					elif self.color == 'B':
						value_pieces = controller.sigmoid(temp_board.piece_score_black - temp_board.piece_score_white)

					# Determine player king value
					if self.color == 'W':
						king_loc = []
						king_cover = 0

						for loc in temp_board.white_pieces:
							if temp_board.cells[loc[0]][loc[1]].piece.role == 'K':
								king_loc = loc
								break

						for x in range(king_loc[0]-1, king_loc[0]+2):
							for y in range(king_loc[1]-1, king_loc[1]+2):
								if x > -1 and x < 8 and y > -1 and y < 8:
									cover = temp_board.coverage_total[x][y]
									if cover[0] == 'W':
										king_cover += cover[1]
					
					elif self.color == 'B':
						king_loc = []
						king_cover = 0

						for loc in temp_board.black_pieces:
							if temp_board.cells[loc[0]][loc[1]].piece.role == 'K':
								king_loc = loc
								break

						for x in range(king_loc[0]-1, king_loc[0]+2):
							for y in range(king_loc[1]-1, king_loc[1]+2):
								if x > -1 and x < 8 and y > -1 and y < 8:
									cover = temp_board.coverage_total[x][y]
									if cover[0] == 'B':
										king_cover += cover[1]

					value_king_self = controller.sigmoid(king_cover)

					# Determine opponent king value
					if self.color == 'W':
						opp_loc = []
						opp_cover = 0

						for loc in temp_board.black_pieces:
							if temp_board.cells[loc[0]][loc[1]].piece.role == 'K':
								opp_loc = loc
								break

						for x in range(opp_loc[0]-1, opp_loc[0]+2):
							for y in range(opp_loc[1]-1, opp_loc[1]+2):
								if x > -1 and x < 8 and y > -1 and y < 8:
									cover = temp_board.coverage_total[x][y]
									if cover[0] == 'B':
										opp_cover += cover[1]
					
					elif self.color == 'B':
						opp_loc = []
						opp_cover = 0

						for loc in temp_board.white_pieces:
							if temp_board.cells[loc[0]][loc[1]].piece.role == 'K':
								opp_loc = loc
								break

						for x in range(opp_loc[0]-1, opp_loc[0]+2):
							for y in range(opp_loc[1]-1, opp_loc[1]+2):
								if x > -1 and x < 8 and y > -1 and y < 8:
									cover = temp_board.coverage_total[x][y]
									if cover[0] == 'W':
										opp_cover += cover[1]

					value_king_opp = controller.sigmoid(opp_cover)

					# Determine opponent response value
					# TO DO

					# Apply weights and biases
					eff_score = (weight_coverage * value_coverage + bias_coverage) + (weight_pieces * value_pieces + bias_pieces) + (weight_king_self * value_king_self + bias_king_self) + (weight_king_opp * value_king_opp + bias_king_opp)
				
					if eff_score > best_score:
						best_score = eff_score
						best_move = move

				# Perform the best move
				new_board = controller.update_coverage(controller.determine_check(controller.perform_move(self.color, new_board, best_move), self.color))
				new_board.last_move_eff = best_score

			return False, False, new_board

		else:
			return True, False, new_board