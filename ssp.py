from models.Graph import Graph
from utilities.graph.GraphChecker import GraphChecker
from pathlib import Path
from utilities.graph.plot_graph import plot
from utilities.loaders.Loader import Loader

file_path = Path("resource") / "grafo_iniziale.json"
config_path = Path("resource") / "config.yml"
graph = Graph(file_path)
checker = GraphChecker(graph)
if checker.validateGraph():
    plot(graph, dict(Loader().from_yaml(config_path)))