import sqlite3
import tkinter as tk
from tkinter import messagebox
import math

class CalcolatriceScientifica:
    def __init__(self, root, username="Utente"):
        self.root = root
        self.username = username
        self.root.title("Calcolatrice Scientifica")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e24")
        self.root.resizable(False, False)

        self.espressione = "" 
        
        #Schermo di visualizzazione
        self.risultato = tk.Entry(
            root, font=("Segoe UI", 24), bg="#2b2b36", fg="#ffffff", 
            bd=0, justify="right", insertbackground="#ffffff", relief="flat"
        )
        self.risultato.pack(fill="both", ipadx=8, ipady=18, padx=15, pady=15)
        self.risultato.insert(0, "0")

        #Contenitore dei pulsanti
        self.buttons_frame = tk.Frame(root, bg="#1e1e24")
        self.buttons_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        #Griglia dei pulsanti
        pulsanti = [
            ('sin', 0, 0, '#3b3b4a', 'sci'), ('cos', 0, 1, '#3b3b4a', 'sci'), ('tan', 0, 2, '#3b3b4a', 'sci'), ('π', 0, 3, '#3b3b4a', 'sci'), ('C', 0, 4, '#e53935', 'clear'),
            ('x²', 1, 0, '#3b3b4a', 'sci'), ('√', 1, 1, '#3b3b4a', 'sci'), ('^', 1, 2, '#3b3b4a', 'sci'), ('n!', 1, 3, '#3b3b4a', 'sci'), ('/', 1, 4, '#00adb5', 'op'),
            ('7', 2, 0, '#2b2b36', 'num'), ('8', 2, 1, '#2b2b36', 'num'), ('9', 2, 2, '#2b2b36', 'num'), ('(', 2, 3, '#3b3b4a', 'op'), ('*', 2, 4, '#00adb5', 'op'),
            ('4', 3, 0, '#2b2b36', 'num'), ('5', 3, 1, '#2b2b36', 'num'), ('6', 3, 2, '#2b2b36', 'num'), (')', 3, 3, '#3b3b4a', 'op'), ('-', 3, 4, '#00adb5', 'op'),
            ('1', 4, 0, '#2b2b36', 'num'), ('2', 4, 1, '#2b2b36', 'num'), ('3', 4, 2, '#2b2b36', 'num'), ('log', 4, 3, '#3b3b4a', 'sci'), ('+', 4, 4, '#00adb5', 'op'),
            ('0', 5, 0, '#2b2b36', 'num'), ('.', 5, 1, '#2b2b36', 'num'), ('EXP', 5, 2, '#3b3b4a', 'sci'), ('ln', 5, 3, '#3b3b4a', 'sci'), ('=', 5, 4, '#2e7d32', 'op')
        ]

        for i in range(6): #Genera x la griglia
            self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(5):
            self.buttons_frame.columnconfigure(j, weight=1)

        for testo, riga, colonna, colore, tipo in pulsanti:
            btn = tk.Button(
                self.buttons_frame, text=testo, font=("Segoe UI", 11),
                bg=colore, fg="white", activebackground="#4a4a5a", activeforeground="white",
                bd=0, relief="flat", cursor="hand2", command=lambda t=testo, tp=tipo: self.gestisci_pressione(t, tp)
            ) #Creazione pulsante
            btn.grid(row=riga, column=colonna, sticky="nsew", padx=2, pady=2)

    def gestisci_pressione(self, testo, tipo):
        """Gestisce la pressione dei bottoni"""
        if tipo == 'clear':
            self.espressione = ""
            self.aggiorna_schermo("0")
        
        elif testo == '=':
            try:
                expr_elaborata = self.espressione.replace('^', '**').replace('π', str(math.pi))
                risultato = eval(expr_elaborata)
                
                #Arrotonda per evitare errori di floating point
                if isinstance(risultato, float):
                    risultato = round(risultato, 10)

                #Salva nel DB
                self.salva_cronologia(self.espressione, risultato)
                
                self.aggiorna_schermo(str(risultato))
                self.espressione = str(risultato)
            except ZeroDivisionError:
                messagebox.showerror("Errore", "Impossibile dividere per zero!")
                self.pulisci_schermo()
            except Exception:
                messagebox.showerror("Errore", "Espressione non valida")
                self.pulisci_schermo()

        elif tipo == 'sci':
            try:
                valore_attuale = float(self.risultato.get()) if self.risultato.get() else 0.0
                
                if testo == 'sin':
                    risultato = math.sin(math.radians(valore_attuale))
                elif testo == 'cos':
                    risultato = math.cos(math.radians(valore_attuale))
                elif testo == 'tan':
                    risultato = math.tan(math.radians(valore_attuale))
                elif testo == '√':
                    risultato = math.sqrt(valore_attuale)
                elif testo == 'x²':
                    risultato = valore_attuale ** 2
                elif testo == 'n!':
                    risultato = math.factorial(int(valore_attuale))
                elif testo == 'log':
                    risultato = math.log10(valore_attuale)
                elif testo == 'ln':
                    risultato = math.log(valore_attuale)
                elif testo == 'π':
                    self.espressione += str(math.pi)
                    self.aggiorna_schermo(self.espressione)
                    return
                elif testo == 'EXP':
                    self.espressione += "*10**"
                    self.aggiorna_schermo(self.espressione)
                    return

                self.aggiorna_schermo(str(round(risultato, 10)))
                self.espressione = str(round(risultato, 10))
            except Exception:
                messagebox.showerror("Errore", "Operazione scientifica non valida sul valore attuale")
                self.pulisci_schermo()

        else:  #Numeri e Operatori standard
            if self.risultato.get() == "0" and tipo == 'num':
                self.espressione = testo
            else:
                self.espressione += str(testo)
            self.aggiorna_schermo(self.espressione)

    def aggiorna_schermo(self, testo):
        """Aggiorna il display"""
        self.risultato.delete(0, tk.END)
        self.risultato.insert(tk.END, testo)

    def pulisci_schermo(self):
        """Pulisce lo schermo"""
        self.espressione = ""
        self.aggiorna_schermo("0")
    
    def salva_cronologia(self, espressione, risultato):
        """Salva il calcolo nel database SQLite"""
        try:
            #Connessione a SQLite
            connessione = sqlite3.connect("calcolatrice.db")
            cursore = connessione.cursor()
            
            #Leggi la cronologia attuale
            query_select = "SELECT cronologia FROM utenti WHERE nome = ?"
            cursore.execute(query_select, (self.username,))
            risultato_query = cursore.fetchone()

            cronologia_attuale = ""
            if risultato_query and risultato_query[0]:
                cronologia_attuale = risultato_query[0]

            #Crea la nuova riga di testo puro per salvare la cronologia
            nuovo_calcolo = f"{espressione} = {risultato}"

            # Se c'è già testo, aggiungi il nuovo calcolo andando a capo
            if cronologia_attuale:
                cronologia_aggiornata = f"{cronologia_attuale}\n{nuovo_calcolo}"
            else:
                cronologia_aggiornata = nuovo_calcolo

            # Aggiorna il database
            query_update = "UPDATE utenti SET cronologia = ? WHERE nome = ?"
            cursore.execute(query_update, (cronologia_aggiornata, self.username))
            connessione.commit()

        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
        finally:
            if 'connessione' in locals():
                cursore.close()
                connessione.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Avvio non consentito",
        "Non puoi avviare direttamente questo file.\nEffettua prima il login tramite CalcoDB.py"
    )
    root.destroy()