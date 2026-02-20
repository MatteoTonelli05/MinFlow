import sys, os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from netgraph import InteractiveGraph
from matplotlib.widgets import Button
from models import Graph

plt.ion()
_fig = _ax = _ax_btn = None
_continue = False

def plot(graph: Graph, config: dict):
    global _fig, _ax, _ax_btn, _continue

    DG = nx.DiGraph() # creo il grafo direzionato
    for e in graph.edges:  # aggiungo tutti gli archi
        DG.add_edge(e.source, e.target, label=f"{e.flow}/{e.capacity} [c:{e.cost}]") # label  --> flow/capacity [cost]

    node_color = {}
    
    # ho scelto lo shell layout perchè mi sembrava che mediante i cerchi concentrici rendesse più piacevole la vista
    pos = nx.shell_layout(DG) 
    for n in graph.nodes: # assegno i colori ai nodi in base alla loro funzione
        if n.id in DG.nodes:
            color = "#00FF00" if n.supply > 0 else "#FF0000" if n.supply < 0 else "#EDEDED"
            node_color[n.id] = config.get(
                "supply_color" if n.supply > 0 else "demand_color" if n.supply < 0 else "empty_node_color", color
            ) 

    edge_labels = nx.get_edge_attributes(DG, 'label')

    if _fig is None or not plt.fignum_exists(_fig.number):
        # se la finestra non esiste ancora (o è stata chiusa), la creo da zero
        _fig = plt.figure()
        _ax = _fig.add_axes([0, 0.1, 0.9, 0.9]) # area grafo
        _ax_btn = _fig.add_axes([0.4, 0.01, 0.3, 0.07]) # area bottone
    else:
        _ax.clear() # riuso la finestra esistente pulendo solo l'area grafo

    _continue = False
    btn = Button(_ax_btn, "Prossima Iterazione")
    # globals().update() è necessario perché la lambda non può usare 'global' per modificare _continue
    # https://stackoverflow.com/questions/42211594/lambda-to-assign-a-value-to-global-variable
    btn.on_clicked(lambda e: globals().update(_continue=True))

    ig = InteractiveGraph(
        DG, ax=_ax, node_layout=pos, edge_layout='arc',
        edge_layout_kwargs=dict(rad=config.get("edge_curve_rad", 0.2)),
        arrows=True, node_color=node_color,
        node_size=config.get("node_size", 8), node_labels=True,
        edge_labels=edge_labels, edge_width=config.get("edge_width", 2.5),
        edge_color=config.get("edge_color", "#333333"),
        edge_label_fontdict=dict(
        size=config.get("font_size_edge_labels", 7)
        )
    )
    _fig.canvas.draw_idle()

    # mentre aspetto il click SUL BOTTONE blocco la stampa per eliminare il warning di netgraph
    # https://stackoverflow.com/questions/42952623/stop-python-module-from-printing
    with open(os.devnull, "w") as devNull:
        sys.stdout = devNull
        while not _continue:
            plt.pause(0.05) 
        sys.stdout = sys.__stdout__