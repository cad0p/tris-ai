# import secrets                              # imports secure module.
from copy import deepcopy
from time import sleep
from typing import Union

from numpy.random import rand
from numpy import asarray, matmul, unravel_index, argmax, float64, divide, ndarray, array


def didRobotWin(game: list) -> int:
	"""

	:param game:
	:return: returns -1 if robot lost, 0 if deuce, 1 if robot won
		(in the case that the game is not finished yet, it's going to return 1)
	"""
	if len(game) == 5:
		if not win(game[-1], 1):
			return 0
		else:
			return -1
	else:
		if not win(game[-1], 1):
			return 1
		else:
			return -1


def convertBoardForRobot(board: list) -> ndarray:
	convertedBoard = deepcopy(board)
	for row in range(len(board)):
		for col in range(len(board[0])):
			if convertedBoard[row][col] == '':
				convertedBoard[row][col] = -1
	return asarray(convertedBoard)


def getPlayerMovesFromGame(player: int, game: list) -> list:
	"""

	:param player: the player
	:param game: the game you want to analyze player moves
	:return: [(1,2),(2,2),(3,2)] for example
	"""
	playerMoves = []
	for board in game:
		for row in range(len(board)):
			for col in range(len(board)):
				if (theMove := (row, col)) not in playerMoves and board[row][col] == player:
					playerMoves.append(theMove)
	return playerMoves


class Robot:
	dim: int
	weights: ndarray
	history: list
	board: Union[list, ndarray]
	choice: tuple  # (2, 1) [ or (3, 2) with natural notation]
	player: int  # represents the number of the player in the game.

	def __init__(self, dim: int = 3, weights: ndarray = None, player: int = 2):
		self.dim = dim
		self.weights = rand(dim, dim) if weights is None else weights
		print(self.weights)
		self.history: list = []
		self.player = player

	def nextMove(self, board):
		self.board = convertBoardForRobot(board)

		result = matmul(self.weights, self.board)
		print(result)
		# this is because it is actually an array
		# (in case you do it against an axis)
		theMove = unravel_index(argmax(result), result.shape)
		self.choice = theMove
		print((theMove[0] + 1, theMove[1] + 1))
		return self.choice

	def good(self):
		return

	def bad(self):
		"""
		Adjusts the weights to try again and have better luck!

		:return: nothing
		"""
		# result = matmul(self.weights, self.board)
		correction = rand(self.dim, self.dim)
		correction -= 0.5
		divide(correction, 100)
		self.weights += correction
		# newResult = matmul(self.weights, self.board)
		# tryNewChoice = unravel_index(argmax(newResult), result.shape)
		# tryCount = 1
		# while self.choice == tryNewChoice:
		# 	# we are trying to lower the value of the maximum element
		# 	# in the result matrix.
		# 	print("trying again.. ", tryCount)
		# 	change = divide(newResult - result, correction)
		# 	# this is the step-derivative
		# 	tryNewChoice = argmax(result)[0]
		# 	tryCount += 1
		return

	def badGame(self):
		game = self.history[-1]
		while didRobotWin(game) != 1:
			self.bad()
			player1moves = getPlayerMovesFromGame(1, self.history[-1])
			game = startGame(robot=self, player1Moves=player1moves)[-1]


def startGame(dim=3, robot=None, history=None, player1Moves: list = None) -> list:
	"""

	:param dim: the dimension of the board
	:param robot: if a robot plays in place of the second player
	:param history: if there is a past history that you want to keep track of
	:param player1Moves: gets the list of moves from last to first
		(to easily pop the moves from first to last!)
		-- edit: now it pops from the beginning, without having to reverse the list
	:return: the updated history
	"""

	if history is None:
		history = []
	# save the history in the robot
	if robot:
		robot.history = history
	thisHistory = []
	history.append(thisHistory)  # [thisHistory] will be modified and history will keep its contents
	# dimension
	board = []
	empty = []
	winner = 0  # no one is winning
	for row in range(dim):
		board.append([])
		for col in range(dim):
			board[row].append('')
			empty.append((row, col))

	printBoard(board)

	print(player1Moves)

	while winner == 0 and len(empty) > 0:
		winner = newRound(board, empty, robot, thisHistory,
			player1Move=player1Moves.pop(0) if player1Moves is not None else None
		)
	# history = stats(history, board, empty, robot, winner)

	print("The winner is player", winner, '!') \
		if winner != 0 else print("It's a draw! I suggest playing again..")
	print("History:")
	printHistory(history, fromSlice=-1) # only get the last result
	print(didRobotWin(thisHistory))
	if player1Moves is None and didRobotWin(thisHistory) == -1:
		# # [if player1Moves is None] is to avoid recursion
		# sleep(2)
		# # this is to tell the robot he has lost the game
		# robot.badGame()
		pass

	return history


def printBoard(a: list):
	"""

	:param a: the board of the game, a 3x3 grid
	:return: the board in stdout
	"""
	for row in a:
		print(' '.join([str(elem) if elem != '' else '-' for elem in row]))


def printHistory(history: list, fromSlice: int = None, toSlice: int = None):
	"""

	:param history:
	:param fromSlice: the slicing of a python list
	:param toSlice: the slicing of a python list
	:return: nothing
	"""
	for gameIndex, game in enumerate(history[fromSlice:toSlice]):
		if fromSlice is not None:
			gameIndex += fromSlice if fromSlice >= 0 else len(history) + fromSlice
		print("Game", gameIndex, ":")
		for gameRoundIndex, gameRound in enumerate(game):
			print("Round", gameRoundIndex, ":")
			printBoard(gameRound)
		print("End Game", gameIndex)


def newRound(board, empty, robot, history=None, player1Move=None) -> int:
	if history is None:
		history = []

	while True:
		print("Player 1")
		row, col = (0, 0)
		if player1Move:
			print((player1Move[0] + 1, player1Move[1] + 1))
		if not player1Move:
			try:
				row = int(input("Row:"))
				col = int(input("Col:"))

				row -= 1
				col -= 1
			except ValueError:
				print("Value not valid! Insert a number between 1 and 3 for row and col!")
				continue

		thisMove = (row, col) if not player1Move else player1Move
		if player1Move:
			row, col = player1Move
		# error
		if empty.count(thisMove) == 0:
			if 0 <= thisMove[0] < 3 and 0 <= thisMove[1] < 3:
				print("Cell already occupied!")
				if player1Move:
					# player 1 has lost because he can't make that move!
					return -1
			else:
				print("Insert a number between 1 and 3 for row and col!")
		# correct
		else:
			board[row][col] = 1
			emptySlots(empty, thisMove)
			printBoard(board)
			break

	if win(board, 1):
		history.append(deepcopy(board))
		return 1
	elif len(empty) == 0:
		history.append(deepcopy(board))
		return 0

	while not robot:
		print("Player 2")
		row = int(input("Row:"))
		col = int(input("Col:"))
		row -= 1
		col -= 1
		thisMove = (row, col)
		# error
		if empty.count(thisMove) == 0:
			print("Cell already occupied!")
		# correct
		else:
			board[row][col] = 2
			emptySlots(empty, thisMove)
			printBoard(board)
			break
	while robot:
		print("Robot")
		# thisMove = secrets.choice(empty)
		thisMove = robot.nextMove(board)
		row, col = thisMove
		if empty.count(thisMove) == 0:
			# error
			print("Cell already occupied!")
			printBoard(board)
			robot.bad()
		else:
			# correct
			board[row][col] = 2
			emptySlots(empty, thisMove)
			printBoard(board)
			break

	if win(board, 2):
		history.append(deepcopy(board))
		return 2
	else:
		history.append(deepcopy(board))
		return 0


def emptySlots(empty, thisMove: (int, int)) -> None:
	empty.remove(thisMove)


def win(board, player) -> bool:
	dim = len(board)
	# print("board")
	# printBoard(board)
	# initialize diagonals
	diag1 = diag2 = True
	for i in range(dim):
		# columns, rows
		if ([row[i] for row in board].count(player) == 3 or
					board[i].count(player) == 3):
			return True
		diag1 = diag1 and (board[i][i] == player)
		diag2 = diag2 and (board[i][dim-1-i] == player)
	if diag1 or diag2:
		return True
	else:
		return False


# def stats(


# def chooseCell(board, empty, history

bestWeights = array(
		[
			[-453.81391636,  104.43291649,  -40.89840344],
			[ 127.50819116,  -25.10198367,  -31.08633784],
			[  85.63707048,  111.88746899, -225.64269217]
		]
)


# trisRobot = Robot(weights=bestWeights)
trisRobot = Robot()


print("Hi! This is tris.")
print("You can call me anywhere by calling startGame()")
print("You can customize some settings that way!")
gameHistory = startGame(robot=trisRobot)


def displayStats(history, robot=None):
	if robot:
		print(robot.weights)


while (userInput := input("Do you want to play again? y/n  (press 's' for stats) \n")
			) not in ['n', 'N']:
	if userInput in ['s', 'S']:
		displayStats(gameHistory, robot=trisRobot)
		continue
	startGame(history=gameHistory, robot=trisRobot)
