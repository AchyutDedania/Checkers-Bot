import random
from components.GuiHandler import Board,Square,Piece

WHITE    = (255, 255, 255)
GREY     = (128, 128, 128)
PURPLE      = (178, 102, 255)
BLACK    = (  0,   0,   0)
GOLD     = (51,0,51)
HIGH     = (160, 190, 255)


# Function to create a deep copy of the board
def copy_board(board):
    new_board = Board()
    new_board.matrix = [[Square(square.color) for square in row] for row in board.matrix]
    for x in range(8):
        for y in range(8):
            if board.matrix[x][y].squarePiece:
                new_board.matrix[x][y].squarePiece = Piece(board.matrix[x][y].squarePiece.color, board.matrix[x][y].squarePiece.king)
    return new_board

# Function to move a piece on the board
def move_piece(board, start_x, start_y, end_x, end_y):
    piece = board.getSquare(start_x, start_y).squarePiece
    board.remove_piece(start_x, start_y)
    board.getSquare(end_x, end_y).squarePiece = piece
    # Check if the move is a jump
    if abs(end_x - start_x) == 2 and abs(end_y - start_y) == 2:
        # Calculate the coordinates of the jumped piece
        jumped_x = (start_x + end_x) // 2
        jumped_y = (start_y + end_y) // 2
        # Remove the jumped piece
        board.remove_piece(jumped_x, jumped_y)
    board.king(end_x, end_y)
    

# Minimax function to determine the best move
def minimax(self, board, depth,alpha,beta,maximizing_player):
    possible_moves = self.getPossibleMoves(board)
    if depth == 0 or not possible_moves:
        return self.evaluate(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_moves:
            for end_pos in move[2]:
                new_board = copy_board(board)
                move_piece(new_board, move[0], move[1], end_pos[0], end_pos[1])
                eval = minimax(self,new_board, depth - 1, alpha,beta,False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (move, end_pos)
                elif(eval==max_eval):
                    if(random.choice([True,False])):
                        best_move = (move, end_pos)
                alpha=max(alpha,eval)
                if beta<=alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_moves:
            for end_pos in move[2]:
                new_board = copy_board(board)
                move_piece(new_board, move[0], move[1], end_pos[0], end_pos[1])
                eval = minimax(self,new_board, depth - 1, alpha,beta,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (move, end_pos)
                elif(eval==min_eval):
                    if(random.choice([True,False])):
                        best_move = (move, end_pos)
                beta=min(beta,eval)
                if beta<=alpha:
                    break
        return min_eval, best_move

# Modified group2 function to use Minimax algorithm
def group2(self, board):
    possible_moves = self.getPossibleMoves(board)
    num=len(possible_moves)
    depth=4 # Set the depth of the Minimax algorithm
    if(num>5):
        depth=3
    elif(num>3):
        depth=4
    else:
        depth=5
     
    _, best_move = minimax(self,board, depth,float('-inf'),float('inf'), True)
    if best_move:
        return best_move
    else:
        self.game.end_turn()
        return
