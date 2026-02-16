import networkx as nx
import matplotlib.pyplot as plt
from numpy import random

def plot(graph_data):
    G = nx.DiGraph()
    for node in graph_data["nodes"]:
        G.add_node(node["id"], demand=-node["supply"])
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], 
                capacity=edge["capacity"], 
                weight=edge["cost"])
    flow_cost, flow_dict = nx.capacity_scaling(G)
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G,k=2, seed=0)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, min_target_margin=12)
    nx.draw_networkx_labels(G, pos)

    # Etichette archi: "Flusso / Capacità (Costo)"
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        actual_flow = flow_dict[u][v]
        edge_labels[(u, v)] = f"{actual_flow}/{d['capacity']} (c:{d['weight']})"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.axis('off')
    plt.show()