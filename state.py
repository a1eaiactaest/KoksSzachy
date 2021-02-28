#!/usr/bin/env python3
import chess

class State(object):
  def __init__(self, board=None):
    if board is None:
      self.board = chess.Board()
    else:
      self.board = board


  def key(self):
    return (self.board.board_fen(), self.board.turn, self.board.castling_rights, self.board.ep_square)    

  def edges(self):
    return list(self.board.legal_moves)


class Valuator(object):
  def __init__(self, fen):
    self.board = chess.Board()
    self.values = { # wartosci poszczegolnych figur
      chess.PAWN: 1,
      chess.KNIGHT: 3,
      chess.BISHOP: 3,
      chess.ROOK: 5,
      chess.QUEEN: 9,
      chess.KING: 99999
    }

    self.positions = positions = {
			# gdzie najlepiej stac
     	chess.PAWN: [ 
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
        ],
        chess.KNIGHT: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -20, -10, -10, -10, -10, -10, -10, 20
        ],
        chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
        ],
        chess.ROOK: [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0
        ],
        chess.QUEEN: [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
        ],
        chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20
        ]
    }
    
    self.board.set_fen(fen)
    self.leaves_explored = 0

  def poseval(self): # ocena pozycji
    ret = 0

    for piece in self.values:
      # dla bialych
      ws = self.board.pieces(piece, chess.WHITE)
      ret += len(ws) * self.values[piece]
      for square in ws: # for square in white squares
        ret += self.positions[piece][-square]
      
      # dla czarnych 
      bs = self.board.pieces(piece, chess.BLACK)
      ret -= len(bs) * self.values[piece]
      for square in bs:
        ret -= self.positions[piece][square]

    return ret

  def mm(self, depth, move, big): # MINIMAX :0
    if depth == 0:
        return node, self.position_eval()
    if big:
      # best move 
      bmove = None
      # best score 
      bscore = -9999 # ujemne bo liczymy dla czarnych 
      moves = list(self.board.legal_moves)

      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # wykonaj ruch
        nmove, nscore = self.minimax(depth - 1, move, False) # new move, new score
        if nscore > bscore:
          bscore, k
           

  def move_selection(depth):
    pass

if __name__ == "__main__":
  s = State()
