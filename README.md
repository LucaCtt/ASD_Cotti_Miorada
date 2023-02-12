# Progetto di Algoritmi e Strutture Dati AA 2021/2022

Progetto per il corso di Algoritmi e Strutture Dati della laurea magistrale
in Ingegneria Informatica presso l'Università degli Studi di Brescia.

In questo documento sono riportate esclusivamente le istruzioni per l'avvio dell'applicazione.
Le scelte progettuali sono documentate nella relazione.
I test per verificare la performance dell'implementazione si trovano in
[questo notebook su Google Colab](https://colab.research.google.com/drive/1EhVerQB7eSn5XzcdeW06sb2c1d9Vlafc?usp=sharing).

- [Progetto di Algoritmi e Strutture Dati AA 2021/2022](#progetto-di-algoritmi-e-strutture-dati-aa-20212022)
  - [Struttura del progetto](#struttura-del-progetto)
  - [Requisiti](#requisiti)
  - [Avvio dell'applicazione](#avvio-dellapplicazione)
    - [Generazione di istanze di test](#generazione-di-istanze-di-test)
      - [Istanze di test casuali](#istanze-di-test-casuali)
      - [Istanze di test sudoku](#istanze-di-test-sudoku)
    - [Esecuzione dell'algoritmo EC](#esecuzione-dellalgoritmo-ec)
    - [Confronto tra due risultati dell'algoritmo EC](#confronto-tra-due-risultati-dellalgoritmo-ec)
  - [Formato file](#formato-file)
    - [File di input](#file-di-input)
      - [Istanza casuale](#istanza-casuale)
      - [Istanza sudoku](#istanza-sudoku)
    - [File di output](#file-di-output)
      - [Istanza casuale](#istanza-casuale-1)
      - [Istanza sudoku](#istanza-sudoku-1)
  - [Licenza](#licenza)
  - [Autori](#autori)


## Struttura del progetto

    .
    ├── exact-cover             
    │   ├── __main__.py         # Punto di ingresso dell'applicazione
    │   ├── cli.py              # Interfaccia a riga di comando
    │   ├── compare.py          # Funzioni di confronto tra due risultati dell'algoritmo EC
    │   ├── ec.py               # Implementazione dell'algoritmo EC (ed EC+)
    │   └── inst                
    │       ├── rand.py         # Generazione di istanze di test casuali
    │       └── sudoku.py       # Generazione di istanze di test sudoku
    ├── test                    
    │   ├── rand                
    │   │   └── ...             # Istanze di test casuali
    │   └── sudoku               
    │       └── ...             # Istanze di test sudoku
    ├── .env                    # Variabili d'ambiente
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

Una volta installate le dipendenze, è possibile avviare l'applicazione usando l'interprete di
Python, specificando uno dei seguenti comandi:

- `gen`: genera istanze di test;
- `ec`: esegue l'algoritmo EC;
- `compare`: confronta risultati dell'algoritmo EC.

In qualsiasi momento è possibile possibile utilizzare
l'opzione `-h` (o `--help`) per ottenere una descrizione delle opzioni disponibili.

Per esempio, per mostrare l'help del comando principale:

```bash
python exact-cover -h
```

### Generazione di istanze di test

Per generare istanze di test è possibile utilizzare il comando `gen`.
I sottocomandi `rand` e `sudoku` generano rispettivamente istanze di test casuali e sudoku.

Nella cartella `test` è possibile trovare delle istanze di test già generate (e risolte).

#### Istanze di test casuali

Le opzioni disponibili sono:
- `-o`, `--output`: file su cui salvare l'istanza generata (default: `test/in.txt`);
- `-m`, `--mdim`: cardinalità dell'insieme M (default: `10`);
- `-n`, `--ndim`: cardinalità dell'insieme N (default: `10`);
- `-p`, `--prob`: probabilità di generaee 1 nella distribuzione binomiale (default: `0.5`);
- `-g`, `--guarantee`: se deve essere garantita almeno una soluzione all'istanza generata (default: `False`).

Per esempio, per generare un'istanza di test casuale con `100` elementi in M, `100` elementi in N,
probabilità di 1 pari a `0.5` e senza garanzia di soluzione:

```bash
python exact-cover gen rand -o test/100x100x05.txt -m 100 -n 100 -p 0.5
```

#### Istanze di test sudoku

La generazione di sudoku è configurabile con le seguenti opzioni:
- `-o`, `--output`: file su cui salvare l'istanza generata (default: `test/in.txt`);
- `-s`, `--side-dim`: dimensione (del lato) del sudoku (default: `9`);
- `-d`, `--diff`: difficoltà del sudoku, da 0 (sudoku pieno) a 1 (sudoku vuoto) (default: `0.3`);

Per esempio, per generare un'istanza sudoku `9x9`, con difficoltà pari a `0.3`:

```bash
python exact-cover gen sudoku -o test/9x9x03.txt
```

### Esecuzione dell'algoritmo EC

Il comando `ec` esegue l'algoritmo EC (o EC+).

Le opzioni supportate sono:
- `-i`, `--input`: file da cui leggere l'istanza (default: `test/in.txt`);
- `-o`, `--output`: file su cui salvare il risultato dell'algoritmo (default: `test/out.txt`);
- `-p`, `--plus`: se deve essere eseguito l'algoritmo EC+ (default: `False`);
- `-t`, `--time`: tempo massimo di esecuzione dell'algoritmo in secondi (opzionale).
- `-s`, `--sparse`: se deve essere usata la rappresentazione sparsa (default: `False`).

Il seguente comando esegue l'algoritmo EC+ sull'istanza di test `test/100x100x05.txt`,
salvando il risultato in `test/out.txt` e senza limitare il tempo di esecuzione:

```bash
python exact-cover ec -i test/100x100x05.txt -o test/out_plus.txt -p
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
- `-i`, `--input`: lista di file da cui leggere i risultati.

Per esempio, per confrontare i risultati dell'algoritmo EC+ e EC:

```bash
python exact-cover compare -i test/out.txt test/out_plus.txt
```

Il comando accetta un numero arbitrario di file da confrontare: è sufficiente separarli con uno spazio.

```bash
python exact-cover compare -i test/out1.txt test/out2.txt test/out3.txt test/out4.txt
```

## Formato file

### File di input

#### Istanza casuale

```text
;;; Exact-Cover (Random)                      # Tipo di istanza.
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

#### Istanza sudoku

```text
;;; Exact-Cover (Sudoku)                      
;;; Generated at: 2023-02-04 14:46:34.223187  
;;; Dimension: 4                              # Dimensione del sudoku (dim x dim)
;;; Difficulty: 0.4                           # Difficoltà
;;; Sudoku puzzle:                            #
;;; +-----+-----+                             #
;;; | 3 4 |   1 |                             #
;;; |   1 | 3   |                             # Sudoku da risolvere.
;;; +-----+-----+                             #
;;; | 4   | 1 3 |                             #
;;; | 1 3 |     |                             #
;;; +-----+-----+                             #
0 0 0 0 0 0 0 0 0 0 0 0 0 ...                 # 
0 0 0 0 0 0 0 0 0 0 0 0 0 ...                 # Matrice A equivalente al sudoku.
...                                           #
```
### File di output

#### Istanza casuale

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

#### Istanza sudoku

```text
;;; EC Algorithm (Plus version)
;;; Executed at: 2023-02-04 14:50:18.334008
;;; Execution time: 34.082059568000005s (0.568 minutes) 
;;; Stopped: False
;;; Time limit reached: False
;;; Nodes visited: 2900522
;;; Total nodes: 18446744073709551615
;;; Percentage of nodes visited: 0.0%
;;;
;;; Sudoku solutions:                                      #
;;; +-----+-----+                                          #
;;; | 3 4 | 2 1 |                                          #
;;; | 2 1 | 3 4 |                                          # Soluzioni del sudoku.
;;; +-----+-----+                                          #
;;; | 4 2 | 1 3 |                                          #
;;; | 1 3 | 4 2 |                                          #
;;; +-----+-----+                                          #
;;;
;;; Set   1: [0 0 ... ]
;;; ...
;;;
;;; Exact Coverages:
[ 3  8 10 13 18 21 27 32 36 38 41 47 49 55 60 62]
```

## Licenza

MIT (vedi [LICENSE](LICENSE)).

## Autori

Luca Cotti, Stefano Miorada