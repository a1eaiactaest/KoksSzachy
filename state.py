#!/usr/bin/env python3
import chess

MAXVAL = 1000000
class Valuator:
  def __init__(self, fen):
    self.board = chess.Board()
    self.values = { # wartosci poszczegolnych figur
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
    self.leaves_explored = 0 # konce gry, leaves(liscie) to konce "drzewka" minimaxu,

  def mateval(self): # ocena materialu
    val = 0
    #for piece in self.values:
    for piece in self.values:
      val += len(self.board.pieces(piece, chess.WHITE)) * self.values[piece]
      val -= len(self.board.pieces(piece, chess.BLACK)) * self.values[piece]

    return val

  def poseval(self): # ocena pozycji
    val  = 0
    """
    #for piece in self.values:
    for piece in range(1,7):
      # dla bialych
      ws = self.board.pieces(piece, chess.WHITE)
      val += len(ws) * self.values[piece]
      for square in ws: # for square in white squares
        val += self.positions[piece][-square]
      
      # dla czarnych 
      bs = self.board.pieces(piece, chess.BLACK)
      val -= len(bs) * self.values[piece]
      for square in bs:
        val -= self.positions[piece][square]
        """
    for piece in self.values: # (1,7)
      # eval white pieces
      w_squares = self.board.pieces(piece, chess.WHITE)
      val += len(w_squares) * self.values[piece]
      for square in w_squares:
        val += self.positions[piece][-square]

      b_squares = self.board.pieces(piece, chess.BLACK)
      val -= len(b_squares) * self.values[piece]
      for square in b_squares:
        val -= self.positions[piece][square]

    return val
  
  

  # https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm 
  def mm(self, depth, move, big): # MINIMAX :0
    if depth == 0:
      return move, self.poseval()

    if big:
      # best move 
      bmove = None
      # best score 
      bscore = -9999 # ujemne bo liczymy dla czarnych 
      moves = list(self.board.legal_moves)

      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # wykonaj ruch
        nmove, nscore = self.minimax(depth - 1, move, False) # new move, new score
        if nscore > bscore:
          bscore, bmove = nscore, move
        self.board.pop()

      # zwroc najlepszy ruch wraz z jego wartoscia
      return bmove, bscore 

  def ab(self, negative_depth, positive_depth, move, a, b, move_hist, big):
    seq = [] # ruchy, posortowane
    if negative_depth == 0:
      seq.append(move)
      return seq, self.poseval()
    
    moves = list(self.board.legal_moves)

    if not moves: # komputer sprawdza czy ma w zasiegu jakies checkm8 albo paty
      if self.board.is_checkmate():
        if self.board.result() == "1-0": # jesli checkm8 jest z korzyscia dla nas
          seq.append(move)
          return seq, 1000000
        elif self.board.result() == "0-1":
          seq.append(move)
          return seq, -1000000

    bmove = None
    bscore = -10000001 if big else 10000001 

    # najnowszy obliczony najlepszy ruch na poczatek listy, powinno pomoc w obcinanu galezi z minimaxa
    if move_hist and len(move_hist) >= negative_depth:
      if negative_depth == 4 and not self.board.turn:
        print(move_hist[negative_depth-1])
      if move_hist[negative_depth-1] in moves:
        moves.insert(0, move_hist[negative_depth-1])
    
    if big:
      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, False)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore > bscore:
          seq = nseq
          bscore, bmove = nscore, move

        # robimy to samo z betą 
        if nscore >= b:
          seq.append(bmove)
          return seq, bscore

        # update alfy
        if nscore > a:
          a = nscore

      # zwroc najlepszy wynik
      seq.append(bmove)
      return seq, bscore
          
    if not big: # to samo co powyżej tyle ze dla alfy
      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, True)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore < bscore:
          seq = nseq
          bscore, bmove = nscore, move

        # robimy to samo z alfa
        if nscore <= a:
          seq.append(bmove)
          return seq, bscore

        # update bety
        if nscore < b:
          b = nscore

      # zwroc najlepszy wynik
      seq.append(bmove)
      return seq, bscore

  def run_mm(self, depth):
    big = self.board.turn
    bmove, bscore = self.mm(depth, None, big)
    return str(bmove) # zwroc najlepszy ruch obliczony przez minimaxa

  def run_ab(self, depth):
    big = self.board.turn
    seq, bscore = self.ab(depth, 0, None, -10000001, 10000001, None, big)
    for i in range(1, len(seq)):
      print(f"computers move: {seq[-i]}")
    return str(seq[-1])

  def leaves(self): # zwroc 
    my_leaves = self.leaves_explored
    self.leaves_explored = 0 # reset
    return my_leaves

  def calc_moves(self): # oblicz wartosci ruchow i posegreguj je w tej kolejnosci
    moves = list(self.board.legal_moves)
    ret = []
    for move in moves:
      self.board.push(move)
      ret.append(self.mateval())
      self.board.pop()
    my_sorted = sorted(range(len(ret)), key=lambda x: ret[x], reverse=False)
    return [moves[i] for i in my_sorted]

  def timeout():
    pass

  # https://www.youtube.com/watch?v=JnXKZYFmGOg bardzo polecam koks filmik
  def iter_deep(self, depth): 
    tree, ret = self.ab(1, 0, None, -10000001, 10000001, None, self.board.turn)
    for i in range(2, depth+1):
      print(f"Iteration nr.{i}")
      tree, ret = self.ab(i, 0, None, -10000001, 10000001, tree, self.board.turn)
    print(f"depth reached {len(tree)}")
    return str(tree[-1])
    

if __name__ == "__main__":
  import time
  fen = "r2qkbr1/ppp1pppp/2n1b2n/8/8/5P2/PPPP2PP/RNB1KBNR b KQq - 0 6"
  v = Valuator(fen)
  start_time = time.time()
  print(v.iter_deep(4))
  print(v.leaves())
  print("Time taken:", time.time() - start_time)
