#!/usr/bin/env python3
import chess
import math

MAXVAL = 10000

class KoksSzachy:
  values = { # centipawns
    chess.PAWN: 100, # pion
    chess.BISHOP: 300, # skoczek
    chess.KNIGHT: 300, # goniec
    chess.ROOK: 500, # wieza
    chess.QUEEN: 900, # hetman
    chess.KING: 0 # krol, zero bo nie da sie przejac
  }
  positions = {
    # gdzie najlepiej stac przedstawione w arrayach 8x8 
    # moze kiedys: https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
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
    chess.KNIGHT: [
      -50,-40,-30,-30,-30,-30,-40,-50,
      -40,-20,  0,  0,  0,  0,-20,-40,
      -30,  0, 10, 15, 15, 10,  0,-30,
      -30,  5, 15, 20, 20, 15,  5,-30,
      -30,  0, 15, 20, 20, 15,  0,-30,
      -30,  5, 10, 15, 15, 10,  5,-30,
      -40,-20,  0,  5,  5,  0,-20,-40,
      -50,-40,-30,-30,-30,-30,-40,-50 
    ],
    chess.BISHOP: [
      -20,-10,-10,-10,-10,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5, 10, 10,  5,  0,-10,
      -10,  5,  5, 10, 10,  5,  5,-10,
      -10,  0, 10, 10, 10, 10,  0,-10,
      -10, 10, 10, 10, 10, 10, 10,-10,
      -10,  5,  0,  0,  0,  0,  5,-10,
      -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
      ],
    chess.QUEEN: [
      -20,-10,-10, -5, -5,-10,-10,-20,
      -10,  0,  0,  0,  0,  0,  0,-10,
      -10,  0,  5,  5,  5,  5,  0,-10,
       -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
      -10,  5,  5,  5,  5,  5,  0,-10,
      -10,  0,  5,  0,  0,  0,  0,-10,
      -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -30,-40,-40,-50,-50,-40,-40,-30,
      -20,-30,-30,-40,-40,-30,-30,-20,
      -10,-20,-20,-20,-20,-20,-20,-10,
       20, 20,  0,  0,  0,  0, 20, 20,
       20, 30, 10,  0,  0, 10, 30, 20
    ]}

  """
  chess.KING w middle gamie
  -50,-40,-30,-20,-20,-30,-40,-50,
  -30,-20,-10,  0,  0,-10,-20,-30,
  -30,-10, 20, 30, 30, 20,-10,-30,
  -30,-10, 30, 40, 40, 30,-10,-30,
  -30,-10, 30, 40, 40, 30,-10,-30,
  -30,-10, 20, 30, 30, 20,-10,-30,
  -30,-30,  0,  0,  0,  0,-30,-30,
  -50,-30,-30,-30,-30,-30,-30,-50
  """

  def __init__(self, fen):
    self.game = chess.Board()
    self.game.set_fen(fen)
    self.leaves_explored = 0 # mozliwosci rozwiniecia gry

  def leaves(self): # mozliwosci ruchow
    my_nodes = self.leaves_explored
    self.leaves_explored = 0 # reset
    return my_nodes

  def evaluate(self): # ewaluacja zmiennych takich jak material i pozycja
    # ocena pozycji
    pval = 0
    for piece in self.values:
      w_squares = self.game.pieces(piece, chess.WHITE)  
      pval += len(w_squares) * self.values[piece]
      for square in w_squares:
        pval += self.positions[piece][-square]

      b_squares = self.game.pieces(piece, chess.BLACK)
      pval -= len(b_squares) * self.values[piece]
      for square in b_squares:
        pval -= self.positions[piece][square]
    
    return pval
  
  # https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm 
  def minmax(self, negative_depth, positive_depth, move, a, b, move_hist, ismax): #alpha-beta minimax
    seq = [] # sekwencja ruchow
    if negative_depth == 0: # czy to ostatni poziom depth
      seq.append(move)
      return seq, self.evaluate()
    
    moves = list(self.game.legal_moves) # mozliwe, legalne ruchy
    #print('moves before:',moves, 'moves length:',len(moves))

    # wartosci "game over", jesli nie ma legalnych ruchow
    if not moves: # jesli nie ma ruchow sprawdz czy sa zakonczenia gry
      if self.game.is_checkmate():
        if self.game.result() == '1-0': # sprawdza czy wynik jest korzystny
          seq.append(move)
          return seq, MAXVAL
        elif self.game.result() == '0-1':
          seq.append(move)
          return seq, -MAXVAL

    bmove = None
    bscore = -MAXVAL if ismax else MAXVAL

    # najnowszy obliczony najlepszy ruch na poczatek listy, powinno pomoc w obcinanu galezi z minimaxa
    if move_hist and len(move_hist) >= negative_depth:
      if move_hist[negative_depth-1] in moves:
        moves.insert(0, move_hist[negative_depth-1]) # do indexu 0
    
    if ismax: # dla gracza zwiekszajacego, raz to jest czarny raz bialy
      #print((moves))
      for move in moves:
        self.leaves_explored += 1
        self.game.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.minmax(negative_depth-1, positive_depth+1, move, a, b, move_hist, False) # jesli teraz max=True nastepnie musi byc False
        self.game.pop() # cofnij ruch

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
          
    if not ismax: # dla gracza zmniejszajacego to samo co powyżej tyle ze dla alfy
      #print((moves))
      for move in moves:
        self.leaves_explored += 1

        self.game.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.minmax(negative_depth-1, positive_depth+1, move, a, b, move_hist, True) # to samo co wyzej ok. 141
        self.game.pop() # cofnij ruch

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

  # https://www.youtube.com/watch?v=JnXKZYFmGOg bardzo polecam koks filmik
  def iter_deep(self, depth): 
    tree, ret = self.minmax(1, 0, None, -MAXVAL, MAXVAL, None, self.game.turn) # oblicz raz
    for i in range(2, depth):
      tree, ret = self.minmax(i, 0, None,-MAXVAL, MAXVAL, tree, self.game.turn) # licz w petli, ustaw {tree} jako move_hist
    if len(tree) == 1:
      #print('BOB')
      if not self.game.is_checkmate():
        return list(self.game.legal_moves)[0]
    return str(tree[-1])

if __name__ == "__main__":
  import sys
  #fen = "r1b2k1r/pp1pQppp/3P4/5P2/8/5N2/4KP1P/qN3B1R b - - 3 19"
  #fen = "r1b1k3/ppp1nQ2/4P1pN/2q5/8/6P1/5PBP/R3R1K1 b - - 2 28"
  v = KoksSzachy(sys.argv[1]) # bierz fen z argumentu
  m = v.iter_deep(5)
  print(m)
