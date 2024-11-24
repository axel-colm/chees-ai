from .chess import Board

class AlphaBeta:
    def __init__(self):
        pass

    def alphabeta(board: Board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return board.evaluate()
        if maximizing_player:
            max_eval = float('-inf')
            pieces = board.get_pieces_of(1)
            for piece in pieces:
                moves = board.get_legal_moves(*piece)
                for move in moves:
                    board.move(*piece, *move)
                    eval = AlphaBeta.alphabeta(board, depth - 1, alpha, beta, False)
                    board.undo_move()
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            pieces = board.get_pieces_of(-1)
            for piece in pieces:
                moves = board.get_legal_moves(*piece)
                for move in moves:
                    board.move(*piece, *move)
                    eval = AlphaBeta.alphabeta(board, depth - 1, alpha, beta, True)
                    board.undo_move()
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval
        
    def get_best_move(b: Board, depth, maximizing_player):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        board = b.copy()
        pieces = board.get_pieces_of(maximizing_player)
        for piece in pieces:
            moves = board.get_legal_moves(*piece)
            for move in moves:
                board.move(*piece, *move)
                eval = AlphaBeta.alphabeta(board, depth - 1, alpha, beta, not maximizing_player)
                board.undo_move()
                if eval > max_eval:
                    max_eval = eval
                    best_move = (piece, move)
        return best_move