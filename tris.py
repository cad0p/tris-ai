import secrets                              # imports secure module.


def startGame(dim=3, robot=True, history=None) -> list:
	if history is None:
		history = []
	thisHistory = []
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
		winner, thisHistory = newRound(board, empty, robot, thisHistory)
	# history = stats(history, board, empty, robot, winner)
	history.append(thisHistory)
	print("The winner is player", winner, '!') if winner != 0 else print("It's a draw! I suggest playing again..")
	print("History:")
	printHistory(history, fromSlice=-1) # only get the last result

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


def newRound(board, empty, robot, history=None) -> (int, list):
	if history is None:
		history = []

	while True:
		print("Player 1")
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
			board[row][col] = 1
			emptySlots(empty, thisMove)
			printBoard(board)
			break

	if win(board, 1):
		history.append(board)
		return 1, history
	elif len(empty) == 0:
		history.append(board)
		return 0, history

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
		history.append(board)
		return 2, history
	else:
		history.append(board)
		return 0, history


def emptySlots(empty, thisMove: (int, int)):
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


print("Hi! This is tris.")
print("You can call me anywhere by calling startGame()")
print("You can customize some settings that way!")
gameHistory = startGame()
while input("Do you want to play again? y/n \n") == 'y':
	startGame(history=gameHistory)
