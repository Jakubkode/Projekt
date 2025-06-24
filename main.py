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

