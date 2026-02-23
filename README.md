# SSP – Ricerca Operativa  
**Algoritmo Successive Shortest Path per il Minimum Cost Flow**

## Descrizione del progetto
Questo progetto implementa l’algoritmo **Successive Shortest Path (SSP)** per la risoluzione del problema di **Minimum Cost Flow** su grafi con nodi caratterizzati da valori di **supply** e **demand**.

L’algoritmo procede iterativamente selezionando un nodo con supply positivo e individuando un cammino a costo minimo verso un nodo con domanda tramite l’algoritmo di **Dijkstra**. Il flusso viene quindi aggiornato nel grafo residuo fino alla soddisfazione di tutti i vincoli.

Il progetto è stato sviluppato a scopo didattico nell’ambito del corso di **Ricerca Operativa**.

---

## Struttura del progetto

```
ssp_RicercaOperativa/
│
├── ssp.py                     # Script principale
│
├── models/
│   ├── Graph.py               # Definizione del grafo
│   ├── Node.py                # Definizione dei nodi
│   └── Edge.py                # Definizione degli archi
│
├── utilities/
│   ├── graph/
│   │   ├── GraphChecker.py    # Controlli di validità  del grafo
│   │   └── Plotting.py        # Visualizzazione del grafo
│   │
│   ├── known_algorithms/
│   │   └── Disjkstra.py       # Algoritmo di Dijkstra
│   │
│   └── loaders/
│       └── Loader.py          # Caricamento file di input
│
├── resource/
│   ├── grafo_iniziale.json    # Grafo di input
│   └── config.yml             # Configurazione grafica
│
└── README.md
```

---

## Requisiti
- Interprete Python versione 3.8 o superiore
- Gestore di pacchetti pip
- Librerie esterne:
  - PyYAML
  - NetworkX
  - Matplotlib (per la visualizzazione del grafo)

---

## Esecuzione

1. Spostarsi nella directory principale del progetto:
   ```bash
   cd ssp_RicercaOperativa
   ```

2. Avviare lo script principale:
   ```bash
   python ssp.py
   ```

---

## Logica dell’algoritmo

1. Selezione di un nodo con supply positivo.
2. Ricerca del cammino minimo tramite Dijkstra sul grafo residuo.
3. Calcolo del flusso incrementale ammissibile.
4. Aggiornamento di flussi e capacità residue.
5. Aggiornamento dei potenziali dei nodi.
6. Terminazione al soddisfacimento di tutti i vincoli.

---

## Controlli di validità
Prima dell’esecuzione, il grafo viene verificato tramite il modulo `GraphChecker`.  
In caso di violazione dei vincoli del problema, l’esecuzione viene interrotta.

---

## Input
Il grafo è definito tramite file JSON contenenti nodi (supply/demand) e archi (capacità e costi).  
Le impostazioni di visualizzazione sono configurabili tramite file YAML.

---

## Obiettivo
Determinare un flusso che soddisfi tutti i vincoli di supply e demand, rispetti le capacità degli archi e minimizzi il costo totale.

---

