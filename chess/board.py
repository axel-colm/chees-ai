from typing import List, Tuple

class Board:
    # Constants
    WIDTH = 8
    HEIGHT = 8
    
    # Variables
    board: List[List[int]]
    moves: List[str]
    
    def __init__(self):
        # create empty board
        self.board = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        
        self.init_board()
        
    def apply_move(self, move: list) -> bool:
        for coord in move:
            if isinstance(coord, str):
                start, end = coord.split("-")
                x, y = self.convert_coord(start)
                new_x, new_y = self.convert_coord(end)
                if not self.move(x, y, new_x, new_y):
                    return False
                
            elif (isinstance(coord, tuple) or isinstance(coord, list)) and len(coord) == 2 and len(coord[0]) == 2 and len(coord[1]) == 2:
                x, y = self.convert_coord(coord[0])
                new_x, new_y = self.convert_coord(coord[1])
                if not self.move(x, y, new_x, new_y):
                    return False
            else:
                return False
        return True
            
    #########################################################
    #                       Board functions                 #
    #########################################################
        
    def init_board(self):
        """
        Initialize the board with the pieces in their starting positions
        
        1: black pawn
        2: black rook
        3: black knight
        4: black bishop
        5: black queen
        6: black king
        
        -1: white pawn
        -2: white rook
        -3: white knight
        -4: white bishop
        -5: white queen
        -6: white king
        
        """
        # Pawns
        for i in range(self.WIDTH):
            self.board[1][i] = -1
            self.board[self.HEIGHT - 2][i] = 1
            
        # Rooks
        self.board[0][0] = -2
        self.board[0][self.WIDTH - 1] = -2
        self.board[self.HEIGHT - 1][0] = 2
        self.board[self.HEIGHT - 1][self.WIDTH - 1] = 2
        
        # Knights
        self.board[0][1] = -3
        self.board[0][self.WIDTH - 2] = -3
        self.board[self.HEIGHT - 1][1] = 3
        self.board[self.HEIGHT - 1][self.WIDTH - 2] = 3
        
        # Bishops
        self.board[0][2] = -4
        self.board[0][self.WIDTH - 3] = -4
        self.board[self.HEIGHT - 1][2] = 4
        self.board[self.HEIGHT - 1][self.WIDTH - 3] = 4
        
        # Queens
        self.board[0][3] = -5
        self.board[self.HEIGHT - 1][3] = 5
        
        # Kings
        self.board[0][4] = -6
        self.board[self.HEIGHT - 1][4] = 6
       
        # Moves
        self.moves = []
        
    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT
    
    def is_empty(self, x: int, y: int) -> bool:
        if not self.is_inside(x, y):
            return False
        return self.board[y][x] == 0
            
    def get_color(self, x: int, y: int) -> int:
        if not self.is_inside(x, y) or self.is_empty(x, y):
            return 0
        return self.board[y][x] // abs(self.board[y][x])
    
    def get_piece(self, x: int, y: int) -> int:
        if not self.is_inside(x, y):
            return 0
        return self.board[y][x]
    
    def convert_coord(self, coord: str) -> Tuple[int, int]:
        x, y = coord[0], coord[1]
        x = x.upper()
        return ord(x) - ord('A'), int(y) - 1
    
    def convert_coord_inv(self, x: int, y: int) -> str:
        return chr(x + ord('A')) + str(y + 1) 
    
    def get_pieces_of(self, color: int) -> List[Tuple[int, int]]:
        pieces = []
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.get_color(j, i) == color:
                    pieces.append((j, i))
        return pieces
    
    def is_check(self, color: int) -> bool:
        king_pos = next((j, i) for i in range(self.HEIGHT) for j in range(self.WIDTH) if self.board[i][j] == 6 * color)
        opponent_pieces = self.get_pieces_of(-color)
        for piece in opponent_pieces:
            if self.can_move(piece[0], piece[1], king_pos[0], king_pos[1]):
                return True
        return False
    
    def is_checkmate(self, color: int) -> bool:
        if not self.is_chess(color):
            return False
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.get_color(j, i) == color:
                    moves = self.get_legal_moves(j, i)
                    for move in moves:
                        x, y = move
                        if self.move(j, i, x, y) and not self.is_chess(color):
                            self.undo_move()
                            return False
                        self.undo_move()
        return True
    
    def is_game_over(self) -> bool:
        return False
    
    #########################################################
    #                       Move functions                  #
    #########################################################
    def move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        # Check if the coordinates are valid
        if not self.is_inside(x, y) or not self.is_inside(new_x, new_y):
            return False
        # Check if the move is valid
        piece = self.board[y][x]
        if piece == 0 or not self.can_move(x, y, new_x, new_y):
            return False
                
        # Move the piece
        self.board[new_y][new_x] = piece
        self.board[y][x] = 0
        
        # Special moves
        # Castling
        if abs(piece) == 6 and abs(x - new_x) == 2:
            if new_x == 2:
                self.board[new_y][3] = self.board[new_y][0]
                self.board[new_y][0] = 0
            elif new_x == 6:
                self.board[new_y][5] = self.board[new_y][7]
                self.board[new_y][7] = 0
                
        # Promotion
        if abs(piece) == 1 and (new_y == 0 or new_y == 7):
            self.board[new_y][new_x] = 5 * self.get_color(new_x, new_y)
            
        # Update moves
        self.moves.append(self.convert_coord_inv(x, y) + "-" + self.convert_coord_inv(new_x, new_y))
        
        return True
   
    def undo_move(self):
        if len(self.moves) == 0:
            return False
        move = self.moves.pop()
        start, end = move.split("-")
        x, y = self.convert_coord(start)
        new_x, new_y = self.convert_coord(end)
        piece = self.board[new_y][new_x]
        self.board[new_y][new_x] = 0
        self.board[y][x] = piece
        return True
    
    def can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        piece = self.board[y][x]
        value = False
        if piece == 0 or not self.is_inside(x, y) or not self.is_inside(new_x, new_y):
            return value            
        if piece == 1 or piece == -1:
            return self.pawn_can_move(x, y, new_x, new_y)
        if piece == 2 or piece == -2:
            return self.rook_can_move(x, y, new_x, new_y)
        if piece == 3 or piece == -3:
            return self.knight_can_move(x, y, new_x, new_y)
        if piece == 4 or piece == -4:
            return self.bishop_can_move(x, y, new_x, new_y)
        if piece == 5 or piece == -5:
            return self.queen_can_move(x, y, new_x, new_y)
        if piece == 6 or piece == -6:
            return self.king_can_move(x, y, new_x, new_y)
        return False

    def pawn_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        color = self.get_color(x, y)
        if color == 0:
            return False
        
        direction = -color
        start_row = 1 if color == -1 else 6
        
        return (
            # Move forward
            (y + direction == new_y and x == new_x and self.is_empty(new_x, new_y)) or
            # Move two steps forward
            (y == start_row and y + 2 * direction == new_y and x == new_x and self.is_empty(new_x, new_y) and self.is_empty(new_x, new_y - direction)) or
            # Capture diagonally
            (abs(new_x - x) == 1 and y + direction == new_y and not self.is_empty(new_x, new_y) and self.get_color(new_x, new_y) != color) or
            # En passant
            (y == 4 and abs(new_x - x) == 1 and y + direction == new_y and self.is_empty(new_x, new_y) and 
            not self.is_empty(new_x, y) and self.get_color(new_x, y) != color)   
        )
        
    def rook_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        return (
            # Piece is rook or queen
            abs(self.board[y][x]) in [2, 5] and
            # Destination is different color or empty
            (
                self.get_color(new_x, new_y) != self.get_color(x, y) or
                self.is_empty(new_x, new_y)
            ) and
            # Move horizontally or vertically
            (
                new_x == x and all(self.is_empty(x, i) for i in range(min(y, new_y) + 1, max(y, new_y))) or
                new_y == y and all(self.is_empty(i, y) for i in range(min(x, new_x) + 1, max(x, new_x)))
            )
        )

    def knight_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:

        return (
            # Piece is knight
            abs(self.board[y][x]) == 3 and
            # Destination is different color or empty
            (
                self.get_color(new_x, new_y) != self.get_color(x, y) or
                self.is_empty(new_x, new_y)
            ) and
            # Move in L shape
            (
                (abs(new_x - x) == 1 and abs(new_y - y) == 2) or
                (abs(new_x - x) == 2 and abs(new_y - y) == 1)
            )
        )
    
    def bishop_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        
        return (
            # Piece is bishop or queen
            abs(self.board[y][x]) in [4, 5] and
            # Move diagonally
            abs(new_x - x) == abs(new_y - y) and
            # Destination is different color or empty
            (
            self.get_color(new_x, new_y) != self.get_color(x, y) or
            self.is_empty(new_x, new_y)
            ) and
            # Path is clear
            all(
            self.is_empty(x + i * (1 if new_x > x else -1), y + i * (1 if new_y > y else -1))
            for i in range(1, abs(new_x - x))
            )
        )
    
    def queen_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        rook = self.rook_can_move(x, y, new_x, new_y)
        bishop = self.bishop_can_move(x, y, new_x, new_y)

        return rook or bishop
    
    def king_can_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        return (
            # Piece is king
            abs(self.board[y][x]) == 6 and
            # Destination is different color or empty
            (
                # Normal move
                (
                    (
                        self.get_color(new_x, new_y) != self.get_color(x, y) or
                        self.is_empty(new_x, new_y)
                    ) and
                    # Move one step in any direction
                    (
                        abs(new_x - x) <= 1 and abs(new_y - y) <= 1
                    ) 
                ) or 
                # Castling
                (
                    abs(new_x - x) == 2 and new_y == y and
                    self.is_empty(new_x, y) and
                    self.is_empty(new_x - 1, y) and
                    self.rook_can_move(0 if new_x == 2 else 7, y, new_x - 1, y)
                )
            ) 
            
        )
    
    def get_legal_moves(self, x: int, y: int) -> List[Tuple[int, int]]:
        piece = self.board[y][x]
        if piece == 0:
            return []
        moves = []
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.can_move(x, y, j, i):
                    board = self.copy()
                    board.move(x, y, j, i)
                    if not board.is_check(self.get_color(x, y)):
                        moves.append((j, i))
        return moves
    #########################################################
    #                       Display functions               #
    #########################################################
    def str(self):
        letters = "ABCDEFGH"
        space = 5
        output = " " * space + "|" + "|".join([" " * ((space - len(letter)) // 2) + letter + " " * ((space - len(letter)) // 2 + (space - len(letter)) % 2) for letter in letters]) + "|\n"
        width = len(output)
        output += "-" * (width - 1) + "\n"
        for i in range(self.HEIGHT):
            output += str(self.HEIGHT - i) + " " * (space - len(str(self.HEIGHT - i))) + "|"
            for j in range(self.WIDTH):
                piece = self.board[i][j]
                if piece == 0:
                    output += " " * space 
                else:
                    output += " " * ((space - len(str(piece))) // 2 ) + str(piece) + " " * ((space - len(str(piece))) // 2 + (space - len(str(piece))) % 2)
                output += " " if j != self.WIDTH - 1 else ""
            output += "|\n"
            output += " " * space + "|" + " " * ((space + 1) * self.WIDTH - 1) + "|\n"
        output += "-" * (width - 1) + "\n"
        return output 
    
    def display(self):
        # display board with pieces emojis
        pieces = {
            0: ".",
            1: "♙",
            -1: "♟",
            2: "♖",
            -2: "♜",
            3: "♘",
            -3: "♞",
            4: "♗",
            -4: "♝",
            5: "♕",
            -5: "♛",
            6: "♔",
            -6: "♚"
        }
        letters = "ABCDEFGH"
        output = "    " + " ".join(letters) + "\n"
        output += "-" * (self.WIDTH * 2 + 4) + "\n"
        for i in range(self.HEIGHT):
            output += str(i + 1) + " | "
            for j in range(self.WIDTH):
                piece = self.board[i][j]
                output += pieces[piece] + " "
            output += "\n"
        output += "-" * (self.WIDTH * 2 + 4) + "\n"
        return output
    
    def fen(self):
        fen = ""
        for i in range(self.HEIGHT):
            empty = 0
            for j in range(self.WIDTH):
                piece = self.board[i][j]
                if piece == 0:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += self.piece_to_fen(piece)
            if empty > 0:
                fen += str(empty)
            if i != self.HEIGHT - 1:
                fen += "/"
        return fen
    
    def copy(self):
        new_board = Board()
        new_board.board = [row.copy() for row in self.board]
        new_board.moves = self.moves.copy()
        return new_board
    
    def piece_to_fen(self, piece: int) -> str:
        pieces = {
            1: "p",
            2: "r",
            3: "n",
            4: "b",
            5: "q",
            6: "k",
            -1: "P",
            -2: "R",
            -3: "N",
            -4: "B",
            -5: "Q",
            -6: "K",
        }
        return pieces[piece]
    
    def fen_to_piece(self, piece: str) -> int:
        pieces = {
            "p": 1,
            "r": 2,
            "n": 3,
            "b": 4,
            "q": 5,
            "k": 6,
            "P": -1,
            "R": -2,
            "N": -3,
            "B": -4,
            "Q": -5,
            "K": -6,
        }
        return pieces[piece]
    
    def piece_value(self, piece: int) -> int:
        values = {
            1: 1,
            2: 5,
            3: 3,
            4: 3,
            5: 9,
            6: 1000,
            -1: -1,
            -2: -5,
            -3: -3,
            -4: -3,
            -5: -9,
            -6: -1000,
        }
        return values[piece]
    
    def evaluate(self):
        score = 0
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                piece = self.board[i][j]
                if piece == 0:
                    continue
                score += self.piece_value(piece)
        return score
    
if __name__ == '__main__':
    board = Board()
    board.apply_move(
        [
            "E2-E4",
            "E7-E5",
            "D2-D4",
            "D7-D5",
            "B1-C3",
            "G8-F6",
            "C1-E3",
            "F8-E7",
            "E1-D2",
        ]
    )
    print(board.display())

    
    
    