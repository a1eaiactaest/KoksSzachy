#!/usr/bin/env python3

import os
import chess
import chess.svg
import traceback
import time
from state import State

MAXVALUE = 10000
class Engine(object):
  values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 3,
        chess.QUEEN: 9,
        chess.KING: 0
        }

  position_table = {
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
  def __init__(self):
    self.reset()
    self.memory = {}

  def reset(self):
    self.count = 0

  def __call__(self, s):
    self.count += 1
    key = s.key()
    if key not in self.memory:
      self.memory[key] = self.eval(s)
    return self.memory[key]

  def eval(self, s):
    bd = s.board # plansza
    if bd.is_game_over():
      if bd.result() == "1-0":
        return MAXVALUE # wygrana
      elif bd.result() == "0-1":
        return -MAXVALUE # przegrana
      else:
        return 0 

    value = 0 
    piece_map = s.board.piece_map()
    for x in piece_map:
      tvalue = self.values


s = State() # plansza itd
v = Engine()

from flask import Flask, Response, request
app = Flask(__name__) 

@app.route("/")
def hello():
  ret = open('index.html').read()
  return ret.replace('start', s.board.fen()) # zastap pozycje w configu chassboard z obecnym fen stringiem

def ai_move(s, v):
  pass

@app.route("/move")
def move():
  if not s.board.is_game_over():
    move = request.args.get('move', default="") # przejmij wartosc move z index.html
    if move is not None and move != "":
      print("your move: ", move)
      try:
        s.board.push_san(move)
        ai_move(s, v) # zrobic funkcje ai
      except Exception:
        # https://docs.python.org/3/library/traceback.html#traceback.print_exc
        # https://docs.python.org/3/library/traceback.html#traceback.print_exception
        traceback.print_exc() # w skrocie, wypisz bledy ze stacka
      response = app.response_class(      
        response = s.board.fen(),
        status = 200
      )
      return response
  else:
    print("GAME OVER")
    response = app.response_class(
      response="game over",
      status=200
    )
    return response
  return hello() # caly czas czytaj index.html

@app.route("/move_cords")
def move_cords():
  if not s.board.is_game_over():
    source = int(request.args.get('from', default=''))
    target = int(request.args.get('to', default=''))
    promo = True if request.args.get('promo', default='') == 'true' else False

    move = s.bard.san(chess.Move(source, target, pormotion=chess.QUEEN if promo else None)) # auto promocja do hetmana

    if move is not Noen and move !='':
      print('your move: ', move)
      try:
        s.board.push_san(move)
        ai_move(s, V)
      except Exception:
        traceback.print_exc() # to samo co wczesniej
    response = app.response_class(
      response = s.board.fen(),
      status = 200
    )
    return response 

if __name__ == "__main__":
  s = State()
  app.run(debug=True)
