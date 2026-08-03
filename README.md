# Suite Calcolatrice

# 🧮 Calcolatrice Multifunzione in Python

## 📌 Descrizione

Questa è un'applicazione desktop sviluppata in Python utilizzando `tkinter` per l'interfaccia grafica e `sqlite3` per la gestione del database. L'applicazione offre un sistema di autenticazione per gli utenti e permette di accedere a tre strumenti principali: una calcolatrice standard, una calcolatrice scientifica e un convertitore di basi numeriche. Tutte le operazioni effettuate vengono salvate nella cronologia personale dell'utente all'interno del database locale.

## ✨ Funzionalità

* **Sistema di Autenticazione:** Registrazione e login sicuri. Le password non vengono mai salvate in chiaro; sono cifrate utilizzando l'algoritmo SHA-256 con l'aggiunta di un *salt* (salvate in formato esadecimale) per garantire un'alta sicurezza.


* **Menu di Selezione:** Un'interfaccia grafica dedicata, che appare dopo l'accesso, permette di scegliere quale strumento avviare.


* **Calcolatrice Standard:** Gestisce le operazioni matematiche di base (+, -, *, /) e il calcolo della percentuale.


* **Calcolatrice Scientifica:** Include funzioni avanzate come seno, coseno, tangente, radice quadrata, potenze, fattoriale, logaritmi (base 10 e naturale) ed esponenziali.


* **Convertitore di Basi:** Permette di convertire istantaneamente un valore tra base Decimale (10), Binaria (2), Esadecimale (16) e Ottale (8).


* **Cronologia Integrata:** Ogni espressione calcolata e ogni conversione effettuata vengono salvate automaticamente in formato testuale nel database SQLite, associate all'utente attualmente connesso.



## 📂 Struttura del Progetto

Il software è modularizzato nei seguenti file:

* **Script Principale / Autenticazione:** Gestisce l'interfaccia di accesso, la registrazione e la creazione automatica della tabella `utenti` nel database.


* **`finestre.py`:** Contiene la logica per il menu di selezione post-login.


* **`calcolatriceNormale.py`:** Modulo contenente l'interfaccia e la logica della calcolatrice standard.


* **`calcolatriceScientifica.py`:** Modulo dedicato all'interfaccia e alle operazioni scientifiche/trigonometriche.


* **`calcolatriceConvertitrice.py`:** Modulo per l'interfaccia di conversione dei formati numerici.



## 🚀 Requisiti

Il progetto utilizza esclusivamente librerie standard di Python, eliminando la necessità di scaricare pacchetti esterni tramite `pip`.

* **Python 3.x**
* Moduli utilizzati: `tkinter` (per la GUI), `sqlite3` (per il database), `hashlib` e `os` (per la sicurezza), `math` (per i calcoli scientifici).



## 💻 Come eseguire l'applicazione

1. Clona o scarica il repository sul tuo computer.
2. Apri il terminale e posizionati nella cartella del progetto.
3. **⚠️ Importante:** Devi avviare sempre l'applicazione dal file principale di login. Se tenti di avviare direttamente i moduli delle calcolatrici (es. `calcolatriceNormale.py`, `calcolatriceScientifica.py` o `calcolatriceConvertitrice.py`), l'applicazione ti mostrerà un errore di "Avvio non consentito" e si chiuderà.


4. Esegui il comando di avvio del file principale:
   
python main.py

5. Registra un nuovo utente oppure accedi. Se è il primo avvio in assoluto, il sistema genererà il database locale e inserirà un utente di prova di default (Nome: `Andrea`, Password: `password123`).



## 🛡️ Gestione dei Dati

Il database (es. `calco.db`) viene generato nel medesimo percorso in cui viene lanciato lo script. La tabella `utenti` è così strutturata:

* `id` (Chiave primaria incrementale).


* `nome` (Testo, obbligatorio e univoco).


* `password` (L'hash crittografico).


* `cronologia` (Testo semplice in cui si concatenano le varie operazioni, mandate a capo con `\n`).
