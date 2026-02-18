import networkx as nx
import matplotlib.pyplot as plt
from models.Graph import Graph

def plot(graph: Graph, config: dict):
    if not config: 
        return

    G = nx.DiGraph()
    
    for node in graph.nodes:
        G.add_node(node.id, supply=node.supply)
    
    for edge in graph.edges:
        G.add_edge(edge.source, edge.target,cap=edge.capacity, cost=edge.cost, flow=edge.flow)

    plt.figure(figsize=config["figure_size"])
    pos = nx.spring_layout(G, k=config["layout_k"], seed=config["seed"])
    
    nx.draw_networkx_nodes(G, pos, node_size=config["node_size"], node_color=config["node_color"])
    nx.draw_networkx_labels(G, pos)

    nx.draw_networkx_edges(
        G, pos, 
        arrowstyle='-|>', 
        arrowsize=config["arrow_size"], 
        min_target_margin=config["edge_target_margin"],
        connectionstyle=f'arc3,rad={config["edge_curve_rad"]}'
    )

    # Etichette archi
    edge_labels = {
        (u, v): f"{d['flow']}/{d['cap']} (c:{d['cost']})" 
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=config["font_size_edge_labels"])

    plt.axis('off')
    plt.show()