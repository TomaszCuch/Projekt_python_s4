class Bank:
    def __init__(self, nazwa_banku):
        self.nazwa_banku = nazwa_banku

    def zmien_nazwe_banku(self, nowa_nazwa):
        self.nazwa_banku = nowa_nazwa


class KontoBankowe(Bank):
    def __init__(self, nazwa_banku, numer_konta, wlasciciel, saldo):
        super().__init__(nazwa_banku)
        self.numer_konta = numer_konta
        self.wlasciciel = wlasciciel
        self.__saldo = saldo

    @staticmethod
    def czy_wplata(kwota):
        return kwota > 0

    @staticmethod
    def czy_wyplata(saldo, kwota):
        return 0 < kwota <= saldo and saldo > 0

    @staticmethod
    def czy_transfer(saldo, kwota):
        return 0 < kwota <= saldo and saldo > 0

    def wplata(self, kwota):
        if self.czy_wplata(kwota):
            self.__saldo = self.__saldo + kwota
        else:
            raise ValueError("Kwota wpłaty musi być większa od 0.\n")

    def wyplata(self, kwota):
        if self.czy_wyplata(self.__saldo, kwota):
            self.__saldo = self.__saldo - kwota
        else:
            raise ValueError("Zbyt mało środków na koncie.\n")

    def transfer(self, konto_docelowe, kwota):
        if self.czy_transfer(self.__saldo, kwota):
            self.__saldo = self.__saldo - kwota
            konto_docelowe.zmien_saldo(konto_docelowe.pobierz_saldo() + kwota)
        else:
            raise ValueError("Zbyt mało środków na koncie.\n")

    def pokaz_saldo(self):
        print(f'{self.__saldo:.2f}')

    def pobierz_saldo(self):
        return self.__saldo

    def zmien_numer_konta(self, nowy_numer_konta):
        self.numer_konta = nowy_numer_konta

    def zmien_wlasciciela(self, nowy_wlasciciel):
        self.wlasciciel = nowy_wlasciciel

    def zmien_saldo(self, nowe_saldo):
        self.__saldo = nowe_saldo


class KontoOszczednosciowe(KontoBankowe):
    def __init__(self, nazwa_banku, numer_konta, wlasciciel, saldo, oprocentowanie):
        super().__init__(nazwa_banku, numer_konta, wlasciciel, saldo)
        self.oprocentowanie = oprocentowanie

    def zmien_oprocentowanie(self, nowe_oprocentowanie):
        self.oprocentowanie = nowe_oprocentowanie

    def nalicz_odsetki(self):
        odsetki = round(self.pobierz_saldo() * (self.oprocentowanie / 100), 2)
        self.zmien_saldo(self.pobierz_saldo() + odsetki)
        print(f"Naliczono odsetki dla {self.numer_konta}: {odsetki:.2f} [PLN].\n")


# Lista i słownik dla banków
lista_bankow_nazwa_banku = []
keys_bankow = ['nazwa banku']
slownik_bankow = dict.fromkeys(keys_bankow)
# Lista obiektów klasy Bank
lista_obiektow_bank = []

# Lista i słowniki dla kont bankowych
lista_kb_nazwa_banku = []
lista_kb_numer_konta = []
lista_kb_wlasciciel = []
lista_kb_saldo = []
keys_kb = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]']
slownik_kont_bankowych = dict.fromkeys(keys_kb)
# Lista obiektów klasy KontoBankowe
lista_obiektow_konto_bankowe = []

# Lista i słowniki dla kont oszczędnościowych
lista_ko_nazwa_banku = []
lista_ko_numer_konta = []
lista_ko_wlasciciel = []
lista_ko_saldo = []
lista_ko_oprocentowanie = []
keys_ko = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]', 'oprocentowanie [%]']
slownik_kont_oszczednosciowych = dict.fromkeys(keys_ko)
# Lista obiektów klasy KontoOszczednosciowe
lista_obiektow_konto_oszczednosciowe = []


# Zewnętrzne funkcje sprawdzające poprawność inputów użytkownika
def sprawdz_liczbe(x, max):
    if (0 <= x <= max):
        return True
    else:
        print('Liczba całkowita spoza zakresu.\n')


def sprawdz_nazwe_banku(tekst):
    if tekst and not tekst.startswith(' ') and all(znak.isalpha() or znak.isspace() for znak in tekst):
        return True
    else:
        print('Nazwa banku nie może zaczynać się od spacji i musi składać się z liter. Spróbuj ponownie.\n')


def sprawdz_unikalna_nazwe_banku(nazwa):
    nazwa_mala = nazwa.lower()
    lista_mala = [el.lower() for el in lista_bankow_nazwa_banku]
    if nazwa_mala not in lista_mala:
        return True
    else:
        print(f'Bank o nazwie "{nazwa}" już istnieje. Spróbuj ponownie.\n')
        return False


def sprawdz_nr_konta(numer):
    if numer.isdigit() and len(numer) == 26:
        return True
    else:
        print('Numer konta musi składać się z dokładnie 26 cyfr. Spróbuj ponownie.\n')


def sprawdz_unikalny_nr_konta_bankowego(numer):
    if (numer not in lista_kb_numer_konta):
        return True
    else:
        print(f'Konto bankowe o numerze "{numer}" już istnieje. Spróbuj ponownie.\n')


def sprawdz_unikalny_nr_konta_oszczednosciowego(numer):
    if (numer not in lista_ko_numer_konta):
        return True
    else:
        print(f'Konto oszczędnościowe o numerze "{numer}" już istnieje. Spróbuj ponownie.\n')


def sprawdz_nazwe_wlasciciela(tekst):
    if tekst and not tekst.startswith(' ') and all(znak.isalpha() or znak.isspace() for znak in tekst):
        return True
    else:
        print('Nazwa właściciela nie może zaczynać się od spacji i musi składać się z liter. Spróbuj ponownie.\n')


import re


def czy_poprawne_saldo(tekst):
    wzorzec = r'^\d+(\.\d{1,2})?$'
    return re.fullmatch(wzorzec, tekst) is not None


def sprawdz_saldo(saldo):
    try:
        if float(saldo) == float('inf'):
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")
            return False

        if czy_poprawne_saldo(saldo):
            return True
        else:
            print('Niepoprawna wartość. Spróbuj ponownie.\n')
            return False

    except ValueError:
        print('Saldo musi być liczbą. Spróbuj ponownie.\n')
    except OverflowError:
        print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")


def sprawdz_kwote(kwota):
    try:
        if float(kwota) == float('inf'):
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")
            return False

        if czy_poprawne_saldo(kwota):
            return True
        else:
            print('Niepoprawna wartość. Spróbuj ponownie.\n')
            return False

    except ValueError:
        print('Należy podać liczbę. Spróbuj ponownie.\n')
    except OverflowError:
        print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")


def czy_poprawne_oprocentowanie(tekst):
    wzorzec = r'^[0-9](\.\d{1,2})?$'
    return re.fullmatch(wzorzec, tekst) is not None


def sprawdz_oprocentowanie(oprocentowanie):
    try:
        if float(oprocentowanie) == float('inf'):
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")
            return False

        if czy_poprawne_oprocentowanie(oprocentowanie):
            return True
        else:
            print('Oprocentowanie musi być większe od 0 i mniejsze od 10 [%]. Spróbuj ponownie.\n')
            return False

    except ValueError:
        print('Oprocentowanie musi być liczbą. Spróbuj ponownie.\n')
    except OverflowError:
        print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")


import pandas as pd


def pokaz_banki():
    print('Zbiór dodanych banków:\n')
    df_banki = pd.DataFrame(slownik_bankow)
    df_banki.index = range(1, len(df_banki) + 1)
    print(df_banki)
    print('')


def pokaz_konta_bankowe():
    print('Zbiór dodanych kont bankowych:\n')
    df_konta_bankowe = pd.DataFrame(slownik_kont_bankowych)
    df_konta_bankowe.index = range(1, len(df_konta_bankowe) + 1)
    print(df_konta_bankowe)
    print('')


def pokaz_konta_oszczednosciowe():
    print('Zbiór dodanych kont oszczędnościowych:\n')
    df_konta_oszczednosciowe = pd.DataFrame(slownik_kont_oszczednosciowych)
    df_konta_oszczednosciowe.index = range(1, len(df_konta_oszczednosciowe) + 1)
    print(df_konta_oszczednosciowe)
    print('')


def dodaj_bank():
    while True:
        nazwa_banku = input('Podaj nazwę banku (lub anuluj wpisując 0):\n')
        if nazwa_banku.strip() == "0":
            return
        if sprawdz_nazwe_banku(nazwa_banku):
            if sprawdz_unikalna_nazwe_banku(nazwa_banku):
                b = Bank(nazwa_banku)
                lista_obiektow_bank.append(b)
                lista_bankow_nazwa_banku.append(b.nazwa_banku)
                slownik_bankow['nazwa banku'] = lista_bankow_nazwa_banku
                print(f'Pomyślnie dodano nowy bank: "{b.nazwa_banku}".\n')
                break


def dodaj_konto_bankowe():
    while True:
        nazwa_banku = input('Podaj nazwę banku (lub anuluj wpisując 0):\n')
        if nazwa_banku.strip() == "0":
            if nazwa_banku in lista_kb_nazwa_banku:
                lista_kb_nazwa_banku.remove(nazwa_banku)
            return
        if sprawdz_nazwe_banku(nazwa_banku):
            lista_kb_nazwa_banku.append(nazwa_banku)
            slownik_kont_bankowych['nazwa banku'] = lista_kb_nazwa_banku
            break

    while True:
        numer_konta = input('Podaj numer konta bankowego (lub anuluj wpisując 0):\n')
        if numer_konta.strip() == "0":
            if nazwa_banku in lista_kb_nazwa_banku:
                lista_kb_nazwa_banku.remove(nazwa_banku)
            if numer_konta in lista_kb_numer_konta:
                lista_kb_numer_konta.remove(numer_konta)
            return
        if sprawdz_nr_konta(numer_konta):
            if sprawdz_unikalny_nr_konta_bankowego(numer_konta):
                lista_kb_numer_konta.append(numer_konta)
                slownik_kont_bankowych['numer konta'] = lista_kb_numer_konta
                break

    while True:
        wlasciciel = input('Podaj właściciela (lub anuluj wpisując 0):\n')
        if wlasciciel.strip() == "0":
            if nazwa_banku in lista_kb_nazwa_banku:
                lista_kb_nazwa_banku.remove(nazwa_banku)
            if numer_konta in lista_kb_numer_konta:
                lista_kb_numer_konta.remove(numer_konta)
            if wlasciciel in lista_kb_wlasciciel:
                lista_kb_wlasciciel.remove(wlasciciel)
            return
        if sprawdz_nazwe_wlasciciela(wlasciciel):
            lista_kb_wlasciciel.append(wlasciciel)
            slownik_kont_bankowych['właściciel'] = lista_kb_wlasciciel
            break

    while True:
        try:
            saldo = input('Podaj saldo w [PLN] (lub anuluj wpisując 0):\n')
            if saldo.strip() == "0":
                if nazwa_banku in lista_kb_nazwa_banku:
                    lista_kb_nazwa_banku.remove(nazwa_banku)
                if numer_konta in lista_kb_numer_konta:
                    lista_kb_numer_konta.remove(numer_konta)
                if wlasciciel in lista_kb_wlasciciel:
                    lista_kb_wlasciciel.remove(wlasciciel)
                if saldo in lista_kb_saldo:
                    lista_kb_saldo.remove(saldo)
                return
            if sprawdz_saldo(saldo):
                saldo = float(saldo)
                kb = KontoBankowe(nazwa_banku, numer_konta, wlasciciel, saldo)
                lista_obiektow_konto_bankowe.append(kb)
                lista_kb_saldo.append(saldo)
                slownik_kont_bankowych['saldo [PLN]'] = lista_kb_saldo
                print('Pomyślnie dodano nowe konto bankowe.\n')
                break
        except ValueError:
            print('Saldo musi być liczbą. Spróbuj ponownie.\n')
        except OverflowError:
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")


def dodaj_konto_oszczednosciowe():
    while True:
        nazwa_banku = input('Podaj nazwę banku (lub anuluj wpisując 0):\n')
        if nazwa_banku.strip() == "0":
            if nazwa_banku in lista_ko_nazwa_banku:
                lista_ko_nazwa_banku.remove(nazwa_banku)
            return
        if sprawdz_nazwe_banku(nazwa_banku):
            lista_ko_nazwa_banku.append(nazwa_banku)
            slownik_kont_oszczednosciowych['nazwa banku'] = lista_ko_nazwa_banku
            break

    while True:
        numer_konta = input('Podaj numer konta oszczędnościowego (lub anuluj wpisując 0):\n')
        if numer_konta.strip() == "0":
            if nazwa_banku in lista_ko_nazwa_banku:
                lista_ko_nazwa_banku.remove(nazwa_banku)
            if numer_konta in lista_ko_numer_konta:
                lista_ko_numer_konta.remove(numer_konta)
            return
        if sprawdz_nr_konta(numer_konta):
            if sprawdz_unikalny_nr_konta_oszczednosciowego(numer_konta):
                lista_ko_numer_konta.append(numer_konta)
                slownik_kont_oszczednosciowych['numer konta'] = lista_ko_numer_konta
                break

    while True:
        wlasciciel = input('Podaj właściciela (lub anuluj wpisując 0):\n')
        if wlasciciel.strip() == "0":
            if nazwa_banku in lista_ko_nazwa_banku:
                lista_ko_nazwa_banku.remove(nazwa_banku)
            if numer_konta in lista_ko_numer_konta:
                lista_ko_numer_konta.remove(numer_konta)
            if wlasciciel in lista_ko_wlasciciel:
                lista_ko_wlasciciel.remove(wlasciciel)
            return
        if sprawdz_nazwe_wlasciciela(wlasciciel):
            lista_ko_wlasciciel.append(wlasciciel)
            slownik_kont_oszczednosciowych['właściciel'] = lista_ko_wlasciciel
            break

    while True:
        try:
            saldo = input('Podaj saldo w [PLN] (lub anuluj wpisując 0):\n')
            if saldo.strip() == "0":
                if nazwa_banku in lista_ko_nazwa_banku:
                    lista_ko_nazwa_banku.remove(nazwa_banku)
                if numer_konta in lista_ko_numer_konta:
                    lista_ko_numer_konta.remove(numer_konta)
                if wlasciciel in lista_ko_wlasciciel:
                    lista_ko_wlasciciel.remove(wlasciciel)
                if saldo in lista_ko_saldo:
                    lista_ko_saldo.remove(saldo)
                return
            if sprawdz_saldo(saldo):
                saldo = float(saldo)
                lista_ko_saldo.append(saldo)
                slownik_kont_oszczednosciowych['saldo [PLN]'] = lista_ko_saldo
                break
        except ValueError:
            print('Saldo musi być liczbą. Spróbuj ponownie.\n')
        except OverflowError:
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")

    while True:
        try:
            oprocentowanie = input('Podaj oprocentowanie w [%] (lub anuluj wpisując 0):\n')
            if oprocentowanie.strip() == "0":
                if nazwa_banku in lista_ko_nazwa_banku:
                    lista_ko_nazwa_banku.remove(nazwa_banku)
                if numer_konta in lista_ko_numer_konta:
                    lista_ko_numer_konta.remove(numer_konta)
                if wlasciciel in lista_ko_wlasciciel:
                    lista_ko_wlasciciel.remove(wlasciciel)
                if saldo in lista_ko_saldo:
                    lista_ko_saldo.remove(saldo)
                if oprocentowanie in lista_ko_oprocentowanie:
                    lista_ko_oprocentowanie.remove(oprocentowanie)
                return
            if sprawdz_oprocentowanie(oprocentowanie):
                oprocentowanie = float(oprocentowanie)
                ko = KontoOszczednosciowe(nazwa_banku, numer_konta, wlasciciel, saldo, oprocentowanie)
                lista_obiektow_konto_oszczednosciowe.append(ko)
                lista_ko_oprocentowanie.append(oprocentowanie)
                slownik_kont_oszczednosciowych['oprocentowanie [%]'] = lista_ko_oprocentowanie
                print('Pomyślnie dodano nowe konto oszczędnościowe.\n')
                break
        except ValueError:
            print('Oprocentowanie musi być liczbą. Spróbuj ponownie.\n')
        except OverflowError:
            print("Podana liczba jest zbyt duża. Spróbuj ponownie.\n")


def usun_bank():
    while True:
        el = input('Podaj nazwę banku do usunięcia (lub anuluj wpisując 0):\n')
        if el.strip() == "0":
            return
        if sprawdz_nazwe_banku(el):
            if el in lista_bankow_nazwa_banku:
                for i, bank in enumerate(lista_obiektow_bank):
                    if bank.nazwa_banku == el:
                        del lista_obiektow_bank[i]
                lista_bankow_nazwa_banku.remove(el)
                print(f'Pomyślnie usunięto bank: "{el}".\n')
                return
            else:
                print('Bank o podanej nazwie nie istnieje. Spróbuj ponownie.')
                pokaz_banki()
        else:
            pokaz_banki()


def usun_konto_bankowe():
    while True:
        el = input('Podaj numer konta bankowego do usunięcia (lub anuluj wpisując 0):\n')
        if el.strip() == "0":
            return
        if sprawdz_nr_konta(el):
            if el in lista_kb_numer_konta:
                for i, konto in enumerate(lista_obiektow_konto_bankowe):
                    if konto.numer_konta == el:
                        del lista_obiektow_konto_bankowe[i]
                index = lista_kb_numer_konta.index(el)
                del lista_kb_nazwa_banku[index]
                del lista_kb_numer_konta[index]
                del lista_kb_wlasciciel[index]
                del lista_kb_saldo[index]
                print(f'Pomyślnie usunięto konto bankowe o numerze: "{el}".\n')
                return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()
        else:
            pokaz_konta_bankowe()


def usun_konto_oszczednosciowe():
    while True:
        el = input('Podaj numer konta oszczędnościowego do usunięcia (lub anuluj wpisując 0):\n')
        if el.strip() == "0":
            return
        if sprawdz_nr_konta(el):
            if el in lista_ko_numer_konta:
                for i, konto in enumerate(lista_obiektow_konto_oszczednosciowe):
                    if konto.numer_konta == el:
                        del lista_obiektow_konto_oszczednosciowe[i]
                index = lista_ko_numer_konta.index(el)
                del lista_ko_nazwa_banku[index]
                del lista_ko_numer_konta[index]
                del lista_ko_wlasciciel[index]
                del lista_ko_saldo[index]
                del lista_ko_oprocentowanie[index]
                print(f'Pomyślnie usunięto konto oszczędnościowe o numerze: "{el}".\n')
                return
            else:
                print('Konto oszczędnościowe o podanym numerze nie istnieje. Spróbuj ponownie.\n')
                pokaz_konta_oszczednosciowe()
        else:
            pokaz_konta_oszczednosciowe()


def edytuj_nazwe_banku_banku():
    while True:
        nazwa = input('Podaj bank, którego nazwę chcesz zmienić (lub anuluj wpisując 0):\n')
        if nazwa.strip() == "0":
            return
        if sprawdz_nazwe_banku(nazwa):
            if nazwa in lista_bankow_nazwa_banku:
                nowa_nazwa = input('Podaj nową nazwę banku (lub anuluj wpisując 0):\n')
                if nowa_nazwa.strip() == "0":
                    return
                if sprawdz_nazwe_banku(nowa_nazwa):
                    if sprawdz_unikalna_nazwe_banku(nowa_nazwa):
                        for bank in lista_obiektow_bank:
                            if bank.nazwa_banku == nazwa:
                                bank.zmien_nazwe_banku(nowa_nazwa)
                        index = lista_bankow_nazwa_banku.index(nazwa)
                        lista_bankow_nazwa_banku[index] = nowa_nazwa
                        print(f'Pomyślnie zmieniono nazwę banku z "{nazwa}" na: "{nowa_nazwa}".\n')
                        return
            else:
                print('Nie znaleziono banku o podanej nazwie. Spróbuj ponownie.')
                pokaz_banki()
        else:
            pokaz_banki()



def edytuj_nazwe_banku_konta_bankowego():
    while True:
        numer = input('Podaj numer konta bankowego, w którym chcesz zmienić nazwę banku (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    nowa_nazwa = input('Podaj nową nazwę banku (lub anuluj wpisując 0):\n')
                    if nowa_nazwa.strip() == "0":
                        return
                    if sprawdz_nazwe_banku(nowa_nazwa):
                        for konto in lista_obiektow_konto_bankowe:
                            if konto.numer_konta == numer:
                                konto.zmien_nazwe_banku(nowa_nazwa)
                        index = lista_kb_numer_konta.index(numer)
                        nazwa = lista_kb_nazwa_banku[index]
                        lista_kb_nazwa_banku[index] = nowa_nazwa
                        print(f'Pomyślnie zmieniono nazwę banku z "{nazwa}" na: "{nowa_nazwa}".\n')
                        return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()
        else:
            pokaz_konta_bankowe()

def edytuj_nazwe_banku_konta_oszczednosciowego():
    while True:
        numer = input('Podaj numer konta oszczednosciowego, w którym chcesz zmienić nazwę banku (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    nowa_nazwa = input('Podaj nową nazwę banku (lub anuluj wpisując 0):\n')
                    if nowa_nazwa.strip() == "0":
                        return
                    if sprawdz_nazwe_banku(nowa_nazwa):
                        for konto in lista_obiektow_konto_oszczednosciowe:
                            if konto.numer_konta == numer:
                                konto.zmien_nazwe_banku(nowa_nazwa)
                        index = lista_ko_numer_konta.index(numer)
                        nazwa = lista_ko_nazwa_banku[index]
                        lista_ko_nazwa_banku[index] = nowa_nazwa
                        print(f'Pomyślnie zmieniono nazwę banku z "{nazwa}" na: "{nowa_nazwa}".\n')
                        return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()
        else:
            pokaz_konta_oszczednosciowe()

def edytuj_numer_konta_bankowego():
    while True:
        numer = input('Podaj numer konta bankowego, który chcesz zmienić (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    nowy_numer = input('Podaj nowy numer konta bankowego (lub anuluj wpisując 0):\n')
                    if nowy_numer.strip() == "0":
                        return
                    if sprawdz_nr_konta(nowy_numer):
                        if sprawdz_unikalny_nr_konta_bankowego(nowy_numer):
                            for konto in lista_obiektow_konto_bankowe:
                                if konto.numer_konta == numer:
                                    konto.zmien_numer_konta(nowy_numer)
                            index = lista_kb_numer_konta.index(numer)
                            lista_kb_numer_konta[index] = nowy_numer
                            print(f'Pomyślnie zmieniono numer konta bankowego z "{numer}" na: "{nowy_numer}".\n')
                            return
                        else:
                            pokaz_konta_bankowe()
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()
        else:
            pokaz_konta_bankowe()

def edytuj_numer_konta_oszczednosciowego():
    while True:
        numer = input('Podaj numer konta oszczędnościowego, który chcesz zmienić (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    nowy_numer = input('Podaj nowy numer konta oszczędnościowego (lub anuluj wpisując 0):\n')
                    if nowy_numer.strip() == "0":
                        return
                    if sprawdz_nr_konta(nowy_numer):
                        if sprawdz_unikalny_nr_konta_oszczednosciowego(nowy_numer):
                            for konto in lista_obiektow_konto_oszczednosciowe:
                                if konto.numer_konta == numer:
                                    konto.zmien_numer_konta(nowy_numer)
                            index = lista_ko_numer_konta.index(numer)
                            lista_ko_numer_konta[index] = nowy_numer
                            print(f'Pomyślnie zmieniono numer konta oszczędnościowego z "{numer}" na: "{nowy_numer}".\n')
                            return
                        else:
                            pokaz_konta_oszczednosciowe()
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()
        else:
            pokaz_konta_oszczednosciowe()

def edytuj_wlasciciela_konta_bankowego():
    while True:
        numer = input(
            'Podaj numer konta bankowego, w którym chcesz zmienić nazwę właściciela (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    nowa_nazwa = input('Podaj nową nazwę właściciela (lub anuluj wpisując 0):\n')
                    if nowa_nazwa.strip() == "0":
                        return
                    if sprawdz_nazwe_wlasciciela(nowa_nazwa):
                        for konto in lista_obiektow_konto_bankowe:
                            if konto.numer_konta == numer:
                                konto.zmien_wlasciciela(nowa_nazwa)
                        index = lista_kb_numer_konta.index(numer)
                        nazwa = lista_kb_wlasciciel[index]
                        lista_kb_wlasciciel[index] = nowa_nazwa
                        print(f'Pomyślnie zmieniono nazwę właściciela z "{nazwa}" na: "{nowa_nazwa}".\n')
                        return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()
        else:
            pokaz_konta_bankowe()

def edytuj_wlasciciela_konta_oszczednosciowego():
    while True:
        numer = input(
            'Podaj numer konta oszczędnościowego, w którym chcesz zmienić nazwę właściciela (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    nowa_nazwa = input('Podaj nową nazwę właściciela (lub anuluj wpisując 0):\n')
                    if nowa_nazwa.strip() == "0":
                        return
                    if sprawdz_nazwe_wlasciciela(nowa_nazwa):
                        for konto in lista_obiektow_konto_oszczednosciowe:
                            if konto.numer_konta == numer:
                                konto.zmien_wlasciciela(nowa_nazwa)
                        index = lista_ko_numer_konta.index(numer)
                        nazwa = lista_ko_wlasciciel[index]
                        lista_ko_wlasciciel[index] = nowa_nazwa
                        print(f'Pomyślnie zmieniono nazwę właściciela z "{nazwa}" na: "{nowa_nazwa}".\n')
                        return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()
        else:
            pokaz_konta_oszczednosciowe()

def edytuj_saldo_konta_bankowego():
    while True:
        numer = input('Podaj numer konta bankowego, w którym chcesz zmienić saldo (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    nowe_saldo = input('Podaj nowe saldo konta bankowego w [PLN] (lub anuluj wpisując 0):\n')
                    if nowe_saldo.strip() == "0":
                        return
                    if sprawdz_saldo(nowe_saldo):
                        nowe_saldo = float(nowe_saldo)
                        for konto in lista_obiektow_konto_bankowe:
                            if konto.numer_konta == numer:
                                konto.zmien_saldo(nowe_saldo)
                        index = lista_kb_numer_konta.index(numer)
                        saldo = lista_kb_saldo[index]
                        lista_kb_saldo[index] = nowe_saldo
                        print(f'Pomyślnie zmieniono saldo konta bankowego z {saldo:.2f} na: {nowe_saldo:.2f} [PLN].\n')
                        return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()
        else:
            pokaz_konta_bankowe()

def edytuj_saldo_konta_oszczednosciowego():
    while True:
        numer = input('Podaj numer konta oszczędnościowego, w którym chcesz zmienić saldo (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    nowe_saldo = input('Podaj nowe saldo konta oszczędnościowego w [PLN] (lub anuluj wpisując 0):\n')
                    if nowe_saldo.strip() == "0":
                        return
                    if sprawdz_saldo(nowe_saldo):
                        nowe_saldo = float(nowe_saldo)
                        for konto in lista_obiektow_konto_oszczednosciowe:
                            if konto.numer_konta == numer:
                                konto.zmien_saldo(nowe_saldo)
                        index = lista_ko_numer_konta.index(numer)
                        saldo = lista_ko_saldo[index]
                        lista_ko_saldo[index] = nowe_saldo
                        print(f'Pomyślnie zmieniono saldo konta oszczędnościowego z {saldo:.2f} na: {nowe_saldo:.2f} [PLN].\n')
                        return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()
        else:
            pokaz_konta_oszczednosciowe()

def wplata_konto_bankowe():
    while True:
        numer = input('Podaj numer konta bankowego, na które chcesz dokonać wpłaty (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    wplata = input('Podaj kwotę wpłaty w [PLN] (lub anuluj wpisując 0):\n')
                    if wplata.strip() == "0":
                        return
                    
                    index = lista_kb_numer_konta.index(numer)
                    konto = lista_obiektow_konto_bankowe[index]
                    if sprawdz_kwote(wplata):
                        try:
                            wplata = float(wplata)
                            stare_saldo = konto.pobierz_saldo()
                            konto.wplata(wplata)
                            nowe_saldo = konto.pobierz_saldo()
                            lista_kb_saldo[index] = nowe_saldo
                            print(
                                f'Wpłacono {wplata:.2f} [PLN]. Saldo konta {numer} zmieniło się z {stare_saldo:.2f} do {nowe_saldo:.2f} [PLN].\n')
                            return
                        except ValueError as e:
                            print(e)
                            return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()

def wplata_konto_oszczednosciowe():
    while True:
        numer = input('Podaj numer konta oszczędnościowego, na które chcesz dokonać wpłaty (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    wplata = input('Podaj kwotę wpłaty w [PLN] (lub anuluj wpisując 0):\n')
                    if wplata.strip() == "0":
                        return
                    
                    index = lista_ko_numer_konta.index(numer)
                    konto = lista_obiektow_konto_oszczednosciowe[index]
                    if sprawdz_kwote(wplata):
                        try:
                            wplata = float(wplata)
                            stare_saldo = konto.pobierz_saldo()
                            konto.wplata(wplata)
                            nowe_saldo = konto.pobierz_saldo()
                            lista_ko_saldo[index] = nowe_saldo
                            print(f'Wpłacono {wplata:.2f} [PLN]. Saldo konta {numer} zmieniło się z {stare_saldo:.2f} do {nowe_saldo:.2f} [PLN].\n')
                            return
                        except ValueError as e:
                            print(e)
                            return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()

def wyplata_konto_bankowe():
    while True:
        numer = input('Podaj numer konta bankowego, z którego chcesz wypłacić pieniądze (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_kb_numer_konta:
                while True:
                    wyplata = input('Podaj kwotę wypłaty w [PLN] (lub anuluj wpisując 0):\n')
                    if wyplata.strip() == "0":
                        return
                    
                    index = lista_kb_numer_konta.index(numer)
                    konto = lista_obiektow_konto_bankowe[index]
                    if sprawdz_kwote(wyplata):
                        try:
                            wyplata = float(wyplata)
                            stare_saldo = konto.pobierz_saldo()
                            konto.wyplata(wyplata)
                            nowe_saldo = konto.pobierz_saldo()
                            lista_kb_saldo[index] = nowe_saldo
                            print(f'Wypłacono {wyplata:.2f} [PLN]. Saldo konta {numer} zmieniło się z {stare_saldo:.2f} do {nowe_saldo:.2f} [PLN].\n')
                            return
                        except ValueError as e:
                            print(e)
                            return
            else:
                print('Nie znaleziono konta bankowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_bankowe()

def wyplata_konto_oszczednosciowe():
    while True:
        numer = input('Podaj numer konta oszczędnościowego, z którego chcesz wypłacić pieniądze (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                while True:
                    wyplata = input('Podaj kwotę wypłaty w [PLN] (lub anuluj wpisując 0):\n')
                    if wyplata.strip() == "0":
                        return
                    
                    index = lista_ko_numer_konta.index(numer)
                    konto = lista_obiektow_konto_oszczednosciowe[index]
                    if sprawdz_kwote(wyplata):
                        try:
                            wyplata = float(wyplata)
                            stare_saldo = konto.pobierz_saldo()
                            konto.wyplata(wyplata)
                            nowe_saldo = konto.pobierz_saldo()
                            lista_ko_saldo[index] = nowe_saldo
                            print(f'Wypłacono {wyplata:.2f} [PLN]. Saldo konta {numer} zmieniło się z {stare_saldo:.2f} do {nowe_saldo:.2f} [PLN].\n')
                            return
                        except ValueError as e:
                            print(e)
                            return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()

def transfer_konto_bankowe():
    while True:
        numer_nadawcy = input(
            'Podaj numer konta bankowego, z którego chcesz wykonać transfer (lub anuluj wpisując 0):\n')
        if numer_nadawcy.strip() == "0":
            return
        if sprawdz_nr_konta(numer_nadawcy):
            if numer_nadawcy in lista_kb_numer_konta:
                index_nadawcy = lista_kb_numer_konta.index(numer_nadawcy)
                konto_nadawcy = lista_obiektow_konto_bankowe[index_nadawcy]
                break
            else:
                print('Nie znaleziono konta nadawcy. Spróbuj ponownie.')
                pokaz_konta_bankowe()

    while True:
        numer_odbiorcy = input(
            'Podaj numer konta bankowego, na które chcesz przelać środki (lub anuluj wpisując 0):\n')
        if numer_odbiorcy.strip() == "0":
            return
        if sprawdz_nr_konta(numer_odbiorcy):
            if numer_odbiorcy in lista_kb_numer_konta:
                if numer_odbiorcy == numer_nadawcy:
                    print("Nie można wykonać transferu na to samo konto.\n")
                    continue
                index_odbiorcy = lista_kb_numer_konta.index(numer_odbiorcy)
                konto_odbiorcy = lista_obiektow_konto_bankowe[index_odbiorcy]
                break
            else:
                print('Nie znaleziono konta odbiorcy. Spróbuj ponownie.')
                pokaz_konta_bankowe()

    while True:
        kwota = input('Podaj kwotę transferu w [PLN] (lub anuluj wpisując 0):\n')
        if kwota.strip() == "0":
            return
        
        if sprawdz_kwote(kwota):
            try:
                kwota = float(kwota)
                saldo_przed = konto_nadawcy.pobierz_saldo()
                konto_nadawcy.transfer(konto_odbiorcy, kwota)
                saldo_po = konto_nadawcy.pobierz_saldo()
                lista_kb_saldo[index_nadawcy] = saldo_po
                lista_kb_saldo[index_odbiorcy] = konto_odbiorcy.pobierz_saldo()
                print(f'Pomyślnie przelano {kwota:.2f} [PLN] z konta "{numer_nadawcy}" na konto "{numer_odbiorcy}".\n'
                    f'Saldo nadawcy: {saldo_przed:.2f} → {saldo_po:.2f} [PLN].\n'
                    f'Saldo odbiorcy: {lista_kb_saldo[index_odbiorcy] - kwota:.2f} → {lista_kb_saldo[index_odbiorcy]:.2f} [PLN].\n')
                return
            except ValueError as e:
                print(e)
                return

def transfer_konto_oszczednosciowe():
    while True:
        numer_nadawcy = input(
            'Podaj numer konta oszczędnościowego, z którego chcesz wykonać transfer (lub anuluj wpisując 0):\n')
        if numer_nadawcy.strip() == "0":
            return
        if sprawdz_nr_konta(numer_nadawcy):
            if numer_nadawcy in lista_ko_numer_konta:
                index_nadawcy = lista_ko_numer_konta.index(numer_nadawcy)
                konto_nadawcy = lista_obiektow_konto_oszczednosciowe[index_nadawcy]
                break
            else:
                print('Nie znaleziono konta nadawcy. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()

    while True:
        numer_odbiorcy = input(
            'Podaj numer konta oszczędnościowego, na które chcesz przelać środki (lub anuluj wpisując 0):\n')
        if numer_odbiorcy.strip() == "0":
            return
        if sprawdz_nr_konta(numer_odbiorcy):
            if numer_odbiorcy in lista_ko_numer_konta:
                if numer_odbiorcy == numer_nadawcy:
                    print("Nie można wykonać transferu na to samo konto.\n")
                    continue
                index_odbiorcy = lista_ko_numer_konta.index(numer_odbiorcy)
                konto_odbiorcy = lista_obiektow_konto_oszczednosciowe[index_odbiorcy]
                break
            else:
                print('Nie znaleziono konta odbiorcy. Spróbuj ponownie.')
                pokaz_konta_oszczednosciowe()

    while True:
        kwota = input('Podaj kwotę transferu w [PLN] (lub anuluj wpisując 0):\n')
        if kwota.strip() == "0":
            return
        if sprawdz_kwote(kwota):
            try:
                kwota = float(kwota)
                saldo_przed = konto_nadawcy.pobierz_saldo()
                konto_nadawcy.transfer(konto_odbiorcy, kwota)
                saldo_po = konto_nadawcy.pobierz_saldo()
                lista_ko_saldo[index_nadawcy] = saldo_po
                lista_ko_saldo[index_odbiorcy] = konto_odbiorcy.pobierz_saldo()
                print(f'Pomyślnie przelano {kwota:.2f} [PLN] z konta {numer_nadawcy} na konto {numer_odbiorcy}.\n'
                    f'Saldo nadawcy: {saldo_przed:.2f} → {saldo_po:.2f} [PLN].\n'
                    f'Saldo odbiorcy: {lista_ko_saldo[index_odbiorcy] - kwota:.2f} → {lista_ko_saldo[index_odbiorcy]:.2f} [PLN].\n')
                return
            except ValueError as e:
                print(e)
                return

def zmiana_oprocentowania():
    while True:
        numer = input(
            'Podaj numer konta oszczędnościowego, w którym chcesz zmienić oprocentowanie (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                index = lista_ko_numer_konta.index(numer)
                konto = lista_obiektow_konto_oszczednosciowe[index]

                while True:
                    nowe_opr = input('Podaj nowe oprocentowanie w [%] (lub anuluj wpisując 0):\n')
                    if nowe_opr.strip() == "0":
                        return
                    if sprawdz_oprocentowanie(nowe_opr):
                        nowe_opr = float(nowe_opr)
                        stare_opr = lista_ko_oprocentowanie[index]
                        konto.zmien_oprocentowanie(nowe_opr)
                        lista_ko_oprocentowanie[index] = nowe_opr
                        print(
                            f"Pomyślnie zmieniono oprocentowanie konta {numer} z {stare_opr:.2f} na {nowe_opr:.2f} [%].\n")
                        return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze.\n')
                pokaz_konta_oszczednosciowe()

def naliczanie_odsetek():
    while True:
        numer = input(
            'Podaj numer konta oszczędnościowego, dla którego chcesz naliczyć odsetki (lub anuluj wpisując 0):\n')
        if numer.strip() == "0":
            return
        if sprawdz_nr_konta(numer):
            if numer in lista_ko_numer_konta:
                index = lista_ko_numer_konta.index(numer)
                konto = lista_obiektow_konto_oszczednosciowe[index]
                saldo_przed = konto.pobierz_saldo()

                konto.nalicz_odsetki()

                saldo_po = konto.pobierz_saldo()
                lista_ko_saldo[index] = saldo_po

                print(f"Saldo konta {numer} wzrosło z {saldo_przed:.2f} [PLN] do {saldo_po:.2f} [PLN].\n")
                return
            else:
                print('Nie znaleziono konta oszczędnościowego o podanym numerze.\n')
                pokaz_konta_oszczednosciowe()

def wyszukaj_konto_bankowe_po_banku():
    while True:
        fraza = input(
            "Podaj frazę do wyszukania w nazwie banku:\n").strip().lower()
        dopasowane = [konto for konto in lista_obiektow_konto_bankowe if
                      fraza in konto.nazwa_banku.lower()]
        if dopasowane:
            
            keys_kb = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]']
            sl_kb = dict.fromkeys(keys_kb)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                
            sl_kb['nazwa banku'] = dopasowane_nazwa_banku
            sl_kb['numer konta'] = dopasowane_numer_konta
            sl_kb['właściciel'] = dopasowane_wlasciciel
            sl_kb['saldo [PLN]'] = dopasowane_saldo
            df = pd.DataFrame(sl_kb)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono kont bankowych z nazwą banku zawierającą podaną frazę.\n")
            return

def wyszukaj_konto_oszczednosciowe_po_banku():
    while True:
        fraza = input(
            "Podaj frazę do wyszukania w nazwie banku:\n").strip().lower()
        dopasowane = [konto for konto in lista_obiektow_konto_oszczednosciowe if
                      fraza in konto.nazwa_banku.lower()]
        if dopasowane:
            
            keys_ko = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]', 'oprocentowanie [%]']
            sl_ko = dict.fromkeys(keys_ko)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []
            dopasowane_oprocentowanie = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                dopasowane_oprocentowanie.append(konto.oprocentowanie)

            sl_ko['nazwa banku'] = dopasowane_nazwa_banku
            sl_ko['numer konta'] = dopasowane_numer_konta
            sl_ko['właściciel'] = dopasowane_wlasciciel
            sl_ko['saldo [PLN]'] = dopasowane_saldo
            sl_ko['oprocentowanie [%]'] = dopasowane_oprocentowanie
            df = pd.DataFrame(sl_ko)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono kont bankowych z nazwą banku zawierającą podaną frazę.\n")
            return

def wyszukaj_konto_bankowe_po_wlascicielu():
    while True:
        dane = input("Podaj właściciela konta bankowego:\n").strip().lower()
        if not dane:
            print("Nie podano żadnych danych. Spróbuj ponownie.\n")
            continue

        dopasowane = [konto for konto in lista_obiektow_konto_bankowe
                      if dane in konto.wlasciciel.lower()]

        if dopasowane:
            keys_kb = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]']
            sl_kb = dict.fromkeys(keys_kb)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                
            sl_kb['nazwa banku'] = dopasowane_nazwa_banku
            sl_kb['numer konta'] = dopasowane_numer_konta
            sl_kb['właściciel'] = dopasowane_wlasciciel
            sl_kb['saldo [PLN]'] = dopasowane_saldo
            df = pd.DataFrame(sl_kb)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono konta oszczędnościowego dla podanego właściciela.\n")
            return

def wyszukaj_konto_oszczednosciowe_po_wlascicielu():
    while True:
        dane = input("Podaj właściciela konta oszczędnościowego:\n").strip().lower()
        if not dane:
            print("Nie podano żadnych danych. Spróbuj ponownie.\n")
            continue

        dopasowane = [konto for konto in lista_obiektow_konto_oszczednosciowe
                      if dane in konto.wlasciciel.lower()]

        if dopasowane:
            keys_ko = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]', 'oprocentowanie [%]']
            sl_ko = dict.fromkeys(keys_ko)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []
            dopasowane_oprocentowanie = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                dopasowane_oprocentowanie.append(konto.oprocentowanie)

            sl_ko['nazwa banku'] = dopasowane_nazwa_banku
            sl_ko['numer konta'] = dopasowane_numer_konta
            sl_ko['właściciel'] = dopasowane_wlasciciel
            sl_ko['saldo [PLN]'] = dopasowane_saldo
            sl_ko['oprocentowanie [%]'] = dopasowane_oprocentowanie
            df = pd.DataFrame(sl_ko)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono konta oszczędnościowego dla podanego właściciela.\n")
            return

def wyszukaj_konto_bankowe_po_numerze():
    while True:
        numer = input("Podaj numer konta bankowego (lub anuluj wpisując 0):\n").strip()

        if numer == "0":
            return

        if not sprawdz_nr_konta(numer):
            continue

        dopasowane = [konto for konto in lista_obiektow_konto_bankowe if konto.numer_konta == numer]

        if dopasowane:
            keys_kb = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]']
            sl_kb = dict.fromkeys(keys_kb)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                
            sl_kb['nazwa banku'] = dopasowane_nazwa_banku
            sl_kb['numer konta'] = dopasowane_numer_konta
            sl_kb['właściciel'] = dopasowane_wlasciciel
            sl_kb['saldo [PLN]'] = dopasowane_saldo
            df = pd.DataFrame(sl_kb)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono konta bankowego o podanym numerze.\n")
            return

def wyszukaj_konto_oszczednosciowe_po_numerze():
    while True:
        numer = input("Podaj numer konta oszczednosciowego (lub anuluj wpisując 0):\n").strip()

        if numer == "0":
            return

        if not sprawdz_nr_konta(numer):
            continue

        dopasowane = [konto for konto in lista_obiektow_konto_oszczednosciowe if konto.numer_konta == numer]

        if dopasowane:
            keys_ko = ['nazwa banku', 'numer konta', 'właściciel', 'saldo [PLN]', 'oprocentowanie [%]']
            sl_ko = dict.fromkeys(keys_ko)

            dopasowane_nazwa_banku = []
            dopasowane_numer_konta = []
            dopasowane_wlasciciel = []
            dopasowane_saldo = []
            dopasowane_oprocentowanie = []

            for konto in dopasowane:
                dopasowane_nazwa_banku.append(konto.nazwa_banku)
                dopasowane_numer_konta.append(konto.numer_konta)
                dopasowane_wlasciciel.append(konto.wlasciciel)
                dopasowane_saldo.append(konto.pobierz_saldo())
                dopasowane_oprocentowanie.append(konto.oprocentowanie)

            sl_ko['nazwa banku'] = dopasowane_nazwa_banku
            sl_ko['numer konta'] = dopasowane_numer_konta
            sl_ko['właściciel'] = dopasowane_wlasciciel
            sl_ko['saldo [PLN]'] = dopasowane_saldo
            sl_ko['oprocentowanie [%]'] = dopasowane_oprocentowanie
            df = pd.DataFrame(sl_ko)
            df.index = range(1, len(df) + 1)
            print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
            print(df)
            return
        else:
            print("Nie znaleziono konta oszczednosciowego o podanym numerze.\n")
            return

def stworz_konto_bankowe_na_podstawie_banku():
    if not lista_obiektow_bank:
        print("Brak dostępnych banków. Najpierw dodaj bank.\n")
        return

    pokaz_banki()

    while True:
        try:
            wybor = input("Podaj numer przy nazwie banku, dla którego chcesz utworzyć konto bankowe (lub anuluj wpisując 0):\n")
            if wybor.strip() == "0":
                return
            wybor = int(wybor)
            if sprawdz_liczbe(wybor - 1, len(lista_obiektow_bank) - 1):
                break
        except ValueError:
            print("Wprowadź poprawną liczbę całkowitą.\n")

    wybrany_bank = lista_obiektow_bank[wybor - 1]
    nazwa_banku = wybrany_bank.nazwa_banku

    while True:
        numer_konta = input("Podaj numer konta (26 cyfr) (lub anuluj wpisując 0):\n")
        if numer_konta.strip() == "0":
            return
        if sprawdz_nr_konta(numer_konta) and sprawdz_unikalny_nr_konta_bankowego(numer_konta):
            break
        else:
            pokaz_konta_bankowe()

    while True:
        wlasciciel = input("Podaj właściciela konta (lub anuluj wpisując 0):\n")
        if wlasciciel.strip() == "0":
            return
        if sprawdz_nazwe_wlasciciela(wlasciciel):
            break

    while True:
        try:
            saldo_input = input("Podaj saldo konta bankowego (lub anuluj wpisując 0):\n")
            if saldo_input.strip() == "0":
                return
            if sprawdz_saldo(saldo_input):
                saldo = float(saldo_input)
                break
        except ValueError:
            print("Nieprawidłowa wartość salda. Podaj liczbę.\n")

    konto = KontoBankowe(nazwa_banku, numer_konta, wlasciciel, saldo)
    lista_obiektow_konto_bankowe.append(konto)
    lista_kb_nazwa_banku.append(nazwa_banku)
    lista_kb_numer_konta.append(numer_konta)
    lista_kb_wlasciciel.append(wlasciciel)
    lista_kb_saldo.append(saldo)

    slownik_kont_bankowych['nazwa banku'] = lista_kb_nazwa_banku
    slownik_kont_bankowych['numer konta'] = lista_kb_numer_konta
    slownik_kont_bankowych['właściciel'] = lista_kb_wlasciciel
    slownik_kont_bankowych['saldo [PLN]'] = lista_kb_saldo

    print(f'\nPomyślnie utworzono konto bankowe dla banku: "{nazwa_banku}".\n')


def stworz_konto_oszczednosciowe_na_podstawie_banku():
    if not lista_bankow_nazwa_banku:
        print("Brak dostępnych banków. Najpierw dodaj bank.\n")
        return

    pokaz_banki()

    while True:
        try:
            wybor = input("Podaj numer przy nazwie banku, dla którego chcesz utworzyć konto oszczędnościowe (lub anuluj wpisując 0):\n")
            if wybor.strip() == "0":
                return
            wybor = int(wybor)
            if sprawdz_liczbe(wybor - 1, len(lista_bankow_nazwa_banku) - 1):
                break
        except ValueError:
            print("Wprowadź poprawną liczbę całkowitą.\n")

    nazwa_banku = lista_bankow_nazwa_banku[wybor - 1]

    while True:
        numer_konta = input("Podaj numer konta oszczędnościowego (26 cyfr) (lub anuluj wpisując 0):\n")
        if numer_konta.strip() == "0":
            return
        if sprawdz_nr_konta(numer_konta):
            if sprawdz_unikalny_nr_konta_oszczednosciowego(numer_konta):
                break
            else:
                pokaz_konta_oszczednosciowe()
                continue

    while True:
        wlasciciel = input("Podaj właściciela konta oszczędnościowego (lub anuluj wpisując 0):\n")
        if wlasciciel.strip() == "0":
            return
        if sprawdz_nazwe_wlasciciela(wlasciciel):
            break

    while True:
        try:
            saldo_input = input("Podaj saldo początkowe konta [PLN] (lub anuluj wpisując 0):\n")
            if saldo_input.strip() == "0":
                return
            if sprawdz_saldo(saldo_input):
                saldo = float(saldo_input)
                break
        except ValueError:
            print("Nieprawidłowa wartość salda. Podaj liczbę.\n")

    while True:
        try:
            oprocentowanie_input = input("Podaj oprocentowanie konta oszczędnościowego w [%] (lub anuluj wpisując 0):\n")
            if oprocentowanie_input.strip() == "0":
                return
            if sprawdz_oprocentowanie(oprocentowanie_input):
                oprocentowanie = float(oprocentowanie_input)
                break
        except ValueError:
            print("Nieprawidłowa wartość oprocentowania. Podaj liczbę.\n")

    konto_oszcz = KontoOszczednosciowe(
        nazwa_banku,
        numer_konta,
        wlasciciel,
        saldo,
        oprocentowanie
    )

    lista_obiektow_konto_oszczednosciowe.append(konto_oszcz)
    lista_ko_nazwa_banku.append(nazwa_banku)
    lista_ko_numer_konta.append(numer_konta)
    lista_ko_wlasciciel.append(wlasciciel)
    lista_ko_saldo.append(saldo)
    lista_ko_oprocentowanie.append(oprocentowanie)

    slownik_kont_oszczednosciowych['nazwa banku'] = lista_ko_nazwa_banku
    slownik_kont_oszczednosciowych['numer konta'] = lista_ko_numer_konta
    slownik_kont_oszczednosciowych['właściciel'] = lista_ko_wlasciciel
    slownik_kont_oszczednosciowych['saldo [PLN]'] = lista_ko_saldo
    slownik_kont_oszczednosciowych['oprocentowanie [%]'] = lista_ko_oprocentowanie

    print(f'\nPomyślnie utworzono konto oszczędnościowe w banku: "{nazwa_banku}".\n')

def stworz_konto_oszczednosciowe_na_podstawie_konta_bankowego():
    if not lista_obiektow_konto_bankowe:
        print("Brak dostępnych kont bankowych. Najpierw dodaj konto bankowe.\n")
        return

    while True:
        pokaz_konta_bankowe()
        try:
            wybor = input("Podaj numer przy koncie bankowym, dla którego chcesz utworzyć konto oszczędnościowe (lub anuluj wpisując 0):\n")
            if wybor.strip() == "0":
                return
            wybor = int(wybor)
            if sprawdz_liczbe(wybor - 1, len(lista_obiektow_konto_bankowe) - 1):
                wybrane_konto = lista_obiektow_konto_bankowe[wybor - 1]

                numer_konta = wybrane_konto.numer_konta
                if not sprawdz_unikalny_nr_konta_oszczednosciowego(numer_konta):
                    pokaz_konta_oszczednosciowe()
                    continue

                nazwa_banku = wybrane_konto.nazwa_banku
                wlasciciel = wybrane_konto.wlasciciel
                saldo = wybrane_konto.pobierz_saldo()
                break
        except ValueError:
            print("Wprowadź poprawną liczbę całkowitą.\n")

    while True:
        try:
            oprocentowanie_input = input("Podaj oprocentowanie konta oszczędnościowego w [%] (lub anuluj wpisując 0):\n")
            if oprocentowanie_input.strip() == "0":
                return
            if sprawdz_oprocentowanie(oprocentowanie_input):
                oprocentowanie = float(oprocentowanie_input)
                break
        except ValueError:
            print("Nieprawidłowa wartość oprocentowania. Podaj liczbę.\n")

    konto_oszcz = KontoOszczednosciowe(
        nazwa_banku,
        numer_konta,
        wlasciciel,
        saldo,
        oprocentowanie
    )

    lista_obiektow_konto_oszczednosciowe.append(konto_oszcz)
    lista_ko_nazwa_banku.append(nazwa_banku)
    lista_ko_numer_konta.append(numer_konta)
    lista_ko_wlasciciel.append(wlasciciel)
    lista_ko_saldo.append(saldo)
    lista_ko_oprocentowanie.append(oprocentowanie)

    slownik_kont_oszczednosciowych['nazwa banku'] = lista_ko_nazwa_banku
    slownik_kont_oszczednosciowych['numer konta'] = lista_ko_numer_konta
    slownik_kont_oszczednosciowych['właściciel'] = lista_ko_wlasciciel
    slownik_kont_oszczednosciowych['saldo [PLN]'] = lista_ko_saldo
    slownik_kont_oszczednosciowych['oprocentowanie [%]'] = lista_ko_oprocentowanie

    print(f'\nPomyślnie utworzono konto oszczędnościowe dla numeru konta: "{numer_konta}" w banku: "{nazwa_banku}".\n')



def sprawdz_plik_txt_sredniki(nazwa_pliku, maks_kolumn, separator=";"):
    blad = False
    with open(nazwa_pliku, 'r', encoding='utf-8') as f:
        for i, linia in enumerate(f, start=1):
            kolumny = linia.strip().split(separator)
            if len(kolumny) != maks_kolumn:
                print(f'Niepoprawna liczba kolumn w linii {i}: {len(kolumny)} zamiast {maks_kolumn}')
                blad = True
    if blad:
        return False
    return True



def zapisz_banki_do_pliku():
    if not lista_obiektow_bank == []:
        while True:
            try:
                nazwa_pliku = input("Podaj nazwę pliku do zapisu (lub anuluj wpisując 0):\n").strip()
                if nazwa_pliku == "0":
                    return
                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    plik.write("nazwa_banku\n")
                    for bank in lista_obiektow_bank:
                        plik.write(f"{bank.nazwa_banku}\n")
                print(f'Pomyślnie zapisano dane do pliku: "{nazwa_pliku}".\n')
                return
            except Exception as e:
                print(f"Wystąpił błąd podczas zapisu do pliku: {e}. Spróbuj ponownie.\n")
    else:
        print("Nie można zapisać danych banków do pliku, ponieważ nie dodano jeszcze żadnych banków.\n")


def odczytaj_banki_z_pliku():
    while True:
        try:
            nazwa_pliku = input("Podaj nazwę pliku do odczytu (lub anuluj wpisując 0):\n").strip()
            if nazwa_pliku == "0":
                return
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                linie = plik.readlines()
                if len(linie) <= 1:
                    print("Plik nie zawiera żadnych danych do wczytania.\n")
                else:
                    if not sprawdz_plik_txt_sredniki(nazwa_pliku, 1):
                        pass
                    else:
                        lista_obiektow_bank.clear()
                        lista_bankow_nazwa_banku.clear()
                        for i, linia in enumerate(linie[1:], start=2):
                            nazwa = linia.strip()
                            if sprawdz_nazwe_banku(nazwa):
                                bank = Bank(nazwa)
                                lista_obiektow_bank.append(bank)
                                lista_bankow_nazwa_banku.append(nazwa)
                            else:
                                print(f'Niepoprawna nazwa banku w linii {i}: "{linia.strip()}"\n')
                                return
                            slownik_bankow['nazwa banku'] = lista_bankow_nazwa_banku
                        print(f'Pomyślnie wczytano {len(lista_obiektow_bank)} bank(ów) z pliku: "{nazwa_pliku}".\n')
                        return
        except FileNotFoundError:
            print(f'Plik o nazwie "{nazwa_pliku}" nie istnieje. Spróbuj ponownie.\n')
        except Exception as e:
            print(f'Wystąpił błąd podczas odczytu z pliku: {e}. Spróbuj ponownie.\n')


def zapisz_kb_do_pliku():
    if not lista_obiektow_konto_bankowe == []:
        while True:
            try:
                nazwa_pliku = input("Podaj nazwę pliku do zapisu (lub anuluj wpisując 0):\n").strip()
                if nazwa_pliku == "0":
                    return
                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    plik.write("nazwa_banku;numer_konta;wlasciciel;saldo\n")
                    for konto in lista_obiektow_konto_bankowe:
                        plik.write(
                            f"{konto.nazwa_banku};{konto.numer_konta};{konto.wlasciciel};{konto.pobierz_saldo():.2f}\n")
                print(f'Pomyślnie zapisano dane kont bankowych do pliku: "{nazwa_pliku}".\n')
                return
            except Exception as e:
                print(f"Wystąpił błąd podczas zapisu do pliku: {e}. Spróbuj ponownie.\n")
    else:
        print('Nie można zapisać danych kont bankowych do pliku, ponieważ nie dodano jeszcze żadnych kont bankowych.\n')



def odczytaj_kb_z_pliku():
    while True:
        try:
            nazwa_pliku = input("Podaj nazwę pliku do odczytu (lub anuluj wpisując 0):\n").strip()
            if nazwa_pliku == "0":
                return
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                linie = plik.readlines()
                if len(linie) <= 1:
                    print("Plik nie zawiera żadnych danych do wczytania.\n")
                else:
                    if not sprawdz_plik_txt_sredniki(nazwa_pliku, 4):
                        pass
                    else:
                        lista_obiektow_konto_bankowe.clear()
                        lista_kb_nazwa_banku.clear()
                        lista_kb_numer_konta.clear()
                        lista_kb_wlasciciel.clear()
                        lista_kb_saldo.clear()
                        for i, linia in enumerate(linie[1:], start=2):
                            dane = linia.strip().split(";")
                            if len(dane) == 4:
                                nazwa_banku, numer_konta, wlasciciel, saldo_str = dane

                                if sprawdz_nazwe_banku(nazwa_banku):
                                    pass
                                else:
                                    print(f'Niepoprawna nazwa banku w linii {i}: "{linia.strip()}"\n')
                                    return
                                if sprawdz_nr_konta(numer_konta):
                                    pass
                                else:
                                    print(f'Niepoprawny numer konta oszczędnościowego w linii {i}: "{linia.strip()}"\n')
                                    return
                                if sprawdz_nazwe_wlasciciela(wlasciciel):
                                    pass
                                else:
                                    print(f'Niepoprawna nazwa właściciela w linii {i}: "{linia.strip()}"\n')
                                    return
                                if sprawdz_saldo(saldo_str):
                                    saldo = float(saldo_str)
                                else:
                                    print(f'Niepoprawne saldo w linii {i}: "{linia.strip()}"\n')
                                    return

                                konto = KontoBankowe(nazwa_banku, numer_konta, wlasciciel, saldo)
                                lista_obiektow_konto_bankowe.append(konto)
                                lista_kb_nazwa_banku.append(nazwa_banku)
                                lista_kb_numer_konta.append(numer_konta)
                                lista_kb_wlasciciel.append(wlasciciel)
                                lista_kb_saldo.append(saldo)
                        slownik_kont_bankowych['nazwa banku'] = lista_kb_nazwa_banku
                        slownik_kont_bankowych['numer konta'] = lista_kb_numer_konta
                        slownik_kont_bankowych['właściciel'] = lista_kb_wlasciciel
                        slownik_kont_bankowych['saldo [PLN]'] = lista_kb_saldo
                        print(f'Pomyślnie wczytano {len(lista_obiektow_konto_bankowe)} kont(a) bankowych z pliku: "{nazwa_pliku}".\n')
                        return
        except FileNotFoundError:
            print(f'Plik o nazwie "{nazwa_pliku}" nie istnieje. Spróbuj ponownie.\n')
        except Exception as e:
            print(f"Wystąpił błąd podczas odczytu z pliku: {e}. Spróbuj ponownie.\n")


def zapisz_ko_do_pliku():
    if not lista_obiektow_konto_oszczednosciowe == []:
        while True:
            try:
                nazwa_pliku = input("Podaj nazwę pliku do zapisu (lub anuluj wpisując 0):\n").strip()
                if nazwa_pliku == "0":
                    return
                with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
                    plik.write("nazwa_banku;numer_konta;wlasciciel;saldo;oprocentowanie\n")
                    for konto in lista_obiektow_konto_oszczednosciowe:
                        plik.write(
                            f"{konto.nazwa_banku};{konto.numer_konta};{konto.wlasciciel};"
                            f"{konto.pobierz_saldo():.2f};{konto.oprocentowanie:.2f}\n")
                print(f'Pomyślnie zapisano dane kont oszczędnościowych do pliku: "{nazwa_pliku}".\n')
                return
            except Exception as e:
                print(f"Wystąpił błąd podczas zapisu do pliku: {e}. Spróbuj ponownie.\n")
    else:
        print("Nie można zapisać danych kont oszczędnościowych do pliku, ponieważ nie dodano jeszcze żadnych kont oszczędnościowych.\n")



def odczytaj_ko_z_pliku():
    while True:
        try:
            nazwa_pliku = input("Podaj nazwę pliku do odczytu (lub anuluj wpisując 0):\n").strip()
            if nazwa_pliku == "0":
                return
            with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
                linie = plik.readlines()
                if len(linie) <= 1:
                    print("Plik nie zawiera żadnych danych do wczytania.\n")
                else:
                    if not sprawdz_plik_txt_sredniki(nazwa_pliku, 5):
                        pass
                    else:
                        lista_obiektow_konto_oszczednosciowe.clear()
                        lista_ko_nazwa_banku.clear()
                        lista_ko_numer_konta.clear()
                        lista_ko_wlasciciel.clear()
                        lista_ko_saldo.clear()
                        lista_ko_oprocentowanie.clear()

                        for i, linia in enumerate(linie[1:], start=2):
                            dane = linia.strip().split(";")
                            if len(dane) == 5:
                                nazwa_banku, numer_konta, wlasciciel, saldo_str, oprocentowanie_str = dane
                                
                                if not sprawdz_nazwe_banku(nazwa_banku):
                                    print(f'Niepoprawna nazwa banku w linii {i}: "{linia.strip()}"\n')
                                    return
                                if not sprawdz_nr_konta(numer_konta):
                                    print(f'Niepoprawny numer konta oszczędnościowego w linii {i}: "{linia.strip()}"\n')
                                    return
                                if not sprawdz_nazwe_wlasciciela(wlasciciel):
                                    print(f'Niepoprawna nazwa właściciela w linii {i}: "{linia.strip()}"\n')
                                    return
                                if not sprawdz_saldo(saldo_str):
                                    print(f'Niepoprawne saldo w linii {i}: "{linia.strip()}"\n')
                                    return
                                if not sprawdz_oprocentowanie(oprocentowanie_str):
                                    print(f'Niepoprawne oprocentowanie w linii {i}: "{linia.strip()}"\n')
                                    return
                                
                                saldo = float(saldo_str)
                                oprocentowanie = float(oprocentowanie_str)
                                konto = KontoOszczednosciowe(nazwa_banku, numer_konta, wlasciciel, saldo, oprocentowanie)
                                
                                lista_obiektow_konto_oszczednosciowe.append(konto)
                                lista_ko_nazwa_banku.append(nazwa_banku)
                                lista_ko_numer_konta.append(numer_konta)
                                lista_ko_wlasciciel.append(wlasciciel)
                                lista_ko_saldo.append(saldo)
                                lista_ko_oprocentowanie.append(oprocentowanie)
                        
                        slownik_kont_oszczednosciowych['nazwa banku'] = lista_ko_nazwa_banku
                        slownik_kont_oszczednosciowych['numer konta'] = lista_ko_numer_konta
                        slownik_kont_oszczednosciowych['właściciel'] = lista_ko_wlasciciel
                        slownik_kont_oszczednosciowych['saldo [PLN]'] = lista_ko_saldo
                        slownik_kont_oszczednosciowych['oprocentowanie [%]'] = lista_ko_oprocentowanie
                        
                        print(f'Pomyślnie wczytano {len(lista_obiektow_konto_oszczednosciowe)} kont(a) oszczędnościowych z pliku: "{nazwa_pliku}".\n')
                        return

        except FileNotFoundError:
            print(f'Plik o nazwie "{nazwa_pliku}" nie istnieje. Spróbuj ponownie.\n')
        except Exception as e:
            print(f"Wystąpił błąd podczas odczytu z pliku: {e}. Spróbuj ponownie.\n")







# Program główny
while True:
    try:
        liczba = int(input(
            '―――――――――――――――――――――――――――――――――――――――――――\n                MENU GŁÓWNE\n―――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
            '1 - Przejdź do menu banków\n'
            '2 - Przejdź do menu kont bankowych\n'
            '3 - Przejdź do menu kont oszczędnościowych\n'
            '0 - Zakończ działanie programu\n'))

        if sprawdz_liczbe(liczba, 3):
            if liczba == 1:
                while True:
                    try:
                        wybor = int(input(
                            '―――――――――――――――――――――――――――――――――――――――――――\n                MENU BANKÓW\n―――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                            '1 - Dodaj nowy bank\n'
                            '2 - Usuń wybrany bank\n'
                            '3 - Zarządzaj wybranym bankiem\n'
                            '4 - Pokaż listę utworzonych banków\n'
                            '5 - Wyszukaj bank\n'
                            '6 - Zapisz dane banków do pliku\n'
                            '7 - Odczytaj dane banków z pliku\n'
                            '0 - Wróć do menu głównego\n'))

                        if sprawdz_liczbe(wybor, 7):
                            if wybor == 1:
                                dodaj_bank()

                            if wybor == 2:
                                if not lista_obiektow_bank == []:
                                    usun_bank()
                                else:
                                    print('Nie można usunąć banku, ponieważ nie dodano jeszcze żadnych banków.\n')

                            if wybor == 3:
                                if not lista_obiektow_bank == []:
                                    while True:
                                        try:
                                            edit = int(input(
                                                '――――――――――――――――――――――――――――――――――――――――――――\n          MENU ZARZĄDZANIA BANKIEM\n――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                                                '1 - Zmień nazwę banku\n'
                                                '0 - Wróć\n'))
                                            if sprawdz_liczbe(edit, 1):
                                                if edit == 1:
                                                    edytuj_nazwe_banku_banku()

                                                if edit == 0:
                                                    break
                                        except ValueError:
                                            print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')
                                else:
                                    print('Nie można edytować banku, ponieważ nie dodano jeszcze żadnych banków.\n')

                            if wybor == 4:
                                if not lista_obiektow_bank == []:
                                    pokaz_banki()
                                else:
                                    print('Nie dodano jeszcze żadnych banków.\n')

                            if wybor == 5:
                                if not lista_obiektow_bank == []:
                                    fraza = input("Podaj frazę do wyszukania w nazwie banku:\n").strip().lower()
                                    dopasowane = [bank for bank in lista_obiektow_bank if
                                                  fraza in bank.nazwa_banku.lower()]
                                    if dopasowane:
                                        keys = ['nazwa banku']
                                        sl = dict.fromkeys(keys)

                                        dopasowane_nazwa_banku = []

                                        for bank in dopasowane:
                                            dopasowane_nazwa_banku.append(bank.nazwa_banku)
                                            
                                        sl['nazwa banku'] = dopasowane_nazwa_banku
                                        df = pd.DataFrame(sl)
                                        df.index = range(1, len(df) + 1)
                                        print(f"\nZnaleziono {len(dopasowane)} dopasowanie(a):\n")
                                        print(df)
                                    else:
                                        print("Nie znaleziono banków zawierających podaną frazę.\n")
                                else:
                                    print('Nie można wyszukiwać banków, ponieważ nie dodano jeszcze żadnych banków.\n')

                            if wybor == 6:
                                zapisz_banki_do_pliku()

                            if wybor == 7:
                                odczytaj_banki_z_pliku()

                            if wybor == 0:
                                break
                    except ValueError:
                        print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')

            if liczba == 2:
                while True:
                    try:
                        wybor = int(input(
                            '―――――――――――――――――――――――――――――――――――――――――――――\n             MENU KONT BANKOWYCH\n―――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                            '1 - Dodaj nowe konto bankowe\n'
                            '2 - Usuń wybrane konto bankowe\n'
                            '3 - Zarządzaj wybranym kontem bankowym\n'
                            '4 - Pokaż listę utworzonych kont bankowych\n'
                            '5 - Wyszukaj konto bankowe\n'
                            '6 - Zapisz dane kont bankowych do pliku\n'
                            '7 - Odczytaj dane kont bankowych z pliku\n'
                            '8 - Stwórz konto bankowe na podstawie dodanych banków\n'
                            '0 - Wróć do menu głównego\n'))

                        if sprawdz_liczbe(wybor, 8):
                            if wybor == 1:
                                dodaj_konto_bankowe()

                            if wybor == 2:
                                if not lista_obiektow_konto_bankowe == []:
                                    usun_konto_bankowe()
                                else:
                                    print('Nie można usunąć konta bankowego, ponieważ nie dodano jeszcze żadnych kont bankowych.\n')

                            if wybor == 3:
                                if not lista_obiektow_konto_bankowe == []:
                                    while True:
                                        try:
                                            edit = int(input(
                                                '――――――――――――――――――――――――――――――――――――――――――――\n      MENU ZARZĄDZANIA KONTEM BANKOWYM\n――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                                                '1 - Zmień nazwę banku\n'
                                                '2 - Zmień numer konta bankowego\n'
                                                '3 - Zmień właściciela\n'
                                                '4 - Zmień saldo\n'
                                                '5 - Wpłata\n'
                                                '6 - Wypłata\n'
                                                '7 - Transfer\n'
                                                '0 - Wróć\n'))
                                            if sprawdz_liczbe(edit, 7):
                                                if edit == 1:
                                                    edytuj_nazwe_banku_konta_bankowego()

                                                if edit == 2:
                                                    edytuj_numer_konta_bankowego()

                                                if edit == 3:
                                                    edytuj_wlasciciela_konta_bankowego()

                                                if edit == 4:
                                                    edytuj_saldo_konta_bankowego()

                                                if edit == 5:
                                                    wplata_konto_bankowe()

                                                if edit == 6:
                                                    wyplata_konto_bankowe()

                                                if edit == 7:
                                                    transfer_konto_bankowe()

                                                if edit == 0:
                                                    break
                                        except ValueError:
                                            print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')
                                else:
                                    print(
                                        'Nie można edytować konta bankowego, ponieważ nie dodano jeszcze żadnych kont bankowych.\n')

                            if wybor == 4:
                                if not lista_obiektow_konto_bankowe == []:
                                    pokaz_konta_bankowe()
                                else:
                                    print('Nie dodano jeszcze żadnych kont bankowych.\n')

                            if wybor == 5:
                                if not lista_obiektow_konto_bankowe == []:
                                    while True:
                                        try:
                                            edit = int(input(
                                                '――――――――――――――――――――――――――――――――――――――――――――――\n       MENU WYSZUKIWANIA KONT BANKOWYCH\n――――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                                                '1 - Wyszukaj po nazwie banku\n'
                                                '2 - Wyszukaj po właścicielu konta\n'
                                                '3 - Wyszukaj po numerze konta\n'
                                                '0 - Wróć\n'))
                                            if sprawdz_liczbe(edit, 3):
                                                if edit == 1:
                                                    wyszukaj_konto_bankowe_po_banku()

                                                if edit == 2:
                                                    wyszukaj_konto_bankowe_po_wlascicielu()

                                                if edit == 3:
                                                    wyszukaj_konto_bankowe_po_numerze()

                                                if edit == 0:
                                                    break
                                        except ValueError:
                                            print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')
                                else:
                                    print(
                                        'Nie można wyszukiwać kont bankowych, ponieważ nie dodano jeszcze żadnych kont bankowych.\n')

                            if wybor == 6:
                                zapisz_kb_do_pliku()

                            if wybor == 7:
                                odczytaj_kb_z_pliku()

                            if wybor == 8:
                                stworz_konto_bankowe_na_podstawie_banku()

                            if wybor == 0:
                                break
                    except ValueError:
                        print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')

            if liczba == 3:
                while True:
                    try:
                        wybor = int(input(
                            '―――――――――――――――――――――――――――――――――――――――――――――――――――――\n             MENU KONT OSZCZĘDNOŚCIOWYCH\n―――――――――――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                            '1 - Dodaj nowe konto oszczędnościowe\n'
                            '2 - Usuń wybrane konto oszczędnościowe\n'
                            '3 - Zarządzaj wybranym kontem oszczędnościowym\n'
                            '4 - Pokaż listę utworzonych kont oszczędnościowych\n'
                            '5 - Wyszukaj konto oszczędnościowe\n'
                            '6 - Zapisz dane kont oszczędnościowych do pliku\n'
                            '7 - Odczytaj dane kont oszczędnościowych z pliku\n'
                            '8 - Stwórz konto oszczędnościowe na podstawie dodanych banków\n'
                            '9 - Stwórz konto oszczędnościowe na podstawie dodanych kont bankowych\n'
                            '0 - Wróć do menu głównego\n'))

                        if sprawdz_liczbe(wybor, 9):
                            if wybor == 1:
                                dodaj_konto_oszczednosciowe()

                            if wybor == 2:
                                if not lista_obiektow_konto_oszczednosciowe == []:
                                    usun_konto_oszczednosciowe()
                                else:
                                    print(
                                        'Nie można usunąć konta oszczędnościowego, ponieważ nie dodano jeszcze żadnych kont oszczędnościowych.\n')

                            if wybor == 3:
                                if not lista_obiektow_konto_oszczednosciowe == []:
                                    while True:
                                        try:
                                            edit = int(input(
                                                '――――――――――――――――――――――――――――――――――――――――――――\n  MENU ZARZĄDZANIA KONTEM OSZCZĘDNOŚCIOWYM\n――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                                                '1 - Zmień nazwę banku\n'
                                                '2 - Zmień numer konta oszczędnościowego\n'
                                                '3 - Zmień właściciela\n'
                                                '4 - Zmień saldo\n'
                                                '5 - Zmień oprocentowanie\n'
                                                '6 - Wpłata\n'
                                                '7 - Wypłata\n'
                                                '8 - Transfer\n'
                                                '9 - Nalicz odsetki na konto oszczędnościowe\n'
                                                '0 - Wróć\n'))
                                            if sprawdz_liczbe(edit, 9):
                                                if edit == 1:
                                                    edytuj_nazwe_banku_konta_oszczednosciowego()

                                                if edit == 2:
                                                    edytuj_numer_konta_oszczednosciowego()

                                                if edit == 3:
                                                    edytuj_wlasciciela_konta_oszczednosciowego()

                                                if edit == 4:
                                                    edytuj_saldo_konta_oszczednosciowego()

                                                if edit == 5:
                                                    zmiana_oprocentowania()

                                                if edit == 6:
                                                    wplata_konto_oszczednosciowe()

                                                if edit == 7:
                                                    wyplata_konto_oszczednosciowe()

                                                if edit == 8:
                                                    transfer_konto_oszczednosciowe()

                                                if edit == 9:
                                                    naliczanie_odsetek()

                                                if edit == 0:
                                                    break
                                        except ValueError:
                                            print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')
                                else:
                                    print(
                                        'Nie można edytować konta oszczędnościowego, ponieważ nie dodano jeszcze żadnych kont oszczędnościowych.\n')

                            if wybor == 4:
                                if not lista_obiektow_konto_oszczednosciowe == []:
                                    pokaz_konta_oszczednosciowe()
                                else:
                                    print('Nie dodano jeszcze żadnych kont oszczędnościowych.\n')

                            if wybor == 5:
                                if not lista_obiektow_konto_oszczednosciowe == []:
                                    while True:
                                        try:
                                            edit = int(input(
                                                '――――――――――――――――――――――――――――――――――――――――――――――――\n    MENU WYSZUKIWANIA KONT OSZCZĘDNOŚCIOWYCH\n――――――――――――――――――――――――――――――――――――――――――――――――\nWybierz co chcesz zrobić (wpisz liczbę):\n'
                                                '1 - Wyszukaj po nazwie banku\n'
                                                '2 - Wyszukaj po właścicielu konta\n'
                                                '3 - Wyszukaj po numerze konta\n'
                                                '0 - Wróć\n'))
                                            if sprawdz_liczbe(edit, 3):
                                                if edit == 1:
                                                    wyszukaj_konto_oszczednosciowe_po_banku()

                                                if edit == 2:
                                                    wyszukaj_konto_oszczednosciowe_po_wlascicielu()

                                                if edit == 3:
                                                    wyszukaj_konto_oszczednosciowe_po_numerze()

                                                if edit == 0:
                                                    break
                                        except ValueError:
                                            print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')
                                else:
                                    print(
                                        'Nie można wyszukiwać kont oszczędnościowych, ponieważ nie dodano jeszcze żadnych kont oszczędnościowych.\n')

                            if wybor == 6:
                                zapisz_ko_do_pliku()

                            if wybor == 7:
                                odczytaj_ko_z_pliku()

                            if wybor == 8:
                                stworz_konto_oszczednosciowe_na_podstawie_banku()

                            if wybor == 9:
                                stworz_konto_oszczednosciowe_na_podstawie_konta_bankowego()

                            if wybor == 0:
                                break
                    except ValueError:
                        print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')

            if liczba == 0:
                print('Zakończono pracę programu.')
                break
    except ValueError:
        print('Nie podano liczby całkowitej. Spróbuj ponownie.\n')