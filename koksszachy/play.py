#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import chess
import webbrowser
import time
from koksszachy.engine import KoksSzachy
from flask import Flask, Response, request, render_template, url_for, jsonify
app = Flask(__name__) 

arguments = [
    '-h',
    '--help',
    '-p',
    '--play',
    '-d',
    '--docs'
]

def my_help():
  mes = '''
  użycie: koksszachy [OPTION]
  Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! <3
  Po więcej informacji odwiedź: https://github.com/a1eaiactaest/KoksSzachy
  argumenty:
  -h, --help    pokaż tą wiadomość
  -p, --play    zagraj w swoje ulubione szachy! 
  -d, --docs    przeczytaj dokumentację
  '''
  print(mes)

@app.route("/")
def hello():
  r = render_template('index.html') # musialem uzyc render_template, inaczej ciezko by dzialalo z packagowaniem
  return r

@app.route("/info/<int:depth>/<path:fen>/") # routuj fen i depth do url tak zeby mozna bylo requestowac
def calc_move(depth, fen):
  start = time.time()
  print('\ndepth: %s'%depth)
  engine = KoksSzachy(fen)
  move = engine.iter_deep(depth)
  nodes_explored = engine.leaves()
  val = engine.evaluate()
  end = time.time()
  if move is None:
    print('Game over')
    return 0
  else: 
    #print('computer moves: %s'%move)
    print('nodes explored: %s '% nodes_explored)
    print('eval: %s'% str(val))
    print('fen: %s'% fen)
    print('time elapsed: %s'% (end-start))
    print(engine.board,'\n')
    return move


@app.route("/analysis", methods=['POST'])
def get_data():
  if request.method == 'POST':
    import json
    import urllib
    content = request.get_json() # {"content": ["1. f3 e5 2. g4 Qh4#"]}
    pgn = content['content'][0] # ['1. f3 e5 2. g4 Qh4#']
    pgn = {"pgn": pgn, "pgnFile": "", "analyse":"true"} # dwa ostatnie tak profilaktycznie
    url = 'https://lichess.org/paste?%s'%urllib.parse.urlencode(pgn) # encode url zeby wstawic dane automatycznie
    print(url)
    webbrowser.open_new_tab(url)
    return '', 200 # zwroc odpowiedni kod
 
def main(argument="", show=True):
  try:
    if argument == "":
      argument = sys.argv[1]
    if argument not in arguments:
      print('\n  Wystąpił problem z rozpoznaniem argumentu %s' % argument)
      my_help()
      return 0
    else:
      if argument == '--play' or argument == '-p':
        if show == False:
          print('DEBUG OFF')
          import os
          os.environ['WERKZEUG_RUN_MAIN'] = 'true'
          app.run(debug=False)
        else:
          webbrowser.open_new_tab('http://localhost:5000')
          app.run(debug=False)
      if argument == '--docs' or argument == '-d':
        webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')
        return 0
      if argument == '--help' or argument == '-h':
        my_help()
        return 0
  except IndexError:
    my_help()
    return 0


if __name__ == "__main__":
  try:
    argument = sys.argv[1]
    if argument not in arguments:
      print('\n  Wystąpił problem z rozpoznaniem argumentu "%s"' % argument)
      my_help()
    else:
      if argument == '--play' or argument == '-p':
        webbrowser.open_new_tab('http://localhost:5000')
        app.run(debug=False)
      if argument == '--docs' or argument == '-d':
        webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')
      if argument == '--help' or argument == '-h':
        my_help()
        print('argument: %s'%arugment)
  except IndexError:
    app.run(debug=True)

