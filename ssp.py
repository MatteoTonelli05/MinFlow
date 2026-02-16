from utilities import dijkstra_heap
from utilities import json_translator
import pprint

file_path = r"resource\grafo_iniziale.json"
nodes_info = dijkstra_heap.solve(json_translator.graphJsonLoad(file_path), "s1", "t2")
pprint.pp(nodes_info)