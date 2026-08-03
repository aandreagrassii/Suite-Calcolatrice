import sqlite3
import tkinter as tk
from tkinter import messagebox

class Calcolatrice:
    def __init__(self, master, username="Utente"):
        self.master = master
        self.username = username
        self.master.title("Calcolatrice Standard")
        self.master.geometry("400x600")
        self.master.configure(bg="#1e1e24")
        self.espressione = ""

        #Schermo di visualizzazione
        self.risultato = tk.Entry(
            master, font=("Segoe UI", 28), bg="#2b2b36", fg="#ffffff", 
            bd=0, justify="right", insertbackground="white", relief="flat"
        )
        self.risultato.pack(fill="both", ipadx=8, ipady=20, padx=20, pady=(25, 15))
        self.risultato.insert(0, "0")

        #Container dei pulsanti
        self.buttons_frame = tk.Frame(master, bg="#1e1e24")
        self.buttons_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        #Griglia dei pulsanti
        pulsanti = [
            ('C', 0, 0, '#e53935', 'clear'), ('⌫', 0, 1, '#d84315', 'backspace'), ('%', 0, 2, '#3b3b4a', 'op'), ('/', 0, 3, '#00adb5', 'op'),
            ('7', 1, 0, '#2b2b36', 'num'), ('8', 1, 1, '#2b2b36', 'num'), ('9', 1, 2, '#2b2b36', 'num'), ('*', 1, 3, '#00adb5', 'op'),
            ('4', 2, 0, '#2b2b36', 'num'), ('5', 2, 1, '#2b2b36', 'num'), ('6', 2, 2, '#2b2b36', 'num'), ('-', 2, 3, '#00adb5', 'op'),
            ('1', 3, 0, '#2b2b36', 'num'), ('2', 3, 1, '#2b2b36', 'num'), ('3', 3, 2, '#2b2b36', 'num'), ('+', 3, 3, '#00adb5', 'op'),
            ('0', 4, 0, '#2b2b36', 'num'), ('.', 4, 1, '#2b2b36', 'num'), ('=', 4, 2, '#2e7d32', 'op')
        ]

        for i in range(5): #Genera x la griglia
            self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.buttons_frame.columnconfigure(j, weight=1)

        for testo, riga, colonna, colore, tipo in pulsanti:
            fg_color = "white"
            active_bg = "#4a4a5a"
            
            if tipo == 'clear':
                active_bg = "#c62828"
            elif tipo == 'backspace':
                active_bg = "#bf360c"
            elif testo == '=':
                active_bg = "#1b5e20"

            btn = tk.Button(
                self.buttons_frame, text=testo, font=("Segoe UI", 12),
                bg=colore, fg=fg_color, activebackground=active_bg, activeforeground="white",
                bd=0, relief="flat", cursor="hand2", command=lambda t=testo, tp=tipo: self.gestisci_pressioni(t, tp)
            )
            
            # Posizionamento speciale del pulsante '='
            if testo == '=':
                btn.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)
            else:
                btn.grid(row=riga, column=colonna, sticky="nsew", padx=3, pady=3)

    def gestisci_pressioni(self, testo, tipo):
        """Gestisce la pressione dei bottoni"""
        if tipo == 'clear':
            self.espressione = ""
            self.aggiorna_schermo("0")
            
        elif tipo == 'backspace':
            # Rimuove l'ultimo numero / carattere
            if len(self.espressione) > 0:
                self.espressione = self.espressione[:-1]
            
            if self.espressione == "":
                self.aggiorna_schermo("0")
            else:
                self.aggiorna_schermo(self.espressione)
                
        elif testo == '=':
            try:
                expr_pulita = self.espressione.replace('%', '/100')
                risultato_numerico = eval(expr_pulita)
                if isinstance(risultato_numerico, float):
                    risultato_numerico = round(risultato_numerico, 10)

                self.salva_cronologia(self.espressione, risultato_numerico)
                self.aggiorna_schermo(str(risultato_numerico))
                self.espressione = str(risultato_numerico)
            except ZeroDivisionError:
                messagebox.showerror("Errore", "Impossibile dividere per zero!")
                self.pulisci_schermo()
            except Exception:
                messagebox.showerror("Errore", "Espressione non valida!")
                self.pulisci_schermo()
        else:
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
            # Connessione a SQLite
            connessione = sqlite3.connect("calco.db")
            cursore = connessione.cursor()

            # Leggi la cronologia attuale
            query_select = "SELECT cronologia FROM utenti WHERE nome = ?"
            cursore.execute(query_select, (self.username,))
            risultato_query = cursore.fetchone()

            cronologia_attuale = ""
            if risultato_query and risultato_query[0]:
                cronologia_attuale = risultato_query[0]

            # Crea la nuova riga di testo puro
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
    master = tk.Tk()
    master.withdraw()
    messagebox.showerror(
        "Avvio non consentito",
        "Non puoi avviare direttamente questo file.\nEffettua prima il login tramite CalcoDB.py"
    )
    master.destroy()