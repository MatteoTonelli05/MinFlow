from utilities import dijkstra_heap
from utilities.loaders.json_loader import graphJsonLoad
from utilities.loaders.config_loader import configYmlLoad
from utilities import plot_graph
import os

file_path_graph = os.path.join(".", "resource", "grafo_iniziale.json")
file_path_config = os.path.join(".", "resource", "config.yml")
graph_data = graphJsonLoad(file_path_graph)
config_data = configYmlLoad(file_path_config)

plot_graph.plot(graph_data, config_data)
nodes_info = dijkstra_heap.solve(graph_data, config_data["startNode"], config_data["targetNode"])