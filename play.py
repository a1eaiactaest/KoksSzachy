#!/usr/bin/env python3

import os
import chess
import chess.svg
import time
from state import State

s = State() # plansza itd

from flask import Flask, Response, request
app = Flask(__name__) 

@app.route("/")
def hello():
  ret = open('index.html').read()
  return ret.replace('start', s.board.fen())

@app.route("/newgame")
def newgame():
  s.board.reset()
  response = app.response_class(
    response=s.board.fen(),
    status=200
  )
  return response

if __name__ == "__main__":
  app.run(debug=True)
