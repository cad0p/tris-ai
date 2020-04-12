import secrets                              # imports secure module.
from copy import deepcopy
from random import random


def didRobotWin(game: list) -> int:
	"""

	:param game:
	:return: returns -1 if robot lost, 0 if deuse, 1 if robot won
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


class Robot:
	def __init__(self):
		self.weights = [random() for i in range(10)]
		self.history: list = []


def startGame(dim=3, robot=None, history=None) -> list:

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

	while winner == 0 and len(empty) > 0:
		winner = newRound(board, empty, robot, thisHistory)
	# history = stats(history, board, empty, robot, winner)

	print("The winner is player", winner, '!') if winner != 0 else print("It's a draw! I suggest playing again..")
	print("History:")
	printHistory(history, fromSlice=-1) # only get the last result
	print(didRobotWin(thisHistory))

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


def newRound(board, empty, robot, history=None) -> int:
	if history is None:
		history = []

	while True:
		print("Player 1")
		try:
			row = int(input("Row:"))
			col = int(input("Col:"))
		except ValueError:
			print("Value not valid! Insert a number between 1 and 3 for row and col!")
			continue

		row -= 1
		col -= 1
		thisMove = (row, col)
		# error
		if empty.count(thisMove) == 0:
			if 0 <= thisMove[0] < 3 and 0 <= thisMove[1] < 3:
				print("Cell already occupied!")
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
		thisMove = secrets.choice(empty)
		row, col = thisMove
		# error
		if empty.count(thisMove) == 0:
			print("Cell already occupied!")
		# correct
		else:
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

trisRobot = Robot()

print("Hi! This is tris.")
print("You can call me anywhere by calling startGame()")
print("You can customize some settings that way!")
gameHistory = startGame(robot=trisRobot)
while input("Do you want to play again? y/n \n") == 'y':
	startGame(history=gameHistory, robot=trisRobot)
