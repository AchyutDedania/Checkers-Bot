"""
GROUP_1
Achyut Dedania  2021A7PS2807H
Darsh Nayak     2021A7PS2306H
Vasu Bhadja     2021A7PS2569H
Shrey Paunwala  2021A7PS2808H
"""

import random
from datetime import datetime
from copy import deepcopy

WHITE    = (255, 255, 255)
GREY     = (128, 128, 128)
PURPLE   = (178, 102, 255)
BLACK    = (  0,   0,   0)
GOLD     = ( 51,   0,  51)
HIGH     = (160, 190, 255)

def evaluate_board(bot, board):
    bot_regular_value = 5
    bot_king_value = 10
    opponent_regular_value = -5
    opponent_king_value = -10
    center_value = 1.5
    back_row_penalty = -0.5
    move_value = 0.5
    king_move_value = 1
    protected_piece_bonus = 2
    threatened_penalty = -4
    threatened_opponent_bonus = 4
    progression_bonus = 0.2
    king_safety_bonus = 1.5
    piece_mobility_factor = 0.3
    king_aggression_bonus = 2

    rows, cols = 8, 8
    score = 0
    bot_pieces = 0
    opponent_pieces = 0
    
    def is_protected(board, row, col):
        """Check if the piece at board[row][col] is protected (has adjacent friendly pieces)."""
        piece = board.getSquare(row, col).squarePiece
        adjacent_positions = [(row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
        
        for r, c in adjacent_positions:
            if 0 <= r < rows and 0 <= c < cols:
                if ((board.getSquare(r, c).squarePiece is None) or 
                    piece.color == board.getSquare(r, c).squarePiece.color):
                    return True
        return False

    def is_threatened(board, row, col):
        """Check if the piece at board[row][col] can be captured by the opponent."""
        piece = board.getSquare(row, col).squarePiece
        capture_positions = [(row-2, col-2), (row-2, col+2), (row+2, col-2), (row+2, col+2)]
        jump_over_positions = [(row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
        
        for (r_jump, c_jump), (r_over, c_over) in zip(capture_positions, jump_over_positions):
            if 0 <= r_jump < rows and 0 <= c_jump < cols:
                if 0 <= r_over < rows and 0 <= c_over < cols:
                    if (board.getSquare(r_over, c_over).color != piece.color and 
                        board.getSquare(r_over, c_over) is not None):
                        if board.getSquare(r_jump, c_jump) is None:
                            return True
        return False

    def get_piece_mobility(board, row, col):
        """Count the number of legal moves the piece at board[row][col] can make."""
        piece = board.getSquare(row, col).squarePiece
        mobility = 0
        move_positions = [(row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
        
        if piece.king:
            move_positions += [(row-2, col-2), (row-2, col+2), (row+2, col-2), (row+2, col+2)]
        
        for r, c in move_positions:
            if 0 <= r < rows and 0 <= c < cols:
                if board.getSquare(r, c) is None:
                    mobility += 1
        return mobility

    for row in range(rows):
        for col in range(cols):
            piece = board.getSquare(row, col).squarePiece
            if piece is None:
                continue

            # Bot's regular piece
            if piece.color == bot.eval_color and not piece.king:
                score += bot_regular_value
                bot_pieces += 1
                
                # Apply penalties for being on the back row
                if piece.color == PURPLE and row == 7:
                    score += back_row_penalty
                if piece.color == GREY and row == 0:
                    score += back_row_penalty
                
                # Center control bonus
                if 2 <= row <= 5 and 2 <= col <= 5:
                    score += center_value
                
                # Protection and threat checks
                if is_protected(board, row, col):
                    score += protected_piece_bonus
                if is_threatened(board, row, col):
                    score += threatened_penalty

                # Progression bonus for pieces advancing
                if piece.color == PURPLE:
                    score += progression_bonus * (7 - row)
                else:
                    score += progression_bonus * row

            # Bot's king
            elif piece.color == bot.eval_color and piece.king:
                score += bot_king_value
                bot_pieces += 1
                
                # Center control bonus
                if 2 <= row <= 5 and 2 <= col <= 5:
                    score += center_value
                
                # King aggression bonus for being close to opponent pieces
                if is_threatened(board, row, col):
                    score += king_aggression_bonus
                
                # King safety bonus for being close to the edges
                if col == 0 or col == 7:
                    score += king_safety_bonus
                
                # Protection and threat checks
                if is_protected(board, row, col):
                    score += protected_piece_bonus
                if is_threatened(board, row, col):
                    score += threatened_penalty

            # Opponent's regular piece
            elif piece.color != bot.eval_color and not piece.king:
                score += opponent_regular_value
                opponent_pieces += 1

                # Check if opponent piece is threatened
                if is_threatened(board, row, col):
                    score += threatened_opponent_bonus

            # Opponent's king
            elif piece.color != bot.eval_color and piece.king:
                score += opponent_king_value
                opponent_pieces += 1
                
                # Check if opponent king is threatened
                if is_threatened(board, row, col):
                    score += threatened_opponent_bonus

    # Mobility (based on the number of bot's pieces)
    score += move_value * bot_pieces
    score += king_move_value * (bot_pieces // 2)  # Estimate king mobility
    
    # Factor in piece mobility to encourage movement
    for row in range(rows):
        for col in range(cols):
            if board.getSquare(row, col).squarePiece and board.getSquare(row, col).squarePiece.color == bot.eval_color:
                score += piece_mobility_factor * get_piece_mobility(board, row, col)
    
    return score

    
def filterMoves(possible_moves):
    best_moves = []
    numCapture = 0
    isCapture = False
    for move in possible_moves:
        for end_pos in move[2]:
            if(abs(end_pos[0] - move[0]) == 2 and abs(end_pos[1] - move[1]) == 2):
                best_moves.append(move)
                numCapture += 1
                isCapture = True

    if not best_moves:
        best_moves = possible_moves
    return best_moves, isCapture, numCapture

def checkCapture(move,end_pos):
    if(abs(end_pos[0] - move[0]) == 2 and abs(end_pos[1] - move[1]) == 2):
        return True
    return False
    

# Minimax function to determine the best move
def minimax(bot, board, depth, alpha, beta, maximizing_player, start_time, endCall):
    end_time = datetime.now()
    if (end_time - start_time).total_seconds() >= 18:
        endCall[0] = True
        return float('-inf'), None
    possible_moves = bot.getPossibleMoves(board)
    possible_best_moves, isCapture, numCapture = filterMoves(possible_moves)
        
    if depth == 0 or not possible_best_moves:
        return evaluate_board(bot, board), None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in possible_best_moves:
            for end_pos in move[2]:
                if isCapture:
                    if not checkCapture(move,end_pos):
                        continue
                    if numCapture == 1:
                        return evaluate_board(bot, board), (move, end_pos)
                    
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1], end_pos[0], end_pos[1])
                eval = minimax(bot, new_board, depth - 1, alpha, beta, False, start_time, endCall)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (move, end_pos)

                elif(eval == max_eval):
                    if(random.choice([True,False])):
                        best_move = (move, end_pos)

                alpha = max(alpha,eval)
                if beta <= alpha:
                    break
                if endCall[0]:
                    return max_eval, best_move
        return max_eval, best_move
    
    else:
        min_eval = float('inf')
        best_move = None
        for move in possible_best_moves:
            for end_pos in move[2]:
                if isCapture:
                    if not checkCapture(move, end_pos):
                        continue

                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1], end_pos[0], end_pos[1])
                eval = minimax(bot,new_board, depth - 1, alpha, beta, True, start_time, endCall)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (move, end_pos)

                elif(eval == min_eval):
                    if(random.choice([True,False])):
                        best_move = (move, end_pos)

                beta = min(beta,eval)
                if beta <= alpha:
                    break
                if endCall[0]:
                    return min_eval, best_move
        return min_eval, best_move

# Modified group1 function to use Minimax algorithm
def group1(self, board):
    possible_moves = self.getPossibleMoves(board)

    possible_best_moves = filterMoves(possible_moves)
    num = len(possible_best_moves)
    depth = 3 # Set the depth of the Minimax algorithm
    if(num > 5):
        depth = 3
    elif(num > 3):
        depth = 4
    else:
        depth = 5
        
    start_time = datetime.now()
    endCall = [False]
    _, best_move = minimax(self, board, depth, float('-inf'), float('inf'), True, start_time, endCall)

    if best_move is None:
        random_move = random.choice(possible_moves)
        rand_choice = random.choice(random_move[2]) 
        return random_move, rand_choice
    if best_move:
        return best_move
    else:
        self.game.end_turn()
        return