from utilities.loaders.Loader import Loader
from models.Edge import Edge
from models.Node import Node

class Graph:
    def __init__(self, file_path: str = None):
        self._nodes: dict[str, Node] = {} # Usiamo un dict per accesso O(1)
        self._edges: list[Edge] = []
        self._adj: dict[str, list[Edge]] = {}
        self._radj: dict[str, list[Edge]] = {}

        if file_path:
            # Assumendo che Loader ritorni il dict corretto
            self._load(Loader.from_json(file_path))
    
    def _load(self, graph_data) -> None:
        if not graph_data:
            raise ValueError("Dati non validi.")
        for n in graph_data.get("nodes", []):
            self.add_node(Node.from_dict(n))
        for e in graph_data.get("edges", []):
            self.add_edge(Edge.from_dict(e))

    def add_node(self, node: Node) -> None:
        if node.id in self._nodes:
            raise ValueError(f"Nodo duplicato: '{node.id}'")
        self._nodes[node.id] = node
        self._adj[node.id] = []
        self._radj[node.id] = []

    def add_edge(self, edge: Edge) -> None:
        if edge.source not in self._nodes or edge.target not in self._nodes:
            raise KeyError(f"Nodi inesistenti per l'arco {edge.source}->{edge.target}")
        self._edges.append(edge)
        self._adj[edge.source].append(edge)
        self._radj[edge.target].append(edge)

    @property
    def nodes(self) -> list[Node]:
        return list(self._nodes.values())

    @property
    def edges(self) -> list[Edge]:
        return list(self._edges)

    def get_supply_nodes(self) -> list[Node]:
        return [n for n in self._nodes.values() if n.is_source]
    
    def get_demand_nodes(self) -> list[Node]:
        return [n for n in self._nodes.values() if n.is_target]

    def get_edge(self, source: str, target: str) -> Edge:
        """Ritorna il primo arco tra source e target, o None."""
        for edge in self._adj.get(source, []):
            if edge.target == target:
                return edge
        return None

    def __repr__(self) -> str:
        return f"Graph(nodes={len(self._nodes)}, edges={len(self._edges)})"