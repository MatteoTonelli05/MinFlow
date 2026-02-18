import networkx as nx
import matplotlib.pyplot as plt
from models.Graph import Graph

def plot(graph: Graph, config: dict = None):
    # Configurazione di default se manca
    default_config = {
        "figure_size": (10, 8), "layout_k": 0.5, "seed": 42,
        "node_size": 700, "node_color": "skyblue", "arrow_size": 20,
        "edge_target_margin": 10, "edge_curve_rad": 0.1, "font_size_edge_labels": 8
    }
    if config: default_config.update(config)
    cfg = default_config

    G = nx.DiGraph()
    
    for node in graph.nodes:
        G.add_node(node.id, supply=node.supply)
    
    for edge in graph.edges:
        G.add_edge(edge.source, edge.target, 
                   cap=edge.capacity, cost=edge.cost, flow=edge.flow)

    plt.figure(figsize=cfg["figure_size"])
    pos = nx.spring_layout(G, k=cfg["layout_k"], seed=cfg["seed"])
    
    # Disegno Nodi
    nx.draw_networkx_nodes(G, pos, node_size=cfg["node_size"], node_color=cfg["node_color"])
    nx.draw_networkx_labels(G, pos)

    # Disegno Archi
    nx.draw_networkx_edges(
        G, pos, 
        arrowstyle='-|>', 
        arrowsize=cfg["arrow_size"], 
        min_target_margin=cfg["edge_target_margin"],
        connectionstyle=f'arc3,rad={cfg["edge_curve_rad"]}'
    )

    # Etichette archi
    edge_labels = {
        (u, v): f"{d['flow']}/{d['cap']} (c:{d['cost']})" 
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=cfg["font_size_edge_labels"])

    plt.axis('off')
    plt.show()