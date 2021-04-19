#!/usr/bin/env python3
import chess
import math

class KoksSzachy:
  def __init__(self, fen):
    self.values = { # wartosci poszczegolnych figur podniesione do x*100
      chess.PAWN: 100, # pion
      chess.BISHOP: 300, # skoczek
      chess.KNIGHT: 300, # goniec
      chess.ROOK: 500, # wieza
      chess.QUEEN: 900, # hetman
      chess.KING: 99999 # krol
    }

    self.positions = positions = {
      # gdzie najlepiej stac przedstawione w arrayach 8x8 
      chess.PAWN: [ 
        0, 0, 0, 0, 0, 0, 0, 0,         # 8
        50, 50, 50, 50, 50, 50, 50, 50, # 7
        10, 10, 20, 30, 30, 20, 10, 10, # 6
        5, 5, 10, 25, 25, 10, 5, 5,     # 5
        0, 0, 0, 20, 20, 0, 0, 0,       # 4
        5, -5, -10, 0, 0, -10, -5, 5,   # 3
        5, 10, 10, -20, -20, 10, 10, 5, # 2
        0, 0, 0, 0, 0, 0, 0, 0          # 1
#       a  b  c  d  e  f  g  h 
      ],
      chess.BISHOP: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
      ],
      chess.KNIGHT: [
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
    
    self.board.set_fen(fen)
    self.nodes_explored = 0 # mozliwosci rozwiniecia gry
    self.board = chess.Board()

  def evaluate(self): # ewaluacja zmiennych takich jak material i pozycja
    # ocena materialu
    mval = 0
    for piece in self.values:
      mval += len(self.board.pieces(piece, chess.WHITE)) * self.values[piece]
      mval -= len(self.board.pieces(piece, chess.BLACK)) * self.values[piece]

    # ocena pozycji
    pval = 0
    for piece in self.values:
      w_squares = self.board.pieces(piece, chess.WHITE) # pola, na ktorych stoi var(piece)
      pval += len(w_squares) * self.values[piece]
      for square in w_squares:
        pval += self.positions[piece][-square]

      b_squares = self.board.pieces(piece, chess.BLACK)
      pval -= len(b_squares) * self.values[piece]
      for square in b_squares:
        pval -= self.positions[piece][square]
    
    return mval, pval
  
  # https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm 
  def mm(self, depth, move, maximizing): # ostatni artgument definiuje czy chcemy zwiekszac wynik
    if depth == 0: # ostatni poziom, ewaluuj tylko finalny efekt
      return move, self.evaluate()[1]

    if maximizing:
      # best move 
      bmove = None
      # best score 
      bscore = -math.inf # ujemne bo liczymy dla czarnych 
      moves = list(self.board.legal_moves)

      for move in moves:
        self.nodes_explored += 1
        self.board.push(move) # wykonaj ruch
        nmove, nscore = self.mm(depth - 1, move, False) # new move, new score, oblicz wartosc
        if nscore > bscore:
          bscore, bmove = nscore, move
        self.board.pop() # cofnij ruch 

      # zwroc najlepszy ruch wraz z jego wartoscia
      return bmove, bscore 

  
  def ab(self, negative_depth, positive_depth, move, a, b, move_hist, maximizing): #alpha-beta
    seq = [] # sekwencja ruchow
    if negative_depth == 0: # czy to ostatni poziom depth
      seq.append(move)
      return seq, self.evaluate()[1]
    
    moves = list(self.board.legal_moves)

    # wartosci "game over", jesli nie ma legalnych ruchow
    if not moves: # komputer sprawdza czy ma w zasiegu jakies checkm8 albo paty
      if self.board.is_checkmate():
        if self.board.result() == "1-0": # jesli checkm8 jest z korzyscia dla nas
          seq.append(move)
          return seq, 1000000
        elif self.board.result() == "0-1":
          seq.append(move)
          return seq, -1000000

    bmove = None
    bscore = -10000001 if maximizing else 10000001 

    # najnowszy obliczony najlepszy ruch na poczatek listy, powinno pomoc w obcinanu galezi z minimaxa
    if move_hist and len(move_hist) >= negative_depth:
      if move_hist[negative_depth-1] in moves:
        moves.insert(0, move_hist[negative_depth-1])
    
    if maximizing: # dla gracza zwiekszajacego, w tym przypadku czarny
      for move in moves:
        self.nodes_explored += 1
        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, False)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore > bscore:
          seq = nseq
          bscore, bmove = nscore, move

        # sprawdz czy nowy ruch jest lepszy od bety jesli jest, przerwij - to jest wlasnie alfa-beta pruning
        if nscore >= b:
          seq.append(bmove)
          return seq, bscore

        # update alfy
        if nscore > a:
          a = nscore

      # zwroc najlepszy wynik
      seq.append(bmove)
      return seq, bscore
          
    if not maximizing: # dla gracza zmniejszajacego to samo co powyżej tyle ze dla alfy
      for move in moves:
        self.nodes_explored += 1

        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, True)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore < bscore:
          seq = nseq
          bscore, bmove = nscore, move

        # lepszy niz alfa?
        if nscore <= a:
          seq.append(bmove)
          return seq, bscore

        # update bety
        if nscore < b:
          b = nscore

      # zwroc najlepszy wynik
      seq.append(bmove)
      return seq, bscore

    
  # Debugowanie -------

  # https://www.youtube.com/watch?v=JnXKZYFmGOg bardzo polecam koks filmik
  def iter_deep(self, depth): 
    tree, ret = self.ab(1, 0, None, -10000001, 10000001, None, self.board.turn)
    for i in range(2, depth):
      print("iteration nr.%s"%i)
      tree, ret = self.ab(i, 0, None, -10000001, 10000001, tree, self.board.turn)
    print("depth reached %s"%len(tree))
    return str(tree[-1])

  def run_mm(self, depth):
    maximizing = self.board.turn # tym kto chce zwiekszyc wartosc jest ten kogo jest ruch
    bmove, bscore = self.mm(depth, None, maximizing)
    return str(bmove) # zwroc najlepszy ruch obliczony przez minimaxa

  def run_ab(self, depth):
    maximizing = self.board.turn
    seq, bscore = self.ab(depth, 0, None, -10000001, 10000001, None, maximizing)
    for i in range(1, len(seq)):
      print("computers move: %s"%seq[-i])
    return str(seq[-1])

  def leaves(self): # mozliwosci ruchow
    my_nodes = self.nodes_explored
    self.nodes_explored = 0 # reset
    return my_nodes


