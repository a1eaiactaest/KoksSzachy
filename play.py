#!/usr/bin/env python3
import sys
import chess
from engine import *

from flask import Flask, Response, request, render_template, url_for, jsonify
app = Flask(__name__) 

@app.route("/")
def hello():
  ret = open('index.html').read()
  return ret

@app.route("/info/<int:depth>/<path:fen>/") # routuj fen i depth do url tak zeby mozna bylo requestowac
def calc_move(depth, fen):
  print(f'depth: {depth}')
  engine = KoksSzachy(fen)
  move = engine.iter_deep(depth - 1)
  if move is None:
    print('Game over')
  else: 
    print(f'computer moves: {move}\n')
    return move

@app.route("/analysis", methods=['POST'])
def get_data():
  if request.method == 'POST':
    pgn = request.get_json()
    print(pgn['content'])
    import webbrowser
    from bs4 import BeautifulSoup as bs
    url = 'https://lichess.org/paste'
    webbrowser.open_new_tab(url)
    return '', 200 # musi cos zwracac
 
if __name__ == "__main__":
  app.run(debug=True)
