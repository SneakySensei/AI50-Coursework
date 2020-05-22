"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

# Custom Exception Class for Invalid Moves
class InvalidMoveException(Exception):
    
    def __init__(self, expression, message="Trying to move on a non-empty cell"):
        self.expression = expression
        self.message = message


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
            

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    
    # if board has lesser or eual X(s) than O(s)
    if sum([row.count(X) for row in board]) <= sum([row.count(O) for row in board]):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionSet = set()

    # if cell is empty it's a valid move
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actionSet.add((i, j))

    return actionSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Deepcopy so that original board is not affected as it will be needed for recursion
    resultBoard = copy.deepcopy(board)

    if resultBoard[i][j] is not EMPTY:
        raise InvalidMoveException
    
    resultBoard[i][j] = player(board)
    return resultBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking for 3 in a row
    for row in board:
        if row[0] is not EMPTY and row[0] == row[1] == row[2]:
            return row[0]

    # Checking for 3 in a col
    for col in range(len(board)):
        if board[0][col] is not EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Checking for Diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] is not EMPTY and board[0][2] == board[2][0] == board[1][1]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there is a winner or if there is no possible action left
    if winner(board) is not None or actions(board) == set():
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X: return 1
    elif win == O: return - 1
    else: return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # If AI is X, ie, maximizing player
    if player(board) is X:
        _, bestAction = maximum(board, -math.inf, math.inf)
        return bestAction
    elif player(board) is O:
        _, bestAction = minimum(board, -math.inf, math.inf)
        return bestAction


# Helper function for minimax. Called by minimizing player on its possible moves.
def maximum(board, alpha, beta):

    # If game has ended, ie base case, return utility of the board
    if (terminal(board)):
        return (utility(board), None)

    bestAction = None
    bestScore = -math.inf

    # Shuffling the set of actions makes equally valued moves randomised
    actionList = list(actions(board))
    random.shuffle(actionList)

    # For every successor action,
    for action in actionList:
        # Get the best the opponent can do
        minValue, _ = minimum(result(board, action), alpha, beta)
        # Update current best score and current best move
        if minValue > bestScore:
            bestScore = minValue
            bestAction = action
        
        # If bestScore is irrelevant, prune the rest of the branches
        if bestScore >= beta:
            break
        # Else update alpha
        alpha = max(alpha, bestScore)
    return (bestScore, bestAction)


# Helper function for minimax.  Called by maximizing player on its possible moves.
def minimum(board, alpha, beta):

    # If game has ended, ie base case, return utility of the board
    if (terminal(board)):
        return (utility(board), None)
    
    bestAction = None
    bestScore = math.inf
    
    # Shuffling the set of actions makes equally valued moves randomised
    actionList = list(actions(board))
    random.shuffle(actionList)

    # For every successor action,
    for action in actionList:
        # Get the best the opponent can do
        maxValue, _ = maximum(result(board, action), alpha, beta)
        # Update current best score and current best move
        if maxValue < bestScore:
            bestScore = maxValue
            bestAction = action

        # If bestScore is irrelevant, prune the rest of the branches
        if bestScore <= alpha:
            break
        # Else update beta
        beta = min(beta, bestScore)
    return (bestScore, bestAction)