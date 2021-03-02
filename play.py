#!/usr/bin/env python3
from state import *

from flask import Flask, Response, request, render_template
app = Flask(__name__) 



@app.route("/")
def hello():
  ret = open('index.html').read()
  #return ret.replace('start', s.board.fen()) # zastap pozycje w configu chassboard z obecnym fen stringiem
  return ret

@app.route("/move/<int:depth>/<path:fen>/") # routuj fen i depth do url tak zeby mozna bylo requestowac
def calc_move(depth, fen):
  print(f'depth: {depth}')
  engine = Valuator(fen)
  move = engine.iter_deep(depth - 1)
  if move is None:
    print('Game over')
  else: 
    print(f'computer moves: {move}\n')
    return move


if __name__ == "__main__":
  app.run(debug=True)
