#!/usr/bin/env python3

import os
import chess
import chess.svg
import time

from flask import Flask, render_template
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
  #return render_template("index.html")
  return app.send.static_url_path='index.html')

@app.route("/newgame")
def newgame():
  pass

if __name__ == "__main__":
  app.run(debug=True)
