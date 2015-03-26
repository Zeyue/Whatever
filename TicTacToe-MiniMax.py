#A Tic Tac Toe Game using MiniMax Algorithme (limited depth) for the design of AI
#Author: Zeyue Liang
#Date: 2015-03-26
#Reference: 1. https://inventwithpython.com/chapter10.html
#			2. Course 'Introduction à l'intelligence artificielle' 
#			   in the Option OSY 2015 Centrale-Supélec 
#			   By M. Jean-Philippe Poli

import random

#Display the game board
def drawBoard(board):
	print('    |    |')
	print('  ' + board[7] + ' | ' + board[8] + '  | ' + board[9])
	print('    |    |')
	print('--------------')
	print('    |    |')
	print('  ' + board[4] + ' | ' + board[5] + '  | ' + board[6])
	print('    |    |')
	print('--------------')
	print('    |    |')
	print('  ' + board[1] + ' | ' + board[2] + '  | ' + board[3])
	print('    |    |')

#Let player choose his Letter. X or O in option
def inputPlayerLetter():
	letter = ''
	while not (letter == 'X' or letter == 'O'):
		print('Do you want to be X or O?')
		letter = input().upper()

	if letter == 'X':
		return ['X', 'O']
	else:
		return ['O', 'X']

#Determine who goes first randomly
def whoGoesFirst():
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

#Ask player to play again
def playAgain():
	print('Do you want to play again? (yes or no)')
	return input().lower().startswith('y')

#Make a move on the game board
def makeMove(board, letter, move):
	board[move] = letter

#Judge if a side has won the game
def isWinner(bo, le):
	return (
	(bo[7] == le and bo[8] == le and bo[9] == le) or
	(bo[4] == le and bo[5] == le and bo[6] == le) or
	(bo[1] == le and bo[2] == le and bo[3] == le) or
	(bo[7] == le and bo[4] == le and bo[1] == le) or
	(bo[8] == le and bo[5] == le and bo[2] == le) or
	(bo[9] == le and bo[6] == le and bo[3] == le) or
	(bo[7] == le and bo[5] == le and bo[3] == le) or
	(bo[9] == le and bo[5] == le and bo[1] == le) 
		)

#Judge if the game has been over
def gameOver(board, computerLetter, playerLetter):
	if (isBoardFull(board) 
		or isWinner(board, computerLetter) 
		or isWinner(board, playerLetter)):
		return True
	return False

#Judge if a space is free to make a move
def isSpaceFree(board, move):
	return board[move] == ' '

#Get input of player to make a move
def getPlayerMove(board):
	move = ' '
	while (move not in '1 2 3 4 5 6 7 8 9'.split() or 
		not isSpaceFree(board, int(move))):
		print('What is your next move?(1-9)')
		move = input()
	return int(move)

#Judge if the board is full
def isBoardFull(board):
	for i in range(1, 10):
		if isSpaceFree(board, i):
			return False
	return True

#Using MiniMax to determine the next move of computer
#Maximize min-values of the next floor in the decision tree
def getComputerMove(board, computerLetter, playerLetter, depth):
	best = -100
	bestMove = None
	movesList = generateLegalMoves(board)
	for move in movesList:
		makeMove(board, computerLetter, move)
		val = Min(board, computerLetter, playerLetter, depth)
		unMakeMove(board, move)
		if(val > best):
			best = val
			bestMove = move
	return bestMove


	return Max(board, computerLetter, playerLetter, depth)

#Maximize min-values of the next floor in the decision tree
def Max(board, computerLetter, playerLetter, depth):
	best = -100
	if (depth <= 0 or gameOver(board, computerLetter, playerLetter)):
		return evaluate(board, computerLetter, playerLetter)
	movesList = generateLegalMoves(board)
	for move in movesList:
		makeMove(board, computerLetter, move)
		val = Min(board, computerLetter, playerLetter, depth - 1)
		unMakeMove(board, move)
		if(val > best):
			best = val
	return best

#Minimize max-values of the next floor in the decision tree
def Min(board, computerLetter, playerLetter, depth):
	best = 100
	if (depth <= 0 or gameOver(board, computerLetter, playerLetter)):
		return evaluate(board, computerLetter, playerLetter)
	movesList = generateLegalMoves(board)
	for move in movesList:
		makeMove(board, playerLetter, move)
		val = Max(board, computerLetter, playerLetter, depth - 1)
		unMakeMove(board, move)
		if(val < best):
			best = val
	return best

#Count the winning combos left for one side
def countWinningCombosLeft(board, letter):
	winningCombos = [[7, 8, 9], [4, 5, 6], [1, 2, 3], 
					 [7, 4, 1], [8, 5, 2], [9, 6, 3],
					 [7, 5, 3], [9, 5, 1]]
	number = 0;
	for combo in winningCombos:
		found = False
		for i in combo:
			if not (isSpaceFree(board, i) or board[i] == letter):
				found = False
				break
			found = True
		if found:
			number += 1
	return number

#Heuristic function for Minimax Algorithme 
def evaluate(board, computerLetter, playerLetter):
	if isWinner(board, computerLetter):
		return 100
	elif isWinner(board, playerLetter):
		return -100
	return countWinningCombosLeft(board, computerLetter) - countWinningCombosLeft(board, playerLetter)

#Generate a list containing all legal moves for the current state of board
def generateLegalMoves(board):
	legalMoves = []
	for i in range(1, 10):
		if isSpaceFree(board, i):
			legalMoves.append(i)
	return legalMoves

#Unmake a move
def unMakeMove(board, move):
	board[move] = ' '

#Main game loop
def gameStart():
	print('Welcome to Tic Tac Toe!')

	while True:
		theBorad = [' '] * 10
		playerLetter, computerLetter = inputPlayerLetter()
		turn = whoGoesFirst()
		print('The %s will go first.' % turn)
		gameIsPlaying = True

		while gameIsPlaying:
			if turn == 'player':
				drawBoard(theBorad)
				move = getPlayerMove(theBorad)
				makeMove(theBorad, playerLetter, move)

				if isWinner(theBorad, playerLetter):
					drawBoard(theBorad)
					print('Hooray! You have won the game!')
					gameIsPlaying = False
				else:
					if isBoardFull(theBorad):
						drawBoard(theBorad)
						print('The game is a tie!')
						gameIsPlaying = False
					else:
						turn = 'computer'
			else:
				move = getComputerMove(theBorad, computerLetter, 
					playerLetter, 3)
				makeMove(theBorad, computerLetter,move)

				if isWinner(theBorad, computerLetter):
					drawBoard(theBorad)
					print('The computer has beaten you! You lose.')
					gameIsPlaying = False
				else:
					if isBoardFull(theBorad):
						drawBoard(theBorad)
						print('The game is a tie!')
						gameIsPlaying = False
					else:
						turn = 'player'

		if not playAgain():
			break
#Start game
gameStart()