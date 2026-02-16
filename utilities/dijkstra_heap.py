import heapq
import numpy as np

def __init(graph_data, start_node_id):
    nodes_info = {
        node["id"]: {
            "neighbors": [], 
            "cost": np.inf, 
            "prev": None
        } for node in graph_data["nodes"]
    }

    for edge in graph_data["edges"]:
        nodes_info[edge["source"]]["neighbors"].append((edge["target"], edge["cost"]))

    nodes_info[start_node_id]["cost"] = 0
    heap_cost = []
    heapq.heappush(heap_cost,(0, start_node_id))
    return nodes_info, heap_cost

def solve(graph_data, start_node_id, end_node_id):
    nodes_info, heap_cost = __init(graph_data, start_node_id)

    while (heap_cost):  
        current_cost, current_id = heapq.heappop(heap_cost)
        for neigh_id, cost in nodes_info[current_id]["neighbors"]:
            new_cost = current_cost + cost
            if new_cost < nodes_info[neigh_id]["cost"]:
                nodes_info[neigh_id]["cost"] = new_cost
                nodes_info[neigh_id]["prev"] = current_id
                heapq.heappush(heap_cost, (new_cost, neigh_id))
    
    return nodes_info