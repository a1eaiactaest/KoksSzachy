#!/usr/bin/env python3

import chess
from engine import *
import os.path
import webbrowser

from flask import Flask, Response, request, render_template, url_for, jsonify
app = Flask(__name__) 

# for importing
def run():
  webbrowser.open_new_tab('http://localhost:5000')
  app.run(debug=True)

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
    import json
    import urllib
    content = request.get_json() # {"content": ["1. f3 e5 2. g4 Qh4#"]}
    pgn = content['content'][0] # ['1. f3 e5 2. g4 Qh4#']
    pgn = {"pgn": pgn, "pgnFile": "", "analyse":"true"} # dwa ostatnie tak profilaktycznie
    url = f'https://lichess.org/paste?{urllib.parse.urlencode(pgn)}' # encode url zeby wstawic dane automatycznie
    print(url)
    webbrowser.open_new_tab(url)
    return '', 200 # musi cos zwracac

def my_help():
  mes = '''
  użycie: koksszachy [ARGUMENT]

  Lubisz grać w szachy? Podobał ci się chess.com lub lichess? W takim razie pokochasz KoksSzachy! <3
  Po więcej informacji odwiedź: https://github.com/a1eaiactaest/KoksSzachy

  argumenty:
  -h, --help    pokaż tą wiadomość
  -p, --play    zagraj w swoje ulubione szachy! 
  -d, --docs    przeczytaj dokumentację

  '''
  print(mes)

def main():
  import sys
  try: 
    argument = sys.argv[1]
    if argument == '--play' or argument == '-p':
      run()

    if argument == '--docs' or argument == '-d':
      import webbrowser
      webbrowser.open_new_tab('https://github.com/a1eaiactaest/KoksSzachy/blob/main/README.md')

    if argument == '--help' or argument == '-h':
      my_help()

  except Exception:
    my_help()
    print("error: ", sys.exc_info()[0])
    raise

if __name__ == '__main__':
  main()
