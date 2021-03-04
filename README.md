# KoksSzachy

## Jak to działa?

Silnik KoksSzachów działa na bardzo prostej zasadzie: 

  * Pobranie pozycji [chessboard.js](https://chessboardjs.com/index.html) za pomocą [wpisywania w url](https://github.com/a1eaiactaest/KoksSzachy/blob/a9219e1f95fb4c26696c6a155eed329975d308c9/index.html#L114) [FEN](https://pl.wikipedia.org/wiki/Notacja_Forsytha-Edwardsa) stringów.
  
  * Rekreacja pozycji w bibliotece [python-chess](https://python-chess.readthedocs.io/), która umożliwia stworzenie listy możliwych ruchów i wiele innych, ktore przydadzą się w algorytime Minimax.

  * Ewaluacja materiału. Działa ona na podstawie zliczania wartości wszystkich bierek na planszy. Wartości te są przedstawione w słowniku [```values```](https://github.com/a1eaiactaest/KoksSzachy/blob/3b1fd99b38b88ca2e1cfbf3fbed893bc4f20b5b0/state.py#L8).

  * Ewaluacja pozycji odtworzonej przez wspomnianą wcześniej bibliotekę przy pomocy FEN stringa. Jest ona robiona na podstawie słownika  [```positions```](https://github.com/a1eaiactaest/KoksSzachy/blob/3b1fd99b38b88ca2e1cfbf3fbed893bc4f20b5b0/state.py#L17).
    * Jak działa to działa? To bardzo proste. W słowniku dla każdej figury isnieje odpowiadający jej dwuwymiarowy rray z liczbami całkowitymi. Array odpowiada prawdziwym rozmiarom szachownicy czyli 8x8.
      Weźmy dla przykładu array poświęcony [gońcowi](https://pl.wikipedia.org/wiki/Goniec_(szachy)). Specjalnie zaznaczona została notacja szachowa dla ułatwienia wizualicaji. 
      
      ```python3
      
      {chess.BISHOP: [
        -50, -40, -30, -30, -30, -30, -40, -50, # 8
        -40, -20, 0, 0, 0, 0, -20, -40,         # 7
        -30, 0, 10, 15, 15, 10, 0, -30,         # 6
        -30, 5, 15, 20, 20, 15, 5, -30,         # 5
        -30, 0, 15, 20, 20, 15, 0, -30,         # 4
        -30, 5, 10, 15, 15, 10, 5, -30,         # 3
        -40, -20, 0, 5, 5, 0, -20, -40,         # 2
        -50, -40, -30, -30, -30, -30, -40, -50, # 1
      #  a    b    c    d    e    f    g    h
      ]}
      ```
      Łatwo zauważyć, że każdy z narożników szachownicy ma bardzo niskie wartości. To dlatego, że goniec stając na nich traci możliwość poruszania się po dwóch przekątnych tylko do jednej.  
      Zagłębiając się w wartości tej czy innych figur można dostrzec wiele innych wariantów.

      Arraye są przedstawione z perspektywy pierwszej osoby.
  
  * Gdy białe, gracz, wykonają ruch, czarne, komputer analizują pozycje i materiał zapisując obecna wartość ogólną. Po tym procesie uruchamiany jest algorytm [Minimax](https://github.com/a1eaiactaest/KoksSzachy/blob/a4c1d77ba4bf93270c03e2da8e7c17c50c55f1ef/state.py#L128), który analizuje przyszłe i możliwe posunięcia przeciwnika po wykonanym ruchu.
  W ten sposób algorytm ocenia, który ruch jest dla niego najlepszy. To na ile posunięć do przodu myśli jest kontrolowane przez zmienną ```depth+1```.

    Ciekawe artykuły i źródła na temat algorytmu:  
     * https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm
     * https://www.cs.tau.ac.il/~wolf/papers/deepchess.pdf
     * https://en.wikipedia.org/wiki/Evaluation_function#In_chess
     * https://www.youtube.com/watch?v=JnXKZYFmGOg
     * https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
     * https://towardsdatascience.com/how-a-chess-playing-computer-thinks-about-its-next-move-8f028bd0e7b1
     * https://pl.wikipedia.org/wiki/Algorytm_alfa-beta
     * https://www.chessprogramming.org/Iterative_Deepening

## Użycie

Do odpalenia KoksSzachów potrzeba bibliotek zawartych w pliku [requirements.txt](https://github.com/a1eaiactaest/KoksSzachy/blob/main/requirements.txt)

```bash
git clone https://github.com/a1eaiactaest/KoksSzachy.git

cd KoksSzachy

# UNIX
pip3 install -r requirements.txt

./play.py 

# Windows
pip install -r requirements.txt

python play.py


# webserver na localhost:5000 (127.0.0.1:5000)
```

# Plan

* <s>Narysować boarda na stronie.</s>
* <s>Podpiąć chessboardjs pod python-chessa.</s>
* <s>Bardzo podstawowe działanie takie jak ograniczenie tylko do legalnych ruchów.</s>
* Troche bardziej rozwinięte działanie.
  * <s>Promocja</s>
  * <s>En passant</s>
  * <s>Roszada</s>
* <s>Ewaluacja dla poszczególnych bierek.</s>
* Minimax
  * <s>Alpha-beta</s>
* Javascriptowe funkcje
  * takeBack()
    * implementacja
    * guziczek
  * newGame()
    * <s>implementacja</s>
    * <s>guziczek</s>

## TODO

* Ktoś może sportować javascripta z index.html do oddzielnego pliku.
* To co jest w planie nie zrobione

## docsy

***usunac gdy repo bedzie public***

Dla tych, którzy nie zapisali linku: [docsy](https://docs.google.com/document/d/1dUMeNNF1RS_UTGbHJZl_R7POuJ2NfcSvtbeZV_7FDjg/edit?usp=sharing)
