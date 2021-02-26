#!/usr/bin/env python3
import chess

class State(object):
  def __init__(self, board=None):
    if board is None:
      self.board = chess.Board()
    else:
      self.board = board

  def key(self):
    
  def edges(self):
    return list(self.board.legal_moves)

if __name__ == "__main__":
  s = State()
