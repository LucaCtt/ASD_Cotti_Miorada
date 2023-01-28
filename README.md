# Progetto di Algoritmi e Strutture Dati AA 2021/2022

Progetto per il corso di Algoritmi e Strutture Dati della laurea magistrale
in Ingegneria Informatica presso l'Università degli Studi di Brescia.

- [Progetto di Algoritmi e Strutture Dati AA 2021/2022](#progetto-di-algoritmi-e-strutture-dati-aa-20212022)
  - [Struttura del progetto](#struttura-del-progetto)
  - [Requisiti](#requisiti)
  - [Avvio dell'applicazione](#avvio-dellapplicazione)
    - [Generazione di istanze di test](#generazione-di-istanze-di-test)
    - [Esecuzione dell'algoritmo EC](#esecuzione-dellalgoritmo-ec)
    - [Confronto tra due risultati dell'algoritmo EC](#confronto-tra-due-risultati-dellalgoritmo-ec)
  - [Formato file](#formato-file)
    - [File di input](#file-di-input)
    - [File di output](#file-di-output)
  - [Licenza](#licenza)
  - [Autori](#autori)


## Struttura del progetto

    .
    ├── src                     # Sorgenti
    │   ├── cli.py              # Interfaccia a riga di comando
    │   ├── compare.py          # Funzioni di confronto tra due risultati dell'algoritmo EC
    │   ├── ec.py               # Implementazione dell'algoritmo EC (ed EC+)
    │   ├── gen.py              # Generazione di istanze di test
    │   └── main.py             # Script principale
    ├── test                    # Istanze di test
    │   └── ...
    ├── .gitignore              # Git ignore file
    ├── consegna.pdf            # Consegna del progetto
    ├── CITATION.cff            # File di citazione
    ├── LICENSE                 # Licenza
    ├── README.md               # Questo file
    └── requirements.txt        # Dipendenze Python 

## Requisiti

Per avviare il progetto è richiesto Python 3.9 o superiore.

Dopoiché è possibile installare le dipendenze indicate in `requirements.txt`.
Per esempio, con `pip`:

```python
pip install -r requirements.txt
```

## Avvio dell'applicazione

Una volta installate le dipendenze, è possibile avviare l'applicazione eseguendo lo script `main.py`
nella cartella `src`, che supporta i seguenti sotto-comandi:

- `gen`: genera istanze di test;
- `ec`: esegue l'algoritmo EC;
- `compare`: confronta risultati dell'algoritmo EC;

Sia sul comando principale che sui sotto-comandi è possibile utilizzare
l'opzione `-h` (o `--help`) per ottenere una descrizione delle opzioni disponibili.

Per esempio, per mostrare l'help del comando principale:

```bash
python src/main.py -h
```

### Generazione di istanze di test

Per generare istanze di test è possibile utilizzare il comando `gen`.

Le opzioni disponibili sono:
- `-o`, `--output`: file su cui salvare l'istanza generata (default: `test/in.txt`);
- `-m`, `--mdim`: cardinalità dell'insieme M (default: 10);
- `-n`, `--ndim`: cardinalità dell'insieme N (default: 10);
- `-p`, `--prob`: probabilità di generaee 1 nella distribuzione binomiale (default: 0.5);
- `-g`, `--guarantee`: se deve essere garantita almeno una soluzione all'istanza generata (default: No).

Per esempio, per generare un'istanza di test con 100 elementi in M, 100 elementi in N,
probabilità di 1 pari a 0.5 e con garanzia di soluzione:

```bash
python src/main.py gen -o test/100x100x05.txt -m 100 -n 100 -p 0.5 -g
```

### Esecuzione dell'algoritmo EC

Il comando `ec` esegue l'algoritmo EC (o EC+).

Le opzioni supportate sono:
- `-i`, `--input`: file da cui leggere l'istanza (default: `test/in.txt`);
- `-o`, `--output`: file su cui salvare il risultato dell'algoritmo (default: `test/out.txt`);
- `-p`, `--plus`: se deve essere eseguito l'algoritmo EC+ (default: No).
- `-t`, `--time`: tempo massimo di esecuzione dell'algoritmo in secondi.

Il seguente comando esegue l'algoritmo EC+ sull'istanza di test `test/100x100x0.5.txt`,
salvando il risultato in `test/out.txt` e senza limitare il tempo di esecuzione:

```bash
python src/main.py ec -i test/100x100x05.txt -o test/out_plus.txt -p
```

L'esecuzione dell'algoritmo può essere interrotta in qualsiasi momento
inviando un segnale di interruzione (`Ctrl+C` su Linux e windows, `Cmd+C` su macOS).

Se l'algoritmo viene interrotto o manualmente o perché il tempo massimo di esecuzione è stato raggiunto,
il risultato parziale viene comunque salvato nel file di output.

### Confronto tra due risultati dell'algoritmo EC

Il comando `compare` confronta risultati dell'algoritmo EC,
verificando che siano innanzitutto uguali (ovvero che abbiano lo stesso set COV e lo stesso numero di nodi visitati).
Se questo è vero per ognuno dei risultati, viene indicato il risultato migliore.

Opzioni disponibili:
- `-i`, `--input`: lista di file da cui leggere i risultati;

Per esempio, per confrontare i risultati dell'algoritmo EC+ e EC sull'istanza di test `test/100x100x0.5.txt`:

```bash
python src/main.py compare -i test/out.txt test/out_plus.txt
```

Il comando accetta un numero arbitrario di file da confrontare: è sufficiente separarli con uno spazio.

```bash
python src/main.py compare -i test/out1.txt test/out2.txt test/out3.txt test/out4.txt
```

## Formato file

### File di input

```text
;;; Generated at: 2023-01-28 10:05:39.256451  # Data di generazione.
;;; Cardinality of M: 5                       # Cardinalità insieme M.
;;; Cardinality of N: 8                       # Cardinalità insieme N. 
;;; Probability: 0.5                          # Probabilità di 1 nella distribuzione binomiale. 
;;; Guarantee solution: False                 # Se è garantita almeno una soluzione.
;;; Fixed zero col: False                     # Se è stata generata (e poi sistemata) una colonna con solo 0.
0 0 1 1 0 -                                   #
1 1 1 1 0 -                                   #  
0 1 1 0 1 -                                   #
0 1 0 0 0 -                                   # Matrice di input A.
1 1 0 0 0 -                                   #
0 0 0 0 1 -                                   #
0 1 0 1 1 -                                   #
0 0 1 0 1 -                                   #
```

### File di output

```text
;;; EC Algorithm (Base version)                           # Versione dell'algoritmo.
;;; Executed at: 2023-01-28 10:16:44.389198               # Data di esecuzione.
;;; Execution time: 0.00034165382385253906s (0.0 minutes) # Tempo di esecuzione.
;;; Stopped: False                                        # Se l'algoritmo è stato interrotto.
;;; Time limit reached: False                             # Se il tempo massimo di esecuzione è stato raggiunto.
;;; Nodes visited: 43                                     # Numero di nodi visitati.
;;; Total nodes: 255                                      # Numero totale di nodi.
;;; Percentage of nodes visited: 16.8627%                 # Percentuale di nodi visitati.
;;;
;;; Set   1: [0 0 1 1 0]                                  # 
;;; Set   2: [1 1 1 1 0]                                  #
;;; Set   3: [0 1 1 0 1]                                  #
;;; Set   4: [0 1 0 0 0]                                  # Insiemi di N, con relativo indice.
;;; Set   5: [1 1 0 0 0]                                  #
;;; Set   6: [0 0 0 0 1]                                  #
;;; Set   7: [0 1 0 1 1]                                  #
;;; Set   8: [0 0 1 0 1]                                  #
;;;
;;; Exact Coverages:                                      # 
[6 2]                                                     # Coperture esatte (insieme COV).
[6 5 1]                                                   #
```

## Licenza

MIT.

## Autori

Luca Cotti, Stefano Miorada