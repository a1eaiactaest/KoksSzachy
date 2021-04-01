#!/usr/bin/env python3

import sys
import chess
import webbrowser
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
  użycie: koksszachy [ARGUMENT]
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
  r = render_template('index.html')
  return r

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
    return '', 200 # zwroc odpowiedni kod
 
def main():
  try:
    argument = sys.argv[1]
    if argument not in arguments:
      print(f'\n  Wystąpił problem z rozpoznaniem argumentu {argument}')
      my_help()
      return 0
    else:
      if argument == '--play' or argument == '-p':
        webbrowser.open_new_tab('http://localhost:5000')
        app.run(debug=True)
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
  app.run(debug=True)


