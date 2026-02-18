from models.Graph import Graph
from models.Node import Node
from utilities.graph.GraphChecker import GraphChecker
from pathlib import Path
from utilities.graph.plot_graph import plot
from utilities.loaders.Loader import Loader

def selectSourceAndTarget(graph: Graph):
    return max(graph.get_supply_nodes(), lambda x: x.supply), min(graph.get_demand_nodes(), lambda x: x.supply)

file_path = Path("resource") / "grafo_iniziale.json"
config_path = Path("resource") / "config.yml"
graph = Graph(file_path)
checker = GraphChecker(graph)
if checker.validateGraph():
    plot(graph, dict(Loader().from_yaml(config_path)))
    k,l = selectSourceAndTarget(graph)
    
else:
    print("")