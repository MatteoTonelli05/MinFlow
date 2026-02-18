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
        current_distance, u_id = heapq.heappop(priority_heap)
        if current_distance > distances[u_id]: #racchiude anche i nodi è già rilassati
            continue

        for edge in graph.get_adj(u_id):
            v_id = edge.target
            weight = edge.cost
            new_distance = current_distance + weight

            if new_distance < distances[v_id]:
                distances[v_id] = new_distance
                predecessors[v_id] = u_id
                heapq.heappush(priority_heap, (new_distance, v_id))
    
    return distances, predecessors