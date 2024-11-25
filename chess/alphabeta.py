from .chess import Board

class AlphaBeta:
    def __init__(self):
        pass

    def alphabeta(board: Board, depth, maximizing_player):
        if depth == 0:
            return AlphaBeta.evaluate(board)
        alpha = float('-inf')
        beta = float('inf')        
        if maximizing_player:
            return AlphaBeta.ab_max(board, depth, alpha, beta, maximizing_player)
        else:
            return AlphaBeta.ab_min(board, depth, alpha, beta, -maximizing_player)
    
    def ab_max(board: Board, depth, alpha, beta, player):
        if depth == 0:
            return AlphaBeta.evaluate(board), None
        
        max_eval = float('-inf')
        best_move = None
        for move in board.list_moves(player):
            b = board.copy()
            b.move(*move)
            eval, _ = AlphaBeta.ab_min(b, depth-1, alpha, beta, -player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    
    def ab_min(board: Board, depth, alpha, beta, player):   
        if depth == 0:
            return AlphaBeta.evaluate(board), None
        
        min_eval = float('inf')
        best_move = None
        for move in board.list_moves(player):
            b = board.copy()
            b.move(*move)
            eval, _ = AlphaBeta.ab_max(b, depth-1, alpha, beta, -player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
        
        
    
    def evaluate(board: Board):
        """
        Evaluate the board state
        """
        VALUE_PAWN = 100
        VALUE_KNIGHT = 320
        VALUE_BISHOP = 330
        VALUE_ROOK = 500
        VALUE_QUEEN = 900
        
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(col, row)
                if piece == 0:
                    continue
                color = piece // abs(piece)
                piece = abs(piece)
                if piece == 1:
                    score += VALUE_PAWN * color
                elif piece == 2:
                    score += VALUE_KNIGHT * color
                elif piece == 3:
                    score += VALUE_BISHOP * color
                elif piece == 4:
                    score += VALUE_ROOK * color
                elif piece == 5:
                    score += VALUE_QUEEN * color
        return score