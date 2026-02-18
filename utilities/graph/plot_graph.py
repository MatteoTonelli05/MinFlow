import networkx as nx
import matplotlib.pyplot as plt
from models.Graph import Graph

def plot(graph_obj: Graph, config_data: dict):
    """
    Renderizza il grafo usando l'oggetto Graph personalizzato.
    """
    G = nx.DiGraph()

    # Popolamento da oggetti Node
    for node in graph_obj.nodes:
        # NetworkX usa spesso il segno opposto per la demand (supply = -demand)
        G.add_node(node.id, supply=node.supply)

    # Popolamento da oggetti Edge
    for edge in graph_obj.edges:
        G.add_edge(
            edge.source, 
            edge.target, 
            capacity=edge.capacity, 
            weight=edge.cost,
            flow=edge.flow
        )

    plt.figure(figsize=config_data["figure_size"])
    
    # Layout e disegno base
    pos = nx.spring_layout(G, k=config_data["layout_k"], seed=config_data["seed"])
    
    nx.draw_networkx_nodes(G, pos, node_size=config_data["node_size"], node_color=config_data["node_color"])
    nx.draw_networkx_labels(G, pos)
    
    nx.draw_networkx_edges(
        G, pos, 
        arrowstyle='-|>', 
        arrowsize=config_data["arrow_size"], 
        min_target_margin=config_data["edge_target_margin"], 
        connectionstyle=f'arc3,rad={config_data["edge_curve_rad"]}'
    )

    # Etichette dinamiche basate sullo stato attuale del flusso
    edge_labels = {
        (u, v): f"{d['flow']}/{d['capacity']} (c:{d['weight']})" 
        for u, v, d in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels=edge_labels, 
        font_size=config_data["font_size_edge_labels"]
    )

    plt.axis('off')
    plt.show()