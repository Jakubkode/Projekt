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


