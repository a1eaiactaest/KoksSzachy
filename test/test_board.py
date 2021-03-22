import chess
import chess.pgn

board = chess.Board()
print(board.legal_moves)
print(board) # pokaz startowa pozycje
board.push_san("e4") # z mozliwych ruchow wybierz ten i go wykonaj
board.push_san("e5")
print('\n\n\n')
print(board) # pokaz pozycje figur po ruchach

print(board.legal_moves) # sprawdz czy mozliwe ruchy sie zmienily
print(board.pieces(chess.ROOK, chess.WHITE))
print(chess.pgn.Game())
