# KoksSzachy

## Jak to działa?

Silnik KoksSzachów działa na bardzo prostej zasadzie: 

  * Pobranie pozycji [chessboard.js](https://chessboardjs.com/index.html) za pomocą [wpisywania w url](https://github.com/a1eaiactaest/KoksSzachy/blob/a9219e1f95fb4c26696c6a155eed329975d308c9/index.html#L114) [FEN](https://pl.wikipedia.org/wiki/Notacja_Forsytha-Edwardsa) stringów.
  
  * Rekreacja pozycji w bibliotece [python-chess](https://python-chess.readthedocs.io/), która umożliwia stworzenie listy możliwych ruchów i wiele innych, ktore przydadzą się w algorytime Minimax.

  

## Użycie

Do odpalenia KoksSzachów potrzeba pythonowych bibliotek w pliku [requirements.txt](https://github.com/a1eaiactaest/KoksSzachy/blob/main/requirements.txt)

```bash

pip3 install -r requirements.txt
# następnie...
./play.py # webserver na localhost:5000 (127.0.0.1:5000)

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
