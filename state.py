#!/usr/bin/env python3
import chess

class State(object):
  def __init__(self, board=None):
    if board is None:
      self.board = chess.Board()
    else:
      self.board = board


  def key(self):
    return (self.board.board_fen(), self.board.turn, self.board.castling_rights, self.board.ep_square)    

  def edges(self):
    return list(self.board.legal_moves)


class Valuator(object):
  def __init__(self, fen):
    self.board = chess.Board()
    self.values = { # wartosci poszczegolnych figur
      chess.PAWN: 1,
      chess.KNIGHT: 3,
      chess.BISHOP: 3,
      chess.ROOK: 5,
      chess.QUEEN: 9,
      chess.KING: 99999
    }

    self.positions = positions = {
			# gdzie najlepiej stac
     	chess.PAWN: [ 
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
        ],
        chess.KNIGHT: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -20, -10, -10, -10, -10, -10, -10, 20
        ],
        chess.BISHOP: [
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
    self.leaves_explored = 0

  def poseval(self): # ocena pozycji
    val  = 0

    for piece in self.values:
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

    return val

  def mm(self, depth, move, big): # MINIMAX :0
    if depth == 0:
        return node, self.position_eval()
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
    isort = [] # ruchy, posortowane
    if negative_depth == 0:
      isort.append(move)
      return isort, self.poseval()
    
    moves = list(self.board.legal_moves)

    if not moves: # komputer sprawdza czy ma w zasiegu jakies checkm8 albo paty
      if self.board.is_checkmate():
        if self.board.result() == "1-0": # jesli checkm8 jest z korzyscia dla nas
          isort.append(move)
          return isort, 1000000
        elif self.board.result() == "0-1":
          isort.append(move)
          return isort, -1000000

    bmove = None
    bscore = -10000001 if big else 10000001 

    # najnowszy obliczony najlepszy ruch na poczatek listy, powinno pomoc w obcinanu galezi z minimaxa
    if move_hist and len(move_hist) >= negative_depth:
      if negative_depth == 4 and not self.board.turn:
        print(move_hist[negative_depth-1])
      if move_hist[negative_depth-1] in moves:
        moves.insert(0, move_hist[negative_depth-1]
    
    if big:
      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, False)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore > bscore:
          isort = nseq
          bscore, bmove = nscore, move

        # robimy to samo z betą 
        if nscore >= b:
          isort.append(bmove)
          return isort, bmove

        # update alfy
        if nscore > a:
          a = nscore

      # zwroc najlepszy wynik
      isort.append.append(bmove)
      return isort, bscore
          
    if not big: # to samo co powyżej tyle ze dla alfy
      for move in moves:
        self.leaves_explored += 1
        self.board.push(move) # zrob ruch
        # oblicz, zapisz w var(nseq)
        nseq, nscore = self.ab(negative_depth-1, positive_depth+1, move, a, b, move_hist, True)
        self.board.pop() # cofnij ruch

        # sprawdz czy odkryty ruch jest lepszy niz poprzedni, jesli tak zamien 
        if nscore < bscore:
          isort = nseq
          bscore, bmove = nscore, move

        # robimy to samo z alfa
        if nscore <= a:
          isort.append(bmove)
          return isort, bmove

        # update bety
        if nscore < b:
          b = nscore

      # zwroc najlepszy wynik
      isort.append.append(bmove)
      return isort, bscore

  def move_selection(depth):
    pass

if __name__ == "__main__":
  s = State()
