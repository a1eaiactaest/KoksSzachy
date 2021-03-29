# KoksSzachy

![logo-epic-big-daddy-by-smugas-hacker-epic-ok](https://user-images.githubusercontent.com/73793685/111052894-2bfdb300-8457-11eb-872a-bf4387a76ccb.png)

<sub>chess.com pls don't sue us, it's for fun</sub>

## Jak to działa?

Silnik KoksSzachów działa na bardzo prostej zasadzie:  

  * Pobranie pozycji [chessboard.js](https://chessboardjs.com/index.html) za pomocą [wpisywania w url](https://github.com/a1eaiactaest/KoksSzachy/blob/a9219e1f95fb4c26696c6a155eed329975d308c9/index.html#L114) [FEN](https://pl.wikipedia.org/wiki/Notacja_Forsytha-Edwardsa) stringów.
  
  * Rekreacja pozycji w bibliotece [python-chess](https://python-chess.readthedocs.io/), która umożliwia stworzenie listy możliwych ruchów i wiele innych, które przydadzą się w algorytmie Minimax.

  * Ewaluacja materiału. Działa ona na podstawie zliczania wartości wszystkich bierek na planszy. Wartości te są przedstawione w słowniku [```values```](https://github.com/a1eaiactaest/KoksSzachy/blob/3b1fd99b38b88ca2e1cfbf3fbed893bc4f20b5b0/state.py#L8).

  * Ewaluacja pozycji odtworzonej przez wspomnianą wcześniej bibliotekę przy pomocy FEN stringa. Jest ona robiona na podstawie słownika  [```positions```](https://github.com/a1eaiactaest/KoksSzachy/blob/3b1fd99b38b88ca2e1cfbf3fbed893bc4f20b5b0/state.py#L17).
    * Jak to działa? To bardzo proste - w słowniku dla każdej figury isnieje odpowiadający jej dwuwymiarowy array z liczbami całkowitymi. Array odpowiada prawdziwym rozmiarom szachownicy czyli 8x8.
      Weźmy dla przykładu array poświęcony [gońcowi](https://pl.wikipedia.org/wiki/Goniec_(szachy)). Specjalnie zaznaczona została notacja szachowa dla ułatwienia wizualizacji. 
      
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
  
  * Gdy białe - gracz, wykonają ruch, czarne - czyli komputer analizują pozycje i materiał zapisując obecną wartość ogólną. Po tym procesie uruchamiany jest algorytm [Minimax](https://github.com/a1eaiactaest/KoksSzachy/blob/a4c1d77ba4bf93270c03e2da8e7c17c50c55f1ef/state.py#L128), który analizuje przyszłe i możliwe posunięcia przeciwnika po wykonanym ruchu.
  W ten sposób algorytm ocenia, który ruch jest dla niego najlepszy. To na ile posunięć do przodu liczy jest kontrolowane przez zmienną ```depth+1```.   
  * Obliczone ruchy są zapisywane w odpowiedniej kolejności
  * Komputer wybiera pierwszy ruch z listy i go wykonuje.
  * Wszystko działa dopóki są możliwe ruchy. Nie działa to na podstawie pętli. 

  ## Minimax

  Minimax w KoksSzachach jest zooptymlizowany poprzez [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) oraz iterative deepening.

  Ciekawe artykuły i źródła na temat tych algorytmów: 

  - https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm   
  - https://www.cs.tau.ac.il/~wolf/papers/deepchess.pdf   
  - https://en.wikipedia.org/wiki/Evaluation_function#In_chess   
  - https://www.youtube.com/watch?v=JnXKZYFmGOg   
  - https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/   
  - https://towardsdatascience.com/how-a-chess-playing-computer-thinks-about-its-next-move-8f028bd0e7b1   
  - https://pl.wikipedia.org/wiki/Algorytm_alfa-beta   
  - https://www.chessprogramming.org/Iterative_Deepening  
 
## Jak zagrać?

Do odpalenia KoksSzachów potrzeba bibliotek zawartych w pliku [requirements.txt](https://github.com/a1eaiactaest/KoksSzachy/blob/main/requirements.txt)

```bash
git clone https://github.com/a1eaiactaest/KoksSzachy.git

cd KoksSzachy

# UNIX
pip3 install -r requirements.txt

./koksszachy/play.py 

# Windows
pip install -r requirements.txt

python koksszachy/play.py


# webserver na localhost:5000 (127.0.0.1:5000)
```

# TODO

* <s>Narysować boarda na stronie.</s>
* <s>Podpiąć chessboardjs pod python-chessa.</s>
* <s>Bardzo podstawowe działanie takie jak ograniczenie tylko do legalnych ruchów.</s>
* <s>Troche bardziej rozwinięte działanie.</s>
  * <s>Promocja</s>
  * <s>En passant</s>
  * <s>Roszada</s>
* <s>Ewaluacja dla poszczególnych bierek.</s>
* <s>Minimax</s>
  * <s>Alpha-beta</s>
* <s>Javascriptowe funkcje</s>
  * <s>takeBack()</s>
    * <s>implementacja</s>
    * <s>guziczek</s>
  * <s>newGame()</s>
    * <s>implementacja</s>
    * <s>guziczek</s>
* <s>Ktoś może sportować javascripta z index.html do oddzielnego pliku.</s>
* Frontend
* <s>Analysis Button, czyli klikamy zapisujemy notacje PGN i  przekierowywyuje nas w new tabie do API Lichessa z możliwością analizy naszej gry na podstawie PGN.</s>
* Kto wygrywa, aka wartość zbitych pionów z obu stron.
* <s>favicon i logo jakies do readme</s>
* wybór promocji, tzn. na jaką figurę chcemy wypromować piona
* wypisywanie pgn-u do textarea

### Zgodność

- [x] Windows 
- [ ] Linux
- [ ] MacOS

