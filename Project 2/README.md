# Projekt 2: Turniej szochowy

W ramach projektu należy napisać program w języku Python rozwiązujący
poniższe zadanie.

## Treść zadania[](#treść-zadania)

Jak każdego roku, pod koniec stycznia dni się wydłużają, żacy
Uniwersytetu Bitogrodu wytrwale zakuwają przed sesją, a fani gier
planszowych zacierają ręce, bo czeka na nich nie lada widowisko -
Międzynarodowe Drużynowe Mistrzostwa Szochów, które tym razem zawitają
do Królestwa Bajtycji. Najlepsi szochiści świata i okolic zbiorą się by
walczyć o ufundowaną z królewskiego skarbca nagrodę, a co ważniejsze -
laur mistrza owej cieszącej się w Bajtycji od lat wielką
popularnością gry.

Partia szochów odbywa się pomiedzy dwoma graczami wykonującymi na
przemian po jednym ruchu. Rozgrywka odbywa się na prostokątnej planszy
ustalonego rozmiaru, potencjalnie zawierającej dziury (niedostępne
pola). Figury poruszają się jak w szachach, ale są jednego koloru, więc
nie mogą się zbijać i każdy z graczy może poruszać każdą figurą. Pozycja
(ułożenie figur) która raz wystąpiła podczas rozgrywki, nie może zostać
powtórzona. Partię przegrywa ten z graczy, który jako pierwszy nie może
wykonać żadnego legalnego ruchu. Użyte figury i ich początkowe ułożenie
na planszy jest ustalane losowo przed rozgrywką.

Szochiści z drużyny Bajtycji są kompetentni i jeśli pozycja na to
pozwala, niechybnie znajdą drogę do zwycięstwa. Niestety w poprzedniej
edycji nieco zabrakło im szczęścia i po ubiegłorocznej przegranej z
zespołem Qbicji liczą na rewanż. Tym razem mają przewagę - jako
organizator turnieju, reprezentacja Bajtycji ma prawo w swoich partiach
wybierać, który z graczy pierwszy wykonuje ruch. Jako trener
reprezentacji Bajtycji, Twoim zadaniem jest na podstawie początkowego
ukladu planszy i figur zadecydować, czy Twój zawodnik powinien wykonać
ruch jako pierwszy, czy tez pozwolic na to zawodnikowi drużyny
przeciwnej.

### Dane wejściowe[](#dane-wejściowe)

Do zaimplementowanej funkcji przekazane zostaną następujące argumenty:

-   *N*, *M* - rozmiar planszy
-   lista niedostępnych pól
-   lista początkowych pozycji figur, zawierająca krotki postaci *(s, i,
    j)*, gdzie *s* to litera odpowiadająca rodzajowi figury
    (
    - `"k"` - król,
    - `"q"` - hetman,
    - `"b"` - goniec,
    - `"n"` - skoczek,
    - `"r"` - wieża),
    zaś *i*, *j*
    to jej pozycja na planszy. Pola planszy są indeksowane od *1*, tj.
    mają indeksy *1*, *2*, ..., *N* w poziomie oraz *1*, *2*,..., *M* w
    pionie.

Przykładowe wywołanie może wyglądać następująco (test *12*):

```py highlight
solve(2, 5,
  [(2, 1), (2, 3), (2, 4), (2, 5)],
  [("k", 2, 2)],
  ])
```

Funkcja *solve* powinna zwracać wartość *True* jeśli pierwszy gracz ma
zagwarantowane zwycięstwo przy poprawnej grze, oraz *False* w przeciwnym
wypadku.

Dla powyższych danych rozgrywka odbywa się na planszy *2* x *5* z
wyrzuconą większością prawej strony. Plansza i początkowe rozłożenie
figur przedstawia obrazek poniżej. W tej sytuacji gracz rozpoczynający
partię może zawsze osiągnąć zwyciestwo - wystarczy, że rozpocznie jednym
z dwóch ruchów zaznaczonych na zielono. W obu wypadkach pozostanie
możliwa do wykonania parzysta ilość ruchów, więc pierwszy gracz wykona
ruch jako ostatni i wygra grę. Jeśli pierwszy gracz wykona ruch
oznaczony na czerwono, to z podobnych powodów przegra, ale wyłącznie z
powodu własnego błędu - grając poprawnie zawsze jest w stanie wygrać
niezależnie od akcji przeciwnika, zatem funkcja *solve* powinna zwrócić
*True*.

![](https://github.com/user-attachments/assets/4cd8a6c5-4b4c-46e4-8224-d0e6d21cbf15)

### Przykłady[](#przykłady)

Rozważmy następujący stan początkowy (test *15*).

![](https://github.com/user-attachments/assets/772c006a-0fe8-4cd8-b899-3fe5889490ee)

W tej sytuacji również wygrywa gracz rozpoczynający - niezależnie od
tego, czy ruszy króla w lewo, czy w prawo, pozostałe ruchy są wymuszone
(w każdym następnym momencie istnieje tylko jeden dozwolony ruch) i jest
ich *6*, zatem gracz pierwszy wykona ostatni dozwolony ruch, np.
`1. k(1, 3) n(2, 3) 2. n(1, 1) k(2, 3) 3. k(3, 3) n(2, 3) 4. n(3, 1)` i drugi gracz nie ma żadnego dozwolonego ruchu.

Spójrzmy na jeszcze jeden przykład (test *14*).

![](https://github.com/user-attachments/assets/250c2a64-e68b-4d67-8e8d-399483784ba4)

W tej sytuacji wygraną zawsze jest w stanie osiągnąć drugi gracz. Po
każdym z dwóch możliwych pierwszych ruchów, tj. przesunięciu na *(2, 1)*
króla z *(1, 1)* albo z *(2, 2)*, istnieje tylko jeden możliwy ruch, i
po nim każdy ruch wraca do pozycji już wcześniej osiągniętej. W
szczególności po przesunięciu króla z *(1, 1)* na *(2, 1)* przez
pierwszego gracza i przesunięciu króla z *(2, 2)* na *(1, 1)* przez
drugiego gracza, gracz pierwszy nie może przesunąć króla z *(2, 1)* na
*(2, 2)*, ponieważ prowadzi to do powtorzenia pozycji początkowej -
wprawdzie króle są zamienione miejscami, ale figury tego samego typu
traktujemy jako nierozróżnialne, więc jest to ta sama pozycja.

## Instrukcja[](#instrukcja)

Infrastruktura do projektu dostępna jest w formie archiwum z plikami
źródłowymi w języku Python (link na dole). Szkielet rozwiązania znajduje
się w pliku *example.py* - importuje on funkcję
`runtests` z modułu
`data` i uruchamia ją, podając
swoją funkcję rozwiązującą jako argument. Przesyłane rozwiązania powinny
mieć postać analogicznego pliku. Przetestować rozwiązanie można
uruchamiając ów plik, np.

```py highlight
python3 example.py
```

Na wyjście standardowe wypisane zostaną informacje o rezultatach
poszczególnych testów, a także podsumowanie z ilością testów
zakończonych sukcesem i przybliżonym łącznym czasie obliczeń.

## Warunki techniczne[](#warunki-techniczne)

-   Program powinien być napisany w języku Python i działać z wersją
    3.12.1.
-   Program nie może wykorzystywać zewnętrznych bibliotek (biblioteka
    standardowa jest dopuszczalna)
