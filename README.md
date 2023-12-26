
# Matlab to C++ compiler


Wymagania:
1. Python
2. ply==3.11

Instrukcja obsługi:
1. Wejść do folderu z plkiem `main.py`
2. Zainstalować wymagane biblioteki: `pip install -r requirements.txt`
3. Uruchomić program poleceniem: `python3 main.py "nazwa pliku matlaba"` (przy braku argumentu zostanie wykorzystany plik `input1.m`)
4. Wynik zostanie zapisany do pliku `output.cpp`
5. Poprawność działania wyniku można sprawdzić wykonując polecenie: `g++ output.cpp  && ./a.out`
