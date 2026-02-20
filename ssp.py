from models.Graph import Graph
from models.Node import Node
from models.Edge import Edge
from utilities.graph.GraphChecker import GraphChecker
from pathlib import Path
from utilities.graph.Plotting import plot
from utilities.loaders.Loader import Loader
from utilities.known_algorithms.Disjkstra import dijkstra

def selectSource(graph: Graph) -> Node:
    """
    Sceglie la sorgente con il supply maggiore (l'idea è di massimizzare il flusso)
    
    :param graph: grafo su cui eseguire la ricerca
    """
    supplies = graph.get_supply_nodes()
    if supplies:
        return max(supplies, key = lambda x: x.supply)
    else:
        return None

def theres_path(graph: Graph, distances) -> bool:
    """
    Controlla se i nodi demand (supply < 0) siano raggiungibili
    
    :param graph: grafo su cui eseguire la ricerca 
    :param distances: distanze dal nodo iniziale come dizionario {id_nodo: distanza}
    :return se c'è ancora un cammino disponibile nel grafo
    """
    return any(distances.get(n.id) < float('inf') for n in graph.get_demand_nodes())

def get_min_residual_capacity(path: list[Edge]) -> int:
        """
        Data una lista di archi che rappresentano il cammino,
        restituisce la minima capacità residua disponibile.

        :param path: lista di archi che rappresentano il cammino
        :return: minima capacità residua disponibile.
        """
        if path:
            return min(map(lambda x: x.residual_capacity, path))
        return 0

file_path = Path("resource") / "temp.json"
config_path = Path("resource") / "config.yml"
graph = Graph(file_path)
checker = GraphChecker(graph)
ok = 1
if checker.validateGraph():
    while ok > 0:
        plot(graph, dict(Loader().from_yaml(config_path)))
        s = selectSource(graph)
        
        if s and s.supply > 0:
            distances, predecessors = dijkstra(graph, s.id)
            targets = [n for n in graph.get_demand_nodes() if distances.get(n.id) != float('inf')]
            if targets:
                t = min(targets, key=lambda x: x.supply)
                
                path = graph.reconstruct_path(predecessors, s.id, t.id)
                delta = min(s.supply, abs(t.supply), get_min_residual_capacity(path=path))
                graph.augment_flow(path, delta)
                s.supply -= delta
                t.supply += delta
                
                for n in graph.nodes:
                    if distances.get(n.id) < float('inf'):
                        n.potential = n.potential - distances.get(n.id)
            else:
                print("Nessun cammino verso nodi di domanda: soluzione non ammissibile.")
                ok = -1
        else:
            print(graph)
            ok = 0
else:
    print("Il grafo non rispetta i vincoli base (assunzioni) del Minimum Cost Max Flow")