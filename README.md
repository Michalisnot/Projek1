# Projekt Informatyka nr.1

Program został napisany aby implementował następujące transformacje (bez analizy dokładnościowej):
    - XYZ (geocentryczne) -> BLH (elipsoidalne fi, lambda, h)
    - BLH -> XYZ 
    - XYZ -> NEUp 
    - BL(GRS80, WGS84, ew. Krasowski) -> 2000 
    - BL(GRS80, WGS84, ew. Krasowski) -> 1992 
Ponadto program umożliwia podawanie argumentów przy wywołaniu za pomocą zmiennej sys.argv,
potrafi transformować wiele współrzędnych zapisanych w pliku tekstowym przekazywanym do programu jako argument 
i tworzyć plik wynikowy, obsługuje przypadki gdy użytkownik wprowadzi niepoprawne wartości.

## Spis treści


1. [Wymagania systemowe]
2. [Wiadome problemy]




## Jak używać

(Instrukcja dotycząca sposobu użycia projektu, wraz z przykładami kodu lub demonstracjami.) Przykładowe wykorzystanie programu:

Oznaczenia: 
--xyz2plh (zamienia xyz na flh)
--plh2xyz (zamiena flh na xyz)
--xyz2neu (zamieniia xyz na NEU)
--bl2xy1992 (zamiania bl na Ukł. 1992)
--bl2xy2000 (zamiania bl na Ukł. 2000)
Do obsługi pliku TRZEBA podać po fladze transformacji: -f (należy wówczas podać nazwę pliku) lub -r (trzeba wpisać dane dla 1 transformacji)
	-r (ręczne wpisywanie danych)
	-f (dane z pliku)
Przykład:
F:\[...]>python skrypty.py --xyz2plh -r 3664940.5 1409153.59 5009571.17

Wyniki transformacji otrzymamy wówczas w pliku: Results_[nazwa_flagi]

## Wymagania systemowe

Do tego aby swobodnie korzystać z naszego projektu należy posiadać: system operacyjny windows 10, Python w wersji 3.11.8, a w samym oprogramowaniu trzeba mieć pobrane biblioteki math oraz numpy.

## Znane problemy
Program nie obsługuje wyjątku w przypadku nadmiernej ilości danych w trybie -r
Program obsługuje pliki tylko z 4-wierszowym nagłówkiem


