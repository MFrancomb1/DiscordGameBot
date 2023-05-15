from typing import Optional
import chess
from chess import STARTING_FEN
from stockfish import Stockfish
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
        self.in_progress = True
        self.engine = Stockfish(path="C:/Users/Michael/Documents/GitHub/DiscordGameBot/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
            
    def move(self, san: str):
            self.in_progress = True    
            #try to make move
            try:
                self.push_san(san)
                self.engine.set_fen_position(self.fen())
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

    def move_ai(self,):
        self.in_progress = True    
        #try to make move
        try:
            self.push_uci(b.engine.get_best_move())
            self.engine.set_fen_position(self.fen())
            return self.endgame() if self.is_game_over() else None                
        
        #handle illegal movces and other errors
        except (chess.IllegalMoveError, chess.InvalidMoveError, chess.AmbiguousMoveError) as e:
            return e


b = MyBoard()

while b.in_progress:
    print(b.unicode(invert_color=True))
    print(f"{'White' if b.turn else 'Black'} to move: ")
    if not b.turn:
        color = "Black"
        b.move_ai()
    else:
        color = "White"
        i = input()
        b.move(i)
    print(b.peek)        
    print(b.engine.get_best_move())