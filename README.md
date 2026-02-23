# SSP – Ricerca Operativa  
**Algoritmo Successive Shortest Path per il Minimum Cost Flow**

## Descrizione del progetto
Questo progetto implementa l’algoritmo **Successive Shortest Path (SSP)** per la risoluzione del problema di **Minimum Cost Flow** dato un grafo descritto tramite un json.

L’algoritmo procede iterativamente selezionando un nodo con supply positivo e individuando un cammino a costo minimo verso un nodo con domanda tramite l’algoritmo di **Dijkstra**. Il flusso viene quindi aggiornato nel grafo residuo fino alla soddisfazione di tutti i vincoli.

Il progetto è stato sviluppato a scopo didattico nell’ambito del corso di **Ricerca Operativa**.

Tutti i comandi trascritti durante questo documento sono pensati per la **bash Windows**.


## Linguaggi di programmazione
[![Python][Python.js]][Python-url] \
Ho scelto di usare python poichè interessato a sfruttare le semplici visualizzazioni interattive di librerie come NetworkX e Netgraph

## Formati testuali
[![JSON][JSON.js]][JSON-url] \
Essendo lo standard "de facto" per lo scambio di dati, ho preferito sfruttare il formato JSON per rendere il caricamento del grafo più "universale".
Anche in ottica di chiamate ad applicazioni esterne \

[![YAML][YAML.js]][YAML-url] \
Ho scelto Yaml per la leggibilità umana e la semplicità, così evitando eventuali errori di formattazione. 

## Struttura del progetto

```
ssp_RicercaOperativa/
│
├── ssp.py                     # Script principale
├── requirements.txt           # Librerie richieste
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

## Per Iniziare

### Prerequisiti
*(Consigliato)*\
*Prima di installare i requisiti consiglio di creare un ambiente virtuale per evitare conflitti tra eventuali diverse verisioni di pacchetti precedentemente installati*
   ```bash
   python -m venv venv
   .\venv\Scripts\activate.bat
   ```
Tutti i requisiti sono elencati all'interno del file requirements.txt e facilmente scaricabili tramite comando Bash:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
---
### Avvio   
Prima di tutto clonare il progetto, tramite il comando bash:
   ```bash
   git clone https://github.com/MatteoTonelli05/Successive-Shortest-Path.git
   ```

Prima di avviare lo script assicurarsi di inserire all'interno del file 'grafo_iniziale.json' tutti i dati appartenenti al grafo che vogliamo analizzare.

La **struttura** è divisa in due array principali:

1. **Nodes**\
   ogni oggetto nell'array rappresentera un entità della rete:
   - id : Identificativo univoco del nodo (stringa)
   - supply: Bilancio del nodo (intero)
2. **Edges**\
   Ogni oggetto definisce un collegamento unidirezionale tra due nodi:
   - source: ID del nodo di partenza
   - target: ID del nodo di arrivo
   - capacity: Il flusso massimo che può transitare su questo arco
   - cost: Il costo per inviare flusso su questo arco

*ESEMPIO DI JSON CORRETTO*
   ```json
   {
      "nodes": [
         { "id": "S1", "supply": 10 },    // Sorgente: ha 10 unità da inviare
         { "id": "V1", "supply": 0 },     // Nodo di transito: smista il flusso
         { "id": "T1", "supply": -10 }    // Destinazione: richiede 10 unità
      ],
      "edges": [
         {
            "{source": "S1",
            "target": "V1",
            "capacity": 15,                // Può trasportare fino a 15 unità
            "cost": 2                      
         },
         {
            "source": "V1",
            "target": "T1",
            "capacity": 10,
            "cost": 1
         }
      ]
   }
   ```
---

Per avviare lo script accedere alla cartella principale tramite il comando ```cd``` (per capirsi quella che contiene ssp.py) ed eseguire

```bash
python ssp.py
```

## Visualizzazione grafica
Durante l'esecuzione dell'algoritmo, il sistema genera una finestra interattiva per il monitoraggio del flusso. La visualizzazione segue queste convenzioni:
- **Nodi**: Ogni nodo riporta il proprio **ID** e il valore di **Supply** ($b_i$). Il colore del nodo cambia in base al suo stato (offerta, domanda o transito), visualizzabile dal file ```config.yml```.
- **Archi**: Le etichette sugli archi mostrano i dati in tempo reale nel formato
**flusso attuale / capacità (costo)**\
- **Avanzamento**: L'algoritmo non procede automaticamente, il passaggio alla prossima iterazione avviene esclusivamente al click del pulsante dedicato, permettendo l'analisi passo-passo della rete residua e dei cammini minimi individuati.
## Configurazione
Il file ```config.yaml``` agisce come centro di controllo per l'aspetto estetico del grafo. Di seguito la descrizione dei parametri disponibili:
- **supply_color**: Definisce il colore dei nodi di "offerta" ($b_i > 0$).
- **demand_color**: Definisce il colore dei nodi di "domanda" ($b_i < 0$).
- **empty_node_color**: Colore utilizzato per i nodi di transito ($b_i = 0$).
- **node_size**: Scala la dimensione del cerchio dei nodi.
- **font_size_edge_labels**: Regola la leggibilità del testo sopra gli archi (flusso/capacità).
- **edge_width**: Definisce lo spessore delle linee che collegano i nodi.
- **seed**: Fissa la posizione dei nodi nello spazio; cambiando questo numero, il grafo verrà "mescolato" in una nuova disposizione.
- **edge_curve_rad**: Gestisce la curvatura degli archi. Impostandolo a 0 gli archi saranno linee rette, mentre valori superiori creano archi curvi (indispensabile per distinguere archi che collegano gli stessi due nodi in direzioni opposte).

**Nota: alla chiusura della finestra di visualizzazione è obbligatorio chiudere da console l'attività del programma.**

## Formulazione Matematica del problema

Sia dato un grafo direzionato $G = (N, A)$, in cui ad ogni arco $(i, j) \in A$ è associato un costo $c_{ij}$ e una capacità $u_{ij}$.\
Ad ogni vertice $i \in N$ è associata una disponibilità $b_i > 0$ oppure una richiesta $b_i < 0$ oppure $b_i = 0$.\
Il problema del flusso di costo minimo può essere formulato come segue:$$\begin{aligned}
Min \ z(P) = & \sum_{(i,j) \in A} c_{ij}x_{ij} \\
s.t. \ & \sum_{j \in \Gamma_i} x_{ij} - \sum_{j \in \Gamma_i^{-1}} x_{ji} = b_i, \quad i \in N \\
& 0 \le x_{ij} \le u_{ij}, \quad (i, j) \in A
\end{aligned}$$dove $\Gamma_i = \{j : (i, j) \in A\}$ e $\Gamma_i^{-1} = \{j : (j, i) \in A\}$.

---

### Spiegazione Informale

```text 
Il problema del flusso di costo minimo serve a determinare quanto flusso far transitare su ogni arco per minimizzare la spesa totale, rispettando i limiti di capacità di ciascun collegamento. In ogni nodo della rete deve essere garantito il bilancio tra il flusso entrante e quello uscente, in modo che i nodi fornitori immettano la quantità richiesta e i nodi destinatari la ricevano correttamente. L'obiettivo finale è trovare la configurazione degli archi che soddisfi le necessità dei nodi al minor costo possibile, senza mai superare la portata massima consentita su ogni singolo arco.
```

## Assunzioni
1. Tutti i dati (i.e., costi, richieste/disponibilità e capacità) sono valori interi.
2. Il grafo è direzionato.
3. Le richieste e le disponibilità dei diversi nodi soddisfano la condizione $\sum_{i \in N} b_i = 0$.
4. Il problema di flusso di costo minimo ha una soluzione ammissibile.
5. Il grafo contiene un cammino diretto di capacità infinita per ogni coppia di nodi.
6. Tutti i costi $c_{ij}$ sono non negativi e le capacità $u_{ij}$ sono positive.

### Nel codice
- Le assunzioni 2, 3 e 6 vengono controllate all'interno del modulo ```GraphChecker.py``` 
- L'interezza dei dati (assunzione 1) viene regolata dal modulo ```Loader.py``` che traduce il file json in int in modo esplicito, traducendo quindi anche i valori non interi in int
- Le assunzioni 4 e 5 non sono controllate poichè in caso contrario l'algoritmo si fermerebbe senza causare danni.

## Logica di Funzionamento dell'algoritmo
1. **Selezione dei Nodi**\
 Ad ogni iterazione, l'algoritmo individua il nodo con disponibilità residua (sorgente) maggiore.\

 ***Nota:** l'algoritmo originale prevede la scelta di un nodo destinazione, ma per garantire la raggiungibilità tra sorgente e destinatario ho preferito farlo scegliere a seguito del calcolo dei cammini minimi.*

2. **Ricerca del cammino minimo**\
Vengono calcolati i cammini minimi all'interno della **rete residua**. Per garantire l'efficienza, si utilizzano i potenziali dei nodi per trasformare i costi degli archi in valori non negativi, permettendo l'uso dell'algoritmo di Dijkstra.\

***Nota:** per diminuire il costo computazionale si è scelto di usare Dijkstra tramite una struttura Heap.*

3. **Invio del Flusso**\
Una volta individuato il cammino, si invia lungo gli archi che lo compongono la massima quantità di flusso possibile. Questa quantità è limitata dalla capacità residua degli archi del cammino e dal valore di disponibilità/richiesta dei nodi scelti.

4. **Aggiornamento della Rete**\
Dopo l'invio del flusso, le capacità residue degli archi vengono aggiornate e i potenziali dei nodi vengono ricalcolati per riflettere le nuove distanze minime, mantenendo la condizione di ottimalità per l'iterazione successiva.

### Condizioni di Terminazione
La terminazione avviene quando non esistono più nodi con disponibilità o richiesta residua.
Poiché ogni passo riduce il disavanzo totale tra domanda e offerta, l'algoritmo garantisce il raggiungimento della soluzione ottima globale se il problema è ammissibile.\
**Nota:** Nell'algoritmo la terminazione può avvenire anche se non vi sono più **percorsi disponibili** tra una sorgente e una qualsiasi destinazione (problema non ammissibile) o se il grafo non rispetta le **assunzioni** iniziali del problema.

## Analisi della Complessità
L'algoritmo opera attraverso una serie di iterazioni. In ogni iterazione, viene inviata almeno una unità di flusso lungo un cammino minimo tra un nodo sorgente e un nodo destinazione.\
La **complessità computazionale** tiene conto di:
- **Numero di Iterazioni**\
Nel caso peggiore, l'algoritmo esegue un numero di iterazioni pari alla somma delle disponibilità totali dei nodi sorgente, indicata solitamente con $U = \sum_{i:b_i>0} b_i$\
Questo accade perché ogni iterazione può trasportare anche solo una singola unità di flusso.
 - **Costo per Iterazione**\
  Ogni passo richiede la ricerca di un cammino minimo su un grafo con $n$ nodi e $m$ archi. Utilizzando l'algoritmo di Dijkstra con una gestione efficiente della coda di priorità (ad esempio con un heap), il costo di questa operazione è $O(m\log n)$

**Complessità Totale**: $O(U \cdot (m \log n))$.\
**Note:** 
1. Poiché la complessità dipende dal valore numerico delle disponibilità ($U$) e non solo dalla dimensione del grafo, l'SSP è classificato come un algoritmo **Pseudo Polinomiale**.
2. La complessità varia in base alla struttura dati utilizzata ad esempio diventerebbe $O(U \cdot (m + n \log n))$ con un Fibonacci Heap



[Python.js]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[JSON.js]: https://img.shields.io/badge/json-5E5E5E?style=for-the-badge&logo=json&logoColor=white
[JSON-url]: https://www.json.org/json-en.html

[YAML.js]: https://img.shields.io/badge/yaml-CB171E?style=for-the-badge&logo=yaml&logoColor=white
[YAML-url]: https://yaml.org/