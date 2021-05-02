<p align="center">
  <img src="https://user-images.githubusercontent.com/73793685/111052894-2bfdb300-8457-11eb-872a-bf4387a76ccb.png"
</p>

---------------------------------------------------------------------------

<sub>chess.com pls don't sue us, it's for fun</sub>

![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![OSX](https://img.shields.io/badge/-OSX-grey?logo=apple)
![Windows 10](https://img.shields.io/badge/-Windows-grey?logo=windows)
![Python](https://img.shields.io/badge/Python-v3.7%5E-green?logo=python)
![PyPI](https://img.shields.io/pypi/v/KoksSzachy?color=blue&label=version)

## Instalacja i update

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

PROTIP: Jeśli debugujesz, to ci się przyda.
```
$ DEBUG=1 koksszachy --play
```
## Testujesz?

```
$ python3 -m pytest
```

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
  W ten sposób algorytm ocenia, który ruch jest dla niego najlepszy. To na ile posunięć do przodu liczy jest kontrolowane przez zmienną `depth`.   
  * Obliczone ruchy są zapisywane w odpowiedniej kolejności.
  * Komputer wybiera pierwszy ruch z listy i go wykonuje.
  * Wszystko działa dopóki są możliwe ruchy. Nie działa to na podstawie pętli. 

## Minimax
Ty, jako gracz, grasz białymi figurami. Minimax jest wywoływany przez gracza maksymalizującego wynik, w tym przypadku są to czarne figury, czyli komputer. 
Scenariusz, w którym grasz maksymalizujący wygrywa ma przypisaną warość nieskończoną. Idąc tym schematem przegrana dla gracza maksymalizującego ma wartość ujemnej nieskończoności.
  

  Minimax w KoksSzachach jest zooptymlizowany poprzez [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) oraz iterative deepening.

  Ciekawe artykuły i źródła na temat tych algorytmów: 

  - https://pl.wikipedia.org/wiki/Algorytm_min-max
  - https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm   
  - https://www.cs.tau.ac.il/~wolf/papers/deepchess.pdf   
  - https://en.wikipedia.org/wiki/Evaluation_function#In_chess   
  - https://www.chessprogramming.org/Simplified_Evaluation_Function
  - https://www.youtube.com/watch?v=JnXKZYFmGOg   
  - https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/   
  - https://towardsdatascience.com/how-a-chess-playing-computer-thinks-about-its-next-move-8f028bd0e7b1   
  - https://andreasstckl.medium.com/writing-a-chess-program-in-one-day-30daff4610ec
  - https://pl.wikipedia.org/wiki/Algorytm_alfa-beta   
  - https://www.chessprogramming.org/Iterative_Deepening  
  - https://www.youtube.com/watch?v=STjW3eH0Cik
  - https://www.chessprogramming.org/Branching_Factor
  - https://www.flyingmachinestudios.com/programming/minimax/ 

## Różnice depth w iterative deepeningu
Przeprowadziłem prosty eksperyment polegający na mierzeniu różnic czasowych i eksploracyjnych pomiędzy wartościami depth.
Najniższą możliwą wartością depth jest `1`. Zakładając, że mierzymy wszystkie wartości dla klasycznego i każdemu znango ruchu `e4`, wartość zmiennej `leaves_explored`, czyli jednym słowem możliwe rozwinięcia dla danej sytuacji, wynosi `20` rozwinięć.
I jeśli rzeczywiście popatrzymy na szachownicę, ta wartość się jak najbardziej zgadza.

<p align="center">
  <img src="docs/e4_nodes.png"
</p>

Jeśli porównamy wartości depth od `1-8` to zobaczymy prawdziwe różnice.

Chciałem tutaj dać piękny wykres matplotliba, ale nie udało mi się.

| Depth  | Leaves | Czas(s)|
| -------|:------:|------:|
| 1      | 20     | 0.004 | 
| 2      | 102    | 0.014 |
| 3      | 1233   | 0.086 | 
| 4      | 22884  | 1.563 | 
| 5      | 197047 | 13.232| 
| 6      | 768488 | 51.222|
| 7      | 12713930| 886.259| 
| 8      | 78510963| 5392.2| 


</br>

## Co w takim razie oznaczają te wszystkie pojęcia jak `depth`, `node`?

Przyjrzyjmy się zdjęciu tego drzewka:
<p align="center">
  <img = src="docs/tree.png">
  <sub><a href="https://www.google.com/url?sa=i&url=https%3A%2F%2Fphilippmuens.com%2Fminimax-and-mcts&psig=AOvVaw3ghcoLtGNtDNknITafgI5n&ust=1619953199544000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMiO74mqqPACFQAAAAAdAAAAABA1">źródło</a></sub>
</p>

W tym przypadku wartość `depth` będzie wynosiła `3`, ponieważ drzewko zagłębia się na 3 poziomy.

`Node`, to są punkty na drzewku, w KoksSzachach jest to legalny ruch. Istnieją dwa pojęcia na tą wartość:


- `leaf nodes`, `terminal nodes`

  Są to punkty, w których drzewko się kończy. W tym przypadku są to wszytkie punkty na samym dole przy `depth` równemu `3` i jest ich `8`.

- `root node`

  Na drzewku zawsze istnieje taki jeden punkt. W przypadku szachów jest to pozycja, w której obecnie jesteśmy. Od niego rozchodzi się całe drzewko.

- `internal nodes`, `non-leaf nodes`

  Są to wszystkie punkty na drzewku, nie licząc `leaf nodes`. Jak sama nazwa mowi są to punkty "wewnętrzne".


W algorytmie minimax istnieje takie pojęcie jak `branching factor`. Jest to średnia ilość dzieci każdego z punktów na danej głębokości. Na naszym przykładowym drzewku jest to `2`. Ponieważ każdy punkt ma przypisane 2 inne punkty. Oczywiście `branching factor` w szachach nie jest stały i się zmienia zależnie od pozycji oraz tego czy ucinamy pewne rozwinięcia z alpha-beta. Średnio wynosi on od 31 do 35. `Branching factor` można obliczyć w taki sposób:

> The average branching factor can be quickly calculated as the number of non-root nodes (the size of the tree, minus one; or the number of edges) divided by the number of non-leaf nodes (the number of nodes with children).

Zatem w przypadku przykładowego drzewka możemy tą formułę:

```python

>> # (len(tree)-1)/leaves
>> (15-1)/7
2.0

```

