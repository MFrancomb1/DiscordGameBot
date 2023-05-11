from typing import Optional
import chess
from chess import STARTING_FEN
"""
board = chess.Board()
print(board.piece_at(chess.A1))

while(not board.is_game_over()):
    bstr = str(board)
    print(bstr)
    print(board.turn)
    move = input("make a move")

    board.push_san(move)
print(board.outcome())
"""

class MyBoard(chess.Board):

    def __init__(self, fen: str | None = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", *, chess960: bool = False) -> None:
        super().__init__(fen, chess960=chess960)
        self.in_progress = False
            
    def move(self, san: str):
            self.in_progress = True    
            #try to make move
            try:
                self.push_san(san)
                return self.endgame() if self.is_game_over() else None                
            
            #handle illegal movces and other errors
            except (chess.IllegalMoveError, chess.InvalidMoveError, chess.AmbiguousMoveError) as e:
                return e
            
    def startgame(self):
        if self.fen() != chess.STARTING_FEN:  
            self.set_fen(chess.STARTING_FEN)

        self.in_progress = True

    def endgame(self):
        winner = "white" if self.outcome().winner else "black"
        result = str(self.outcome().termination).strip("Termination.")
        return f"{self.unicode(invert_color=True)}\n{result}! Winner is {winner}"
        self.in_progress = False
    
    def emojify(self):
        pass