import heapq
from models.Graph import Graph
from models.Node import Node
import pprint

def dijkstra(graph: Graph, start_node_id: str):
    """
    una semplice implementazione di dijkstra
    
    :param graph: grafo da analizzare
    :param start_node_id: nodo da cui calcolare i cammini minimi
    :return ritorna \n 
    - un dizionario delle distanze dal nodo inizio {nodo_id : distanza_da_start} \n 
    - un dizionario che ad ogni nodo assegna il predecessore per il cammino minimo {nodo_id : id_predecessore}

    """
    distances = {node.id: float('inf') for node in graph.nodes}
    predecessors = {node.id: None for node in graph.nodes}
    distances[start_node_id] = 0
    priority_heap = [(0, start_node_id)]

    while priority_heap:
        current_distance, current_id = heapq.heappop(priority_heap)
        if current_distance > distances[current_id]:
            continue
        for edge in graph.get_adj(current_id):
            if edge.residual_capacity > 0:  
                target_id = edge.target
                u = graph.get_node(edge.source)
                v = graph.get_node(edge.target)
                reduced_cost = max(0,edge.cost - u.potential + v.potential)
                new_distance = current_distance + reduced_cost
                if new_distance < distances[target_id]:
                    distances[target_id] = new_distance
                    predecessors[target_id] = current_id
                    heapq.heappush(priority_heap, (new_distance, target_id))
    
    return distances, predecessors