import heapq
from models.Graph import Graph

def dijkstra(graph: Graph, start_node_id: str):
    """
    Algoritmo per cammini minimi che ritorna
    - distanze dal nodo iniziale come dizionario {id_nodo: distanza}
    - predecessori di ogni nodo come dizionario {id_nodo: id_precedente} per ricostruire il cammino
    """

    distances = {node.id: float('inf') for node in graph.nodes}
    predecessors = {node.id: None for node in graph.nodes}
    distances[start_node_id] = 0
    priority_heap = [(0, start_node_id)]
    
    while priority_heap:
        current_distance, current_id = heapq.heappop(priority_heap)
        if current_distance > distances[current_id]: # racchiude anche i nodi è già rilassati
            continue

        for edge in graph.get_adj(current_id):
            target_id = edge.target
            # il calcolo di dijsktra deve essere fatto sul costo ridotto
            target_distance = edge.cost - edge.source.potential + edge.target.potential 
            new_distance = current_distance + target_distance

            if new_distance < distances[target_id]:
                distances[target_id] = new_distance
                predecessors[target_id] = current_id
                heapq.heappush(priority_heap, (new_distance, target_id))
    
    return distances, predecessors