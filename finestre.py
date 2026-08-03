import tkinter as tk

from calcolatriceScientifica import CalcolatriceScientifica
from calcolatriceNormale import Calcolatrice
from calcolatriceConvertitrice import CalcolatriceConvertitrice

class finestraSelezione:
    def __init__(self, finestraMain, username):
        self.finestraMain = finestraMain
        self.username = username #Passato dal dataabase
        self.finestraMain.title("Seleziona Calcolatrice") 
        self.finestraMain.geometry("400x600")
        self.finestraMain.configure(bg="#1e1e24")

        lbl_welcome = tk.Label(
            self.finestraMain, text=f"Ciao, {self.username}!", 
            font=("Segoe UI", 16), bg="#1e1e24", fg="#ffffff"
        )
        lbl_welcome.pack(pady=(40, 10))

        lbl_sub = tk.Label(
            self.finestraMain, text="Scegli la modalità di utilizzo:", 
            font=("Segoe UI", 10), bg="#1e1e24", fg="#b0b0b0"
        )
        lbl_sub.pack(pady=(0, 30))

        #Configurazione pulsanti
        btn_style = {
            "font": ("Segoe UI", 10),
            "bg": "#2b2b36",
            "fg": "#ffffff",
            "activebackground": "#3b3b4a",
            "activeforeground": "#ffffff",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2"
        }

        self.pulsante2 = tk.Button(self.finestraMain, text="Calcolatrice Standard", command=self.pulsanteNormale, **btn_style)
        self.pulsante2.pack(fill="x", padx=40, ipady=12, pady=10)

        self.pulsante1 = tk.Button(self.finestraMain, text="Calcolatrice Scientifica", command=self.pulsanteScientifica, **btn_style)
        self.pulsante1.pack(fill="x", padx=40, ipady=12, pady=10)

        self.pulsante3 = tk.Button(self.finestraMain, text="Convertitore di Basi", command=self.pulsanteConvertitrice, **btn_style)
        self.pulsante3.pack(fill="x", padx=40, ipady=12, pady=10)

    def pulsanteScientifica(self):
        for widget in self.finestraMain.winfo_children(): #Rimuove tutti i widget dalla finestra principale
            widget.destroy()
        self.app = CalcolatriceScientifica(self.finestraMain, self.username) #Crea istanza

    def pulsanteNormale(self):
        for widget in self.finestraMain.winfo_children():
            widget.destroy()
        self.app = Calcolatrice(self.finestraMain, self.username)
    
    def pulsanteConvertitrice(self):
        for widget in self.finestraMain.winfo_children():
            widget.destroy()
        self.app = CalcolatriceConvertitrice(self.finestraMain, self.username)