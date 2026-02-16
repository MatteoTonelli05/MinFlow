import networkx as nx
import matplotlib.pyplot as plt

def plot(graph_data, config_data):
    G = nx.DiGraph()
    for node in graph_data["nodes"]:
        G.add_node(node["id"], demand=-node["supply"])
    for edge in graph_data["edges"]:
        G.add_edge(edge["source"], edge["target"], 
                capacity=edge["capacity"], 
                weight=edge["cost"])
    flow_cost, flow_dict = nx.capacity_scaling(G)
    plt.figure(figsize=config_data["figure_size"])
    pos = nx.spring_layout(G,k=config_data["layout_k"], seed=config_data["seed"])
    nx.draw_networkx_nodes(G, pos, node_size=config_data["node_size"], node_color=config_data["node_color"])
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=config_data["arrow_size"], min_target_margin=config_data["edge_target_margin"], connectionstyle=f'arc3,rad={config_data["edge_curve_rad"]}')
    nx.draw_networkx_labels(G, pos)

    # Etichette archi: "Flusso / Capacità (Costo)"
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        actual_flow = flow_dict[u][v]
        edge_labels[(u, v)] = f"{actual_flow}/{d['capacity']} (c:{d['weight']})"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=config_data["font_size_edge_labels"])

    plt.axis('off')
    plt.show()