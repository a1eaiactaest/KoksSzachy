# ![KoksSzachy](https://user-images.githubusercontent.com/73793685/111052894-2bfdb300-8457-11eb-872a-bf4387a76ccb.png)

<sub>chess.com pls don't sue us, it's for fun</sub>

![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![OSX](https://img.shields.io/badge/-OSX-grey?logo=apple)
![Windows 10](https://img.shields.io/badge/-Windows-grey?logo=windows)
![Python](https://img.shields.io/badge/Python-v3.7%5E-green?logo=python)
![PyPI](https://img.shields.io/pypi/v/KoksSzachy?color=blue&label=version)

## Jak to działa?

Silnik KoksSzachów działa na bardzo prostej zasadzie:  

  * Pobranie pozycji [chessboard.js](https://chessboardjs.com/index.html) za pomocą [wpisywania w url](https://github.com/a1eaiactaest/KoksSzachy/blob/a9219e1f95fb4c26696c6a155eed329975d308c9/index.html#L114) [FEN](https://pl.wikipedia.org/wiki/Notacja_Forsytha-Edwardsa) stringów.
  
  * Rekreacja pozycji w bibliotece [python-chess](https://python-chess.readthedocs.io/), która umożliwia stworzenie listy możliwych ruchów i wiele innych, które przydadzą się w algorytmie Minimax.

  * Ewaluacja materiału. Działa ona na podstawie zliczania wartości wszystkich bierek na planszy. Wartości te są przedstawione w słowniku [```values```](https://github.com/a1eaiactaest/KoksSzachy/blob/e29ba3a688426a214114697e039a9b4f6cd24bd2/koksszachy/engine.py#L8).

  * Ewaluacja pozycji odtworzonej przez wspomnianą wcześniej bibliotekę przy pomocy FEN stringa. Jest ona robiona na podstawie słownika  [```positions```](https://github.com/a1eaiactaest/KoksSzachy/blob/e29ba3a688426a214114697e039a9b4f6cd24bd2/koksszachy/engine.py#L17).
    * Jak to działa? To bardzo proste - w słowniku dla każdej figury istnieje odpowiadający jej dwuwymiarowy array z liczbami całkowitymi. Array odpowiada prawdziwym rozmiarom szachownicy czyli 8x8.
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
  
  * Gdy białe - gracz, wykonają ruch, czarne - czyli komputer analizują pozycje i materiał zapisując obecną wartość ogólną. Po tym procesie uruchamiany jest algorytm [Minimax](https://pl.wikipedia.org/wiki/Algorytm_min-max), który analizuje przyszłe i możliwe posunięcia przeciwnika po wykonanym ruchu.
  W ten sposób algorytm ocenia, który ruch jest dla niego najlepszy. To na ile posunięć do przodu liczy jest kontrolowane przez zmienną ```depth+1```.   
  * Obliczone ruchy są zapisywane w odpowiedniej kolejności.
  * Komputer wybiera pierwszy ruch z listy i go wykonuje.
  * Wszystko działa dopóki są możliwe ruchy. Nie działa to na podstawie pętli. 

## Minimax
Ty, jako gracz, grasz białymi figurami. Minimax jest wywoływany przez gracza maksymalizującego wynik, w tym przypadku są to czarne figury, czyli komputer. 
Scenariusz, w którym grasz maksymalizujący wygrywa ma przypisaną warość nieskończoną. Idąc tym schematem przegrana dla gracza maksymalizującego ma wartość ujemnej nieskończoności.
  

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
 
## Różnice depth w iterative deepeningu
Przeprowadziłem prosty test polegający na mierzeniu różnic czasowych i eksploracyjnych pomiędzy wartościami depth.
Najniższą możliwą wartością depth jest `1`. Zakładając, że mierzymy wszystkie wartości dla klasycznego i każdemu znango ruchu `e4`, wartość zmiennej `nodes_explored`, czyli jednym słowem możliwe rozwinięcia dla danej sytuacji, wynosi `20` rozwinięć.
I jeśli rzeczywiście popatrzymy na szachownicę, ta wartość się jak najbardziej zgadza.

<p align="center">
  <img src="docs/e4_nodes.png"
</p>

Jeśli porównamy wartości depth od `1-8` to zobaczymy prawdziwe różnice.

Chciałem tutaj dać piękny wykres matplotliba, ale nie udało mi się.

| Depth  | Nodes  | Czas(s)|
| -------|:------:|------:|
| 1      | 20     | 0.004 | 
| 2      | 102    | 0.014 |
| 3      | 1233   | 0.086 | 
| 4      | 22884  | 1.563 | 
| 5      | 197047 | 13.232| 
| 6      | 768488 | 51.222|
| 7      | 12713930| 886.259| 
| 8      | 78510963| 5392.2| 




# Instalacja lub update

## Wymagania

Do zainstalowania KoksSzachów wymagany jest pobrany `Python 3.7` lub nowszy oraz `pip` odpowiadjący wersji Pythona, czyli pythonowy package manager.

### Unix

```bash
$ pip3 install koksszachy --upgrade
```

### Windows

```bash
$ pip install koksszachy --upgrade
```

## Jak zagrać?

```bash
$ koksszachy -p

# lub

$ koksszachy --play
```

### Zgodność

- [x] Windows 
- [x] Linux
- [x] MacOS

