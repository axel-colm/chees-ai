from .board import Board

class Chess(object):

    def __init__(self):
        self.board = Board()
        self.turn = -1

    def reset(self):
        self.board.init_board()
        self.turn = -1 
    
    def load(self, moves: list):
        self.reset()
        self.board.apply_moves(moves)
            
    def move(self, move: str):
        # convert coordinates to row, col
        if self.board.apply_move([move]):
            self.turn = -self.turn
            return True    
        return False

    
    
    
        
        
        