
import copy
import random
import math
import time
import collections

# Function to write output to a text file
def writeOutput(success, board=None):
	output = ''
	if success:
		output += 'OK\n'
		for row in board:
			output += ''.join(str(x) for x in row) + '\n'
		output = output[:-1]
	else:
		output += 'FAIL'
	
	outputFileName = 'output.txt'
	with open(outputFileName, 'w') as f:
		f.write(output)
		f.close()
	
# Function to read input from a text file
def takeInput():
	inputFileName = 'input.txt'
	with open(inputFileName) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	algorithmType = content[0]
	boardSize, queenCount = int(content[1]), int(content[2])
	board = []
	for rowNumber in range(boardSize):
		board.append(map(int, list(content[3 + rowNumber])))
	return (algorithmType, boardSize, queenCount, board)

def printBoard(array):
	for row in array:
		print row
	print '\n'

###########################################################

# Simulated Annealing

INIT_TEMP  = 20000
FIN_TEMP   = 0.05
ALPHA      = 0.98
STEPS      = 200

class SolutionHolder(object):
	def __init__(self, board, queensToPlace):
		self.solution = []
		self.energy = 0.0
		self.board = board
		self.queensToPlace = queensToPlace

		
def generateRandonState(solutionHolder):
	boardSize = len(solutionHolder.board)
	row = random.randint(0, boardSize - 1)
	col = random.randint(0, boardSize - 1)
	while solutionHolder.board[row][col] != 0:
		row = random.randint(0, boardSize - 1)
		col = random.randint(0, boardSize - 1)
	
	random_queen_index = random.randint(0, solutionHolder.queensToPlace - 1)
	old_cordinates = solutionHolder.solution.pop(random_queen_index)
	old_row, old_col = old_cordinates[0], old_cordinates[1]
	solutionHolder.board[old_row][old_col] = 0

	solutionHolder.solution.append((row, col))
	solutionHolder.board[row][col] = 1

	
def initSolution(solutionHolder):
	boardSize = len(solutionHolder.board)
	for i in range(solutionHolder.queensToPlace):
		row = random.randint(0, boardSize - 1)
		col = random.randint(0, boardSize - 1)
		while solutionHolder.board[row][col] != 0:
			row = random.randint(0, boardSize - 1)
			col = random.randint(0, boardSize - 1)
		
		solutionHolder.solution.append((row, col))
		solutionHolder.board[row][col] = 1

def attackCount(board, row, col):
	boardSize = len(board)
	attackCount = 0

	temp_col = col - 1
	treeFound = False
	while temp_col >= 0 and treeFound == False:
		if board[row][temp_col] == 2:
			treeFound = True
		if board[row][temp_col] == 1:
			attackCount += 1
		temp_col -= 1
			
	treeFound = False
	temp_col = col + 1
	while temp_col < boardSize and treeFound == False:
		if board[row][temp_col] == 2:
			treeFound = True
		if board[row][temp_col] == 1:
			attackCount += 1
		temp_col += 1
	
	temp_row = row - 1
	treeFound = False
	while temp_row >= 0 and treeFound == False:
		if board[temp_row][col] == 2:
			treeFound = True
		if board[temp_row][col] == 1:
			attackCount += 1
		temp_row -= 1
	
	temp_row = row + 1
	treeFound = False
	while temp_row < boardSize and treeFound == False:
		if board[temp_row][col] == 2:
			treeFound = True
		if board[temp_row][col] == 1:
			attackCount += 1
		temp_row += 1
		
	temp_row = row + 1
	temp_col = col + 1
	treeFound = False
	while temp_row < boardSize and temp_col < boardSize and treeFound == False:
		if board[temp_row][temp_col] == 2:
			treeFound = True
		if board[temp_row][temp_col] == 1:
			attackCount += 1
		temp_row += 1
		temp_col += 1
	
	temp_row = row - 1
	temp_col = col - 1
	treeFound = False
	while temp_row >= 0 and temp_col >= 0 and treeFound == False:
		if board[temp_row][temp_col] == 2:
			treeFound = True
		if board[temp_row][temp_col] == 1:
			attackCount += 1
		temp_row -= 1
		temp_col -= 1
		
	temp_row = row - 1
	temp_col = col + 1
	treeFound = False
	while temp_row >= 0 and temp_col < boardSize and treeFound == False:
		if board[temp_row][temp_col] == 2:
			treeFound = True
		if board[temp_row][temp_col] == 1:
			attackCount += 1
		temp_row -= 1
		temp_col += 1
	
	temp_row = row + 1
	temp_col = col - 1
	treeFound = False
	while temp_row < boardSize and temp_col >= 0 and treeFound == False:
		if board[temp_row][temp_col] == 2:
			treeFound = True
		if board[temp_row][temp_col] == 1:
			attackCount += 1
		temp_row += 1
		temp_col -= 1
	
	return attackCount
		

def computeSolutionEnergy(solutionHolder):
	boardSize = len(solutionHolder.board)
	conflicts = 0
	for coordinate in solutionHolder.solution:
		row, col = coordinate[0], coordinate[1]
		conflicts += attackCount(solutionHolder.board, row, col)
	solutionHolder.energy = conflicts


def copySolution(sourceSolutionHolder, destinationSolutionHolder):
	destinationSolutionHolder.solution = copy.deepcopy(sourceSolutionHolder.solution)
	destinationSolutionHolder.energy = sourceSolutionHolder.energy
	destinationSolutionHolder.board = copy.deepcopy(sourceSolutionHolder.board)
	
	
def SimulatedAnnealing(board, queensToPlace):
	timer = solution = 0
	boardSize = len(board)
	
	temperature = INIT_TEMP
	currentSolution = SolutionHolder(board, queensToPlace)
	workingSolution = SolutionHolder(board, queensToPlace)
	bestSolution = SolutionHolder(board, queensToPlace)
	
	initSolution(currentSolution)
	computeSolutionEnergy(currentSolution)
	
	bestSolution.energy = 10000.0
	copySolution(currentSolution, workingSolution)
	
	while temperature > FIN_TEMP:
		for step in range(STEPS):
			isStateNeedToChange = False
			
			generateRandonState(workingSolution)
			computeSolutionEnergy(workingSolution)
			
			if workingSolution.energy < currentSolution.energy:
				isStateNeedToChange = True
			else:
				randomProbability = random.random()
				delta_energy = workingSolution.energy - currentSolution.energy
				probability = math.exp((delta_energy*(-1.0))/temperature)
				if probability > randomProbability:
					isStateNeedToChange = True
					
			if isStateNeedToChange:
				isStateNeedToChange = False
				copySolution(workingSolution, currentSolution)
				if currentSolution.energy < bestSolution.energy:
					copySolution(currentSolution, bestSolution)
			else:
				copySolution(currentSolution, workingSolution)
		
		temperature *= ALPHA
		
	if bestSolution.energy == 0:
		writeOutput(True, bestSolution.board)
	else:
		writeOutput(False)

####################################################################

# Helper Function to detarmine if it is safe to place a queen at a position
def safeMove(array, row, col, boardSize):
	
	if row >= boardSize or col >= boardSize:
		return False
	
	if array[row][col] == 2 or array[row][col] == 1:
		return False

	isRowSafe = True
	isColSafe = True
	isForwDiagSafe = True
	isBackDiagSafe = True
	
	for i in range(boardSize):
		#check for same col
		if i >= col and isColSafe == False:
			break
		
		if array[row][i] == 1:
			isColSafe = False
			
		if array[row][i] == 2:
			isColSafe = True
		
		#check for row
		if i >= row and isRowSafe == False:
			break
		
		if array[i][col] == 1:
			isRowSafe = False
			
		if array[i][col] == 2:
			isRowSafe = True
		
		#check for forward diag
		forward_diag_col = row + col - i
		if forward_diag_col >= 0 and forward_diag_col < boardSize:
			if i >= row and isForwDiagSafe == False:
				break
			if array[i][forward_diag_col] == 1:
				isForwDiagSafe = False
			if array[i][forward_diag_col] == 2:
				isForwDiagSafe = True
		
		#check for backward diag
		backward_diag_row = row - col + i
		if backward_diag_row >= 0 and backward_diag_row < boardSize:
			if i >= col and isBackDiagSafe == False:
				break
			if array[backward_diag_row][i] == 1:
				isBackDiagSafe = False
			if array[backward_diag_row][i] == 2:
				isBackDiagSafe = True
		
	return (isRowSafe and isColSafe and isForwDiagSafe and isBackDiagSafe)

##############################################################################

# BFS Solution
	
def createTempBoard(baseBoard, positions):
	newBoard = copy.deepcopy(baseBoard)
	for position in positions:
		newBoard[position[0]][position[1]] = 1
	return newBoard

def alreadyInQueue(queue, tempBoard, nodeLevel):
	for i in range(len(queue)-1, -1, -1):
		state = queue[i]
		if state[1] < nodeLevel:
			return False
		elif state[1] == nodeLevel:
			if state[0] == tempBoard:
				return True
		else:
			pass
	return False


def solutionWithBFSLame(board, queensToPlace):
	stateQueue = []
	boardSize = len(board)
	currentQueenNumber = 0
	tempBoard = copy.deepcopy(board)
	while currentQueenNumber < queensToPlace:
		for row in range(boardSize):
			for col in range(boardSize):
				if safeMove(tempBoard, row, col, boardSize):
					tempBoard[row][col] = 1
					currentQueenNumber += 1
					if currentQueenNumber == queensToPlace:
						writeOutput(True, tempBoard)
						return
					if alreadyInQueue(stateQueue, tempBoard, currentQueenNumber) == False:
						stateQueue.append((copy.deepcopy(tempBoard), currentQueenNumber))
					tempBoard[row][col] = 0
					currentQueenNumber -= 1
		if len(stateQueue) == 0:
			writeOutput(False)
			return
		else:
			
			state = stateQueue.pop(0)
			tempBoard = state[0]
			currentQueenNumber = state[1]

#########################################################

# DFS Solution
def solutionWithDFSHelper(array, boardSize, queenCount, queenPlaced, row, col):
	if queenPlaced >= queenCount:
		writeOutput(True, array)
		return True
	while row < boardSize:
		for nextCol in range(col, boardSize, 1):
			if safeMove(array, row, nextCol, boardSize):
				array[row][nextCol] = 1
				if solutionWithDFSHelper(array, boardSize, queenCount, queenPlaced + 1, row, nextCol + 1) == False:
					array[row][nextCol] = 0
				else:
					return True
		row += 1
		col = 0
	return False

def solutionWithDFS(board, queenCount):
	if solutionWithDFSHelper(board, len(board), queenCount, 0, 0, 0) == False:
		writeOutput(False)
		
###################################################################

if __name__ == '__main__':
	algorithmType, rowCount, queenCount, board = takeInput()
	if sum(x.count(2) for x in board) == 0 and queenCount > rowCount:
		writeOutput(False)
	elif algorithmType == 'BFS':
		solutionWithBFSLame(board, queenCount)
	elif algorithmType == 'DFS':
		solutionWithDFS(board, queenCount)
	else:
		SimulatedAnnealing(board, queenCount)
