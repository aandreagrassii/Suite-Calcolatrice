import sqlite3 #Modulo DB
import tkinter as tk #GUI
from tkinter import messagebox
from finestre import finestraSelezione
import hashlib #Hash
import os #Gestisce percorsi

#Funzioni per hashare le password
def hash_password(password):
    """
    Hasha una password usando SHA-256 con salt.
    """
    #Genera un salt casuale
    salt = os.urandom(32)
    
    # Hasha password + salt
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    #Ritorna salt + hash concatenati (codificati in hex)
    return (salt + password_hash).hex()


def verify_password(password, password_hash):
    """
    Verifica se la password inserita corrisponde all'hash salvato.
    """
    #Decodifica l'hex
    hash_bytes = bytes.fromhex(password_hash)
    #Estrae il salt (primi 32 bytes)
    salt = hash_bytes[:32]

    #Hasha la password inserita con lo stesso salt
    password_check_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    #Confronta (ultimi 32 bytes dell'hash salvato)
    return hash_bytes[32:] == password_check_hash


class Gui:
    def __init__(self, god):
        self.god = god #Finestra principale
        self.god.title("Calcolatrice - Accesso")
        self.god.geometry("400x600")
        self.god.configure(bg="#1e1e24")

        #FORM di login / registrazione
        form_frame = tk.Frame(god, bg="#1e1e24")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(form_frame, text="BENVENUTO", font=("Segoe UI", 16), bg="#1e1e24", fg="#ffffff")
        title_label.pack(pady=(0, 20))

        self.label_utente = tk.Label(form_frame, text="Nome utente", font=("Segoe UI", 10), bg="#1e1e24", fg="#b0b0b0", anchor="w")
        self.label_utente.pack(fill="x", pady=(5, 2))
        
        self.entry_utente = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", insertbackground="white", bd=0, relief="flat")
        self.entry_utente.pack(fill="x", ipady=6, pady=(0, 15))

        self.label_password = tk.Label(form_frame, text="Password", font=("Segoe UI", 10), bg="#1e1e24", fg="#b0b0b0", anchor="w")
        self.label_password.pack(fill="x", pady=(5, 2))
        
        self.entry_password = tk.Entry(form_frame, show="*", font=("Segoe UI", 11), bg="#2b2b36", fg="#ffffff", insertbackground="white", bd=0, relief="flat")
        self.entry_password.pack(fill="x", ipady=6, pady=(0, 20))
        
        # Pulsante di Login
        self.loginButton = tk.Button(
            form_frame, text="Accedi", font=("Segoe UI", 10), bg="#00adb5", fg="#ffffff", 
            activebackground="#008c93", activeforeground="#ffffff", bd=0, relief="flat", 
            cursor="hand2", command=self.verificaLogin
        )
        self.loginButton.pack(fill="x", ipady=8, pady=(0, 10))

        # Pulsante di Registrazione
        self.registerButton = tk.Button(
            form_frame, text="Registrati", font=("Segoe UI", 10), bg="#2b2b36", fg="#ffffff", 
            activebackground="#3b3b4a", activeforeground="#ffffff", bd=0, relief="flat", 
            cursor="hand2", command=self.registraUtente
        )
        self.registerButton.pack(fill="x", ipady=8)

    def verificaLogin(self):
        """Controlla le credenziali nel database"""
        utente = self.entry_utente.get().strip()
        password = self.entry_password.get().strip()

        if not utente or not password: #Se non è stato inserito nome utente o password
            messagebox.showerror("Errore", "Inserisci nome utente e password!")
            return
        
        try:
            #Connessione a SQLite
            connessione = sqlite3.connect("calco.db")
            cursore = connessione.cursor()
            
            query = "SELECT password FROM utenti WHERE nome = ?"
            cursore.execute(query, (utente,))
            risultato = cursore.fetchone()
            
            if risultato:
                password_hash_salvato = risultato[0] #Estrae l'hash dal database
                # Verifica se la password inserita corrisponde all'hash
                if verify_password(password, password_hash_salvato):
                    messagebox.showinfo("Successo", "Login effettuato con successo!")
                    for widget in self.god.winfo_children():
                        widget.destroy()
                    #Passa il nome utente alla classe finestraSelezione (finestre.py)
                    self.app = finestraSelezione(self.god, utente)
                    self.god.update()
                else:
                    messagebox.showerror("Errore", "Nome utente o password errati!")
            else:
                messagebox.showerror("Errore", "Nome utente o password errati!")
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la connessione al database: {e}")
        finally:
            if 'connessione' in locals():
                cursore.close()
                connessione.close()

    def registraUtente(self):
        """Registra un nuovo utente salvando la password hashata"""
        utente = self.entry_utente.get().strip()
        password = self.entry_password.get().strip()

        if not utente or not password:
            messagebox.showerror("Errore", "Compila sia il nome utente che la password!")
            return

        try:
            connessione = sqlite3.connect("calco.db")
            cursore = connessione.cursor()

            # Hasha la password del nuovo utente
            password_hashata = hash_password(password)

            query = "INSERT INTO utenti (nome, password) VALUES (?, ?)"
            cursore.execute(query, (utente, password_hashata))
            connessione.commit()

            messagebox.showinfo("Successo", f"Utente '{utente}' registrato con successo!\nOra puoi effettuare l'accesso.")
            
            # Pulisce i campi di input
            self.entry_utente.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)

        except sqlite3.IntegrityError:
            messagebox.showerror("Errore", "Nome utente già esistente! Scegli un altro nome.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la registrazione: {e}")
        finally:
            if 'connessione' in locals():
                cursore.close()
                connessione.close()


#Mostra il percorso esatto dove il database verrà salvato
percorso_database = os.path.abspath("calco.db")
print(f"Percorso database: {percorso_database}")

try:
    connessione = sqlite3.connect("calco.db")
    cursore = connessione.cursor()
    
    #Crea la tabella se non esiste
    tabella_sql = """
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        cronologia TEXT
    )
    """
    cursore.execute(tabella_sql)
    print("Tabella 'utenti' creata/verificata con successo!")
    print(f"Database disponibile a: {percorso_database}")

    #Inserisce un utente standard di prova (se non esiste già)
    #La password viene HASHATA prima di salvarla
    password_hashata = hash_password("password123")
    
    query = "INSERT INTO utenti (nome, password) VALUES (?, ?)"
    dati_utente = ("Andrea", password_hashata)

    try:
        cursore.execute(query, dati_utente)
        connessione.commit()
        print("Utente di prova inserito con successo (password HASHATA)!")
        print("🔒 La password NON è salvata in chiaro!")
    except sqlite3.IntegrityError:
        #L'utente esiste già, non è un errore
        print("Utente di prova già presente nel database.")
    except Exception as e:
        print(f"❌ Errore durante l'inserimento dell'utente: {e}")

except Exception as e:
    print(f"❌ Errore durante la connessione al database: {e}")

finally:
    if 'connessione' in locals():
        cursore.close()
        connessione.close()
        print("Successo, Connessione al database chiusa.")


if __name__ == "__main__":
    god = tk.Tk() #Crea la finestra principale
    app = Gui(god) 
    god.mainloop() #Avvia l'interfaccia grafica