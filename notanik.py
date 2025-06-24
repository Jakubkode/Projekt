from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

punkty_turystyczne = []
przewodnicy = []
klienci = []

class PunktTurystyczny:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Punkt: {self.nazwa}")

    def pobierz_wspolrzedne(self):
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

class Przewodnik:
    def __init__(self, imie, nazwisko, punkt):
        self.imie = imie
        self.nazwisko = nazwisko
        self.punkt = punkt
        self.wspolrzedne = punkt.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Przewodnik: {self.imie} {self.nazwisko}")

class Klient:
    def __init__(self, imie, punkt):
        self.imie = imie
        self.punkt = punkt
        self.wspolrzedne = punkt.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Klient: {self.imie}")

# ===== FUNKCJE ODSWIEZANIA
def odswiez_comboboxy():
    nazwy = [p.nazwa for p in punkty_turystyczne]
    combobox_punkt_dla_przewodnika['values'] = nazwy
    combobox_punkt_dla_klienta['values'] = nazwy
    combobox_punkt_na_mapie['values'] = nazwy

# ===== DODAWANIE I USUWANIE
def dodaj_punkt():
    nazwa = entry_nazwa_punktu.get()
    lokalizacja = entry_lokalizacja_punktu.get()
    if nazwa and lokalizacja:
        punkt = PunktTurystyczny(nazwa, lokalizacja)
        punkty_turystyczne.append(punkt)
        listbox_punkty.insert(END, f"{punkt.nazwa} ({punkt.lokalizacja})")
        entry_nazwa_punktu.delete(0, END)
        entry_lokalizacja_punktu.delete(0, END)
        odswiez_comboboxy()

def usun_punkt():
    idx = listbox_punkty.curselection()
    if idx:
        i = idx[0]
        punkty_turystyczne[i].marker.delete()
        punkty_turystyczne.pop(i)
        listbox_punkty.delete(i)
        odswiez_comboboxy()

def dodaj_przewodnika():
    imie = entry_imie_przewodnika.get()
    nazwisko = entry_nazwisko_przewodnika.get()
    idx = combobox_punkt_dla_przewodnika.current()
    if idx >= 0:
        przewodnik = Przewodnik(imie, nazwisko, punkty_turystyczne[idx])
        przewodnicy.append(przewodnik)
        listbox_przewodnicy.insert(END, f"{imie} {nazwisko}")
        entry_imie_przewodnika.delete(0, END)
        entry_nazwisko_przewodnika.delete(0, END)

def usun_przewodnika():
    idx = listbox_przewodnicy.curselection()
    if idx:
        i = idx[0]
        przewodnicy[i].marker.delete()
        przewodnicy.pop(i)
        listbox_przewodnicy.delete(i)

def dodaj_klienta():
    imie = entry_imie_klienta.get()
    idx = combobox_punkt_dla_klienta.current()
    if idx >= 0:
        klient = Klient(imie, punkty_turystyczne[idx])
        klienci.append(klient)
        listbox_klienci.insert(END, imie)
        entry_imie_klienta.delete(0, END)

def usun_klienta():
    idx = listbox_klienci.curselection()
    if idx:
        i = idx[0]
        klienci[i].marker.delete()
        klienci.pop(i)
        listbox_klienci.delete(i)

# ===== MAPA
def czysc_markery():
    for x in punkty_turystyczne + przewodnicy + klienci:
        if hasattr(x, 'marker'):
            x.marker.delete()

def pokaz_wszystkie_punkty():
    czysc_markery()
    for p in punkty_turystyczne:
        p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"Punkt: {p.nazwa}")

def pokaz_wszystkich_przewodnikow():
    czysc_markery()
    for p in przewodnicy:
        p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"Przewodnik: {p.imie} {p.nazwisko}")

def pokaz_klientow_punktu():
    czysc_markery()
    idx = combobox_punkt_na_mapie.current()
    if idx >= 0:
        punkt = punkty_turystyczne[idx]
        for k in klienci:
            if k.punkt == punkt:
                k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"Klient: {k.imie}")

def pokaz_przewodnikow_punktu():
    czysc_markery()
    idx = combobox_punkt_na_mapie.current()
    if idx >= 0:
        punkt = punkty_turystyczne[idx]
        for p in przewodnicy:
            if p.punkt == punkt:
                p.marker = map_widget.set_marker(p.wspolrzedne[0], p.wspolrzedne[1], text=f"Przewodnik: {p.imie} {p.nazwisko}")

# ===== GUI
root = Tk()
root.geometry("1200x800")
root.title("System zarządzania punktami turystycznymi i przewodnikami")

# === RAMKI
frame_punkt = Frame(root); frame_punkt.grid(row=0, column=0, sticky=N, padx=10)
frame_przewodnik = Frame(root); frame_przewodnik.grid(row=0, column=1, sticky=N, padx=10)
frame_klient = Frame(root); frame_klient.grid(row=0, column=2, sticky=N, padx=10)
frame_kontrola = Frame(root); frame_kontrola.grid(row=1, column=0, columnspan=3, pady=10)
frame_mapa = Frame(root); frame_mapa.grid(row=2, column=0, columnspan=3)

# === PUNKTY
Label(frame_punkt, text="Dodaj punkt turystyczny").pack()
entry_nazwa_punktu = Entry(frame_punkt); entry_nazwa_punktu.pack()
entry_lokalizacja_punktu = Entry(frame_punkt); entry_lokalizacja_punktu.pack()
Button(frame_punkt, text="Dodaj punkt", command=dodaj_punkt).pack()
Button(frame_punkt, text="Usuń punkt", command=usun_punkt).pack()
listbox_punkty = Listbox(frame_punkt, width=30); listbox_punkty.pack()

# === PRZEWODNICY
Label(frame_przewodnik, text="Dodaj przewodnika").pack()
entry_imie_przewodnika = Entry(frame_przewodnik); entry_imie_przewodnika.pack()
entry_nazwisko_przewodnika = Entry(frame_przewodnik); entry_nazwisko_przewodnika.pack()
combobox_punkt_dla_przewodnika = ttk.Combobox(frame_przewodnik); combobox_punkt_dla_przewodnika.pack()
Button(frame_przewodnik, text="Dodaj przewodnika", command=dodaj_przewodnika).pack()
Button(frame_przewodnik, text="Usuń przewodnika", command=usun_przewodnika).pack()
listbox_przewodnicy = Listbox(frame_przewodnik, width=30); listbox_przewodnicy.pack()

# === KLIENCI
Label(frame_klient, text="Dodaj klienta").pack()
entry_imie_klienta = Entry(frame_klient); entry_imie_klienta.pack()
combobox_punkt_dla_klienta = ttk.Combobox(frame_klient); combobox_punkt_dla_klienta.pack()
Button(frame_klient, text="Dodaj klienta", command=dodaj_klienta).pack()
Button(frame_klient, text="Usuń klienta", command=usun_klienta).pack()
listbox_klienci = Listbox(frame_klient, width=30); listbox_klienci.pack()

# === KONTROLA MAPY
Label(frame_kontrola, text="Punkt:").grid(row=0, column=0)
combobox_punkt_na_mapie = ttk.Combobox(frame_kontrola, width=25); combobox_punkt_na_mapie.grid(row=0, column=1)

Button(frame_kontrola, text="Pokaż wszystkie punkty", command=pokaz_wszystkie_punkty).grid(row=1, column=0, padx=5)
Button(frame_kontrola, text="Pokaż wszystkich przewodników", command=pokaz_wszystkich_przewodnikow).grid(row=1, column=1, padx=5)
Button(frame_kontrola, text="Pokaż klientów punktu", command=pokaz_klientow_punktu).grid(row=1, column=2, padx=5)
Button(frame_kontrola, text="Pokaż przewodników punktu", command=pokaz_przewodnikow_punktu).grid(row=1, column=3, padx=5)

# === MAPA
map_widget = tkintermapview.TkinterMapView(frame_mapa, width=1150, height=500)
map_widget.set_position(52.23, 21.0); map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()
