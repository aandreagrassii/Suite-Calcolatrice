import sqlite3
import tkinter as tk
from tkinter import messagebox

class CalcolatriceConvertitrice:
    def __init__(self, root, username="Utente"):
        self.root = root
        self.username = username
        self.root.title("Convertitore di Basi")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e24")
        self.root.resizable(False, False)

        #Titolo
        self.titolo = tk.Label(root, text="Convertitore Bin/Dec/Hex/Oct", font=("Segoe UI", 14), bg="#1e1e24", fg="#ffffff")
        self.titolo.pack(pady=(20, 10))

        # Box Input
        self.label_input = tk.Label(root, text="Inserisci il valore:", bg="#1e1e24", fg="#b0b0b0", font=("Segoe UI", 10))
        self.label_input.pack(pady=(5, 2))
        self.entry_input = tk.Entry(root, font=("Segoe UI", 14), justify="center", bg="#2b2b36", fg="#ffffff", insertbackground="white", bd=0, relief="flat")
        self.entry_input.pack(pady=5, ipady=6, fill="x", padx=40)

        # Frame Scelta Base di Partenza
        self.frame_basi = tk.LabelFrame(root, text=" Base di partenza ", bg="#1e1e24", fg="#b0b0b0", font=("Segoe UI", 9), padx=15, pady=10, bd=1, relief="solid")
        self.frame_basi.pack(pady=15, fill="x", padx=40)

        self.base_selezionata = tk.StringVar(value="DEC")
        basi = [("Decimale (10)", "DEC"), ("Binario (2)", "BIN"), ("Esadecimale (16)", "HEX"), ("Ottale (8)", "OCT")]
        
        for testo, valore in basi:
            rb = tk.Radiobutton(
                self.frame_basi, text=testo, variable=self.base_selezionata, value=valore, 
                bg="#1e1e24", fg="#ffffff", selectcolor="#1e1e24", activebackground="#1e1e24", 
                activeforeground="#ffffff", font=("Segoe UI", 10), cursor="hand2"
            )
            rb.pack(anchor="w", pady=2)

        # Pulsante per convertire
        self.btn_converti = tk.Button(
            root, text="CONVERTI", font=("Segoe UI", 10), bg="#2e7d32", fg="white", 
            activebackground="#1b5e20", activeforeground="white", bd=0, relief="flat", 
            cursor="hand2", command=self.esegui_conversione
        )
        self.btn_converti.pack(pady=15, fill="x", padx=40, ipady=8)

        # Area Risultati
        self.frame_risultati = tk.Frame(root, bg="#2b2b36", padx=15, pady=10)
        self.frame_risultati.pack(pady=10, fill="x", padx=40)

        self.label_dec = tk.Label(self.frame_risultati, text="DEC: ", font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", anchor="w")
        self.label_dec.pack(fill="x", pady=2)
        self.label_bin = tk.Label(self.frame_risultati, text="BIN: ", font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", anchor="w")
        self.label_bin.pack(fill="x", pady=2)
        self.label_hex = tk.Label(self.frame_risultati, text="HEX: ", font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", anchor="w")
        self.label_hex.pack(fill="x", pady=2)
        self.label_oct = tk.Label(self.frame_risultati, text="OCT: ", font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", anchor="w")
        self.label_oct.pack(fill="x", pady=2)

    def esegui_conversione(self):
        """Esegue la conversione tra basi numeriche"""
        stringa_input = self.entry_input.get().strip()
        if not stringa_input:
            messagebox.showerror("Errore", "Inserisci un valore da convertire!")
            return

        base_partenza = self.base_selezionata.get()

        try:
            # 1. Converti l'input in un intero decimale temporaneo
            if base_partenza == "DEC":
                valore_decimale = int(stringa_input, 10)
            elif base_partenza == "BIN":
                valore_decimale = int(stringa_input, 2)
            elif base_partenza == "HEX":
                valore_decimale = int(stringa_input, 16)
            elif base_partenza == "OCT":
                valore_decimale = int(stringa_input, 8)
        except ValueError:
            messagebox.showerror("Errore", f"Il valore inserito non è valido per la base {base_partenza}!")
            return

        # 2. Genera le rappresentazioni nelle varie basi
        res_dec = str(valore_decimale)
        res_bin = bin(valore_decimale)[2:]  # Toglie il prefisso '0b'
        res_hex = hex(valore_decimale)[2:].upper()  # Toglie '0x' e rende maiuscolo
        res_oct = oct(valore_decimale)[2:]  # Toglie '0o'

        # 3. Aggiorna l'interfaccia grafica
        self.label_dec.config(text=f"DEC: {res_dec}")
        self.label_bin.config(text=f"BIN: {res_bin}")
        self.label_hex.config(text=f"HEX: {res_hex}")
        self.label_oct.config(text=f"OCT: {res_oct}")

        # 4. Salva il calcolo nel database (con formato pulito a testo)
        espressione_salvataggio = f"Convertito {stringa_input} ({base_partenza})"
        risultato_salvataggio = f"DEC:{res_dec} | BIN:{res_bin} | HEX:{res_hex} | OCT:{res_oct}"
        self.salva_cronologia(espressione_salvataggio, risultato_salvataggio)

    def salva_cronologia(self, espressione, risultato):
        """Salva la conversione nel database SQLite come testo puro"""
        try:
            # Connessione a SQLite
            connessione = sqlite3.connect("calco.db")
            cursore = connessione.cursor()

            # 1. Leggi il testo della cronologia attuale
            query_select = "SELECT cronologia FROM utenti WHERE nome = ?"
            cursore.execute(query_select, (self.username,))
            risultato_query = cursore.fetchone()

            cronologia_attuale = ""
            if risultato_query and risultato_query[0]:
                cronologia_attuale = risultato_query[0]

            # 2. Crea la nuova riga di testo puro
            nuovo_calcolo = f"{espressione} = {risultato}"

            # 3. Se c'è già del testo, aggiungi il nuovo calcolo andando a capo (\n)
            if cronologia_attuale:
                cronologia_aggiornata = f"{cronologia_attuale}\n{nuovo_calcolo}"
            else:
                cronologia_aggiornata = nuovo_calcolo

            # 4. Aggiorna il database salvando il testo normale
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
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Avvio non consentito",
        "Non puoi avviare direttamente questo file.\nEffettua prima il login tramite CalcoDB.py"
    )
    root.destroy()