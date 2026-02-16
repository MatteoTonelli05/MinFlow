from utilities import dijkstra_heap
from utilities import json_translator
from utilities import plot_graph
import pprint

file_path = r"resource\grafo_iniziale.json"
graph_data = json_translator.graphJsonLoad(file_path)
plot_graph.plot(graph_data)
nodes_info = dijkstra_heap.solve(graph_data, "s1", "t2")
pprint.pp(nodes_info)