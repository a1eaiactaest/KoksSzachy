#!/usr/bin/env python3
import chess

class State(object):
  def __init__(self, board=None):
    self.board = chess.Board() 
  def edges(self):
    return list(self.board.legal_moves)

if __name__ == "__main__":
  s = State()
