# Projekt Informatyka nr.1

Program został napisany aby implementował następujące transformacje (bez analizy dokładnościowej):      
    - XYZ (geocentryczne) -> BLH (elipsoidalne phi, lambda, h)     
    - BLH -> XYZ        
    - XYZ -> NEUp      
    - BL(GRS80, WGS84 -> 2000        
    - BL(GRS80, WGS84 -> 1992    
Ponadto program umożliwia podawanie argumentów przy wywołaniu za pomocą zmiennej sys.argv,     
potrafi transformować wiele współrzędnych zapisanych w pliku tekstowym przekazywanym do programu jako argument        
i tworzyć plik wynikowy, obsługuje przypadki gdy użytkownik wprowadzi niepoprawne wartości.       

## Spis treści    


1. [Wymagania systemowe]      
2. [Wiadome problemy]       




## Jak używać    

(Instrukcja dotycząca sposobu użycia projektu, wraz z przykładami kodu lub demonstracjami.) Przykładowe wykorzystanie programu:
Uwaga! Wszystkie wyniki są zwtracane poprzez stworzenie pliku wynikowego, nie ma  możliwości na wyrzucenie wyników na konsolę      
Oznaczenia:      
--xyz2plh (zamienia xyz na flh), należy podać współrzędne w kolejności x,y,z, w metrach, otrzymany wyniki to w kolejności phi, lambda, w stopniach jako liczba      dziesiętna i h w metrach       
--plh2xyz (zamiena flh na xyz) należy podać współrzędne w kolejności phi, lambda, w stopniach jako liczba dziesiętna i h w metrach otrzymany wyniki to w kolejności 
        x,y,z, w metrach,    
--xyz2neu (zamieniia xyz na NEU) należy podać współrzędne w kolejności x,y,z,x0,y0,z0 program zwróci współrzędne w kolejności N,E,U     
--bl2xy1992 (zamiania bl na Ukł. 1992) należy podać współrzędne w kolejności B, L, w stopniach jako liczba dziesiętna, metrach otrzymany wyniki to w kolejności x,y w metrach w układzie 1992      
--bl2xy2000 (zamiania bl na Ukł. 2000) należy podać współrzędne w kolejności B, L, w stopniach jako liczba dziesiętna, metrach otrzymany wyniki to w kolejności x,y w metrach w układzie 2000     
Do obsługi pliku TRZEBA podać po fladze transformacji: -f (należy wówczas podać nazwę pliku) lub -r (trzeba wpisać dane dla 1 transformacji)       
	-r (ręczne wpisywanie danych)    
	-f (dane z pliku)    
Przykład:   
dla flagi --xyz2plh:     
F:\[...]>python skrypty.py --xyz2plh -grs80 -r 3664940.5 1409153.59 5009571.17    
Wyniki transformacji otrzymamy wówczas w pliku: Results_xyz2plh:    
phi[deg],        lambda[deg],          H[m]      
[52.097272219326584, 21.03153333279777, 141.3986623911187]       
dla flagi --plh2xyz:      
F:\[...]>python skrypty.py --plh2xyz -grs80 -r 52.097272219326584 21.03153333279777 141.3986623911187    
Wyniki transformacji otrzymamy wówczas w pliku: Results_plh2xyz:     
x[m],        y[m],          z[m]     
3664940.5000059702,1409153.5900022953,5009571.17000816        
dla flagi --xyz2neu:      
F:\[...]>python skrypty.py --xyz2neu -grs80 -r 3664940.5 1409153.59 5009571.17 10 10 10        
Wyniki transformacji otrzymamy wówczas w pliku: Results_xyz2neu:      
n[m],        e[m],          u[m]    
[-20736.24295629],[-5.74501353],[6364956.74386206]    
dla flagi --bl2xy1992:       
F:\[...]>python skrypty.py --bl2xy1992 -grs80 -r 52.097272219326584 21.03153333279777  
Wyniki transformacji otrzymamy wówczas w pliku: Results_bl2xy1992:     
x[m],        y[m]    
472071.3410713384,639114.4909222787     
dla flagi --bl2xy2000:    
F:\[...]>python skrypty.py --bl2xy2000 -grs80 -r 52.097272219326584 21.03153333279777   
Wyniki transformacji otrzymamy wówczas w pliku: Results_bl2xy2000:       
x[m],        y[m]    
5773722.720951517,70502160.78324433  
Dla flagi -f i -wgs84:
F:[...]>python skrypty.py --xyz2plh -wgs84 -f wsp_xd.txt:
Zawartość test_file.txt
[Nagłowek


]
3664940.5,1409153.59,5009571.17
3664940.5,1409153.59,5009571.17    
3664940.5,1409153.59,5009571.17   
Wyniki transformacji otrzymamy wówczas w pliku: Results_xyz2plh:   
phi[deg],        lambda[deg],          H[m]
52.09727221841258,21.03153333279777,141.39859721064568
52.09727221841258,21.03153333279777,141.39859721064568
52.09727221841258,21.03153333279777,141.39859721064568
  
## Wymagania systemowe       

Do tego aby swobodnie korzystać z naszego projektu należy posiadać: system operacyjny windows 10, Python w wersji 3.11.8, a w samym oprogramowaniu trzeba mieć  
 pobrane biblioteki math oraz numpy.     

## Znane problemy     
Program nie obsługuje wyjątku w przypadku nadmiernej ilości danych w trybie -r     
Program obsługuje pliki tylko z 4-wierszowym nagłówkiem     
Program nie wymaga flagi elipsoidy(domyślnie grs80)    
Program wymaga podania x0,y0,z0 w przypadku każdej trójki współrzędnych w przypadku przesłania danych za pomocą pliku do flagi --xyz2neu      


