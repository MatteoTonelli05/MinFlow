from models.Graph import Graph
from models.Node import Node
from utilities.graph.GraphChecker import GraphChecker
from pathlib import Path
from utilities.graph.plot_graph import plot
from utilities.loaders.Loader import Loader
from utilities.known_algorithms.Disjkstra import dijkstra

def selectSource(graph: Graph) -> Node:
    """
    Sceglie la sorgente con il supply maggiore (l'idea è di massimizzare il flusso)
    
    :param graph: grafo su cui eseguire la ricerca
    """
    supplies = graph.get_supply_nodes()
    return (max(graph.get_supply_nodes(), lambda x: x.supply) if supplies else None)

def theres_path(graph: Graph, distances):
    """
    Controlla se i nodi demand (supply < 0) siano raggiungibili
    
    :param graph: grafo su cui eseguire la ricerca 
    :param distances: distanze dal nodo iniziale come dizionario {id_nodo: distanza}
    """
    return any(distances.get(n.id) < float('inf') for n in graph.get_demand_nodes())

file_path = Path("resource") / "grafo_iniziale.json"
config_path = Path("resource") / "config.yml"
graph = Graph(file_path)
checker = GraphChecker(graph)
ok = 1
if checker.validateGraph():
    while ok > 0:
        plot(graph, dict(Loader().from_yaml(config_path)))
        s = selectSource(graph)
        
        if s:
            distances, predecessors = dijkstra(graph, s.id)
            targets = [n for n in graph.get_demand_nodes() if distances.get(n.id) < float('inf')]
            
            if targets:
                t = min(targets, lambda x: x.supply)
                
                path = graph.reconstruct_path(predecessors, s.id, t.id) #TO-DO
                delta = min(s.supply, abs(t.supply), graph.get_min_residual_capacity(path)) #TO-DO
                graph.augment_flow(path, delta) #TO-DO
                
                for n in graph.nodes():
                    if distances.get(n.id) < float('inf'):
                        n.potential = n.potential - distances.get(n.id)
            else:
                # Se ho ancora supply ma non raggiungo nessuna demand, non c'è soluzione ammissibile
                print("Nessun cammino verso nodi di domanda: soluzione non ammissibile.")
                ok = -1
        else:
            print("Tutte le domande soddisfatte: Soluzione Ottima!")
            ok = 0
else:
    print("")