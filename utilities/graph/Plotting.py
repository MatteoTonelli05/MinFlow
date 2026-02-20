# Ho preso spunto da:
# https://networkx.org/documentation/stable/tutorial.html
# https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
# https://stackoverflow.com/questions/72182196/create-graph-with-curved-and-labelled-edges-in-networkx

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from netgraph import InteractiveGraph
from models import Graph


def plot(graph : Graph, config: dict):
    """
    Stampa un grafo usando matplotlib seguendo le configurazioni passate come parametro
    
    :param graph: il grafo preso in considerazione
    :param config: dizionario di configurazione 
    """
    DG = nx.DiGraph()
    
    for e in graph.edges:
        DG.add_edge(e.source, e.target, label=f"{e.flow}/{e.capacity} [c:{e.cost}]")

    pos = nx.shell_layout(DG)
    
    node_color = {}
    for n in graph.nodes:
        if n.id in DG.nodes:
            if n.supply > 0:
                node_color[n.id] = config.get("supply_color","#00FF00")
            elif n.supply < 0:
                node_color[n.id] = config.get("demand_color","#FF0000")
            else:
                node_color[n.id] = config.get("empty_node_color","#EDEDED")
            pos[n.id] = pos[n.id] + np.array([0.2, 0])

    edge_labels = nx.get_edge_attributes(DG, 'label')

    fig, ax = plt.subplots()

    ig = InteractiveGraph(
        DG, 
        node_layout=pos, 
        edge_layout='arc',
        edge_layout_kwargs=dict(rad=config.get("edge_curve_rad",0.2)),
        arrows=True,
        node_color=node_color, 
        node_size=config.get("node_size",8),
        node_labels=True, 
        edge_labels=edge_labels,
        edge_label_fontdict=dict(size=config.get("font_size_edge_labels",7),\
                                  bbox=dict(boxstyle=f'round,pad={config.get("edge_curve_rad",0.2)}', fc='white', alpha=0.7))
    )

    edge_artists = [ig.edge_artists[e] for e in ig.edge_artists]
    edge_keys = list(ig.edge_artists.keys())

    def _on_motion(event):
        """
        gestore di eventi per il movimento del mouse
        
        aggiorna il titolo del grafico mostrando i dettagli dell'arco (sorgente, 
        destinazione e dati di flusso) se il puntatore si trova sopra un arco.
        """
        if event.inaxes != ax:
            return
        for i, (edge_key, artist) in enumerate(ig.edge_artists.items()):
            # Controlla se il mouse è vicino all'edge
            contains, _ = artist.contains(event)
            if contains:
                src, tgt = edge_key[0], edge_key[1]
                label = edge_labels.get((src, tgt), edge_labels.get((tgt, src), ""))
                ax.set_title(f"Edge {src} → {tgt}: {label}", fontsize=10)
                fig.canvas.draw_idle()
                return
        ax.set_title("")
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', _on_motion)

    plt.show()