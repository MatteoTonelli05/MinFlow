from utilities.loaders.Loader import Loader
from models.Edge import Edge
from models.Node import Node

class Graph:
    """
    Grafo orientato con nodi e archi.
    Mantiene liste di adiacenza per accesso rapido agli archi uscenti/entranti.
    """

    def __init__(self, file_path: str):
        self._nodes: list[Node] = []
        self._edges: list[Edge] = []
        self._adj: dict[str, list[Edge]] = {}   # archi uscenti
        self._radj: dict[str, list[Edge]] = {}  # archi entranti
        self._load(Loader.from_json(file_path))
    
    def _load(self, graph_data) -> None:
        """Carica nodi e archi dal dizionario."""
        if graph_data is None:
            raise ValueError("Impossibile caricare il grafo: dati non validi.")
        for n in graph_data["nodes"]:
            self.add_node(Node.from_dict(dict(n)))
        for e in graph_data["edges"]:
            self.add_edge(Edge.from_dict(dict(e)))

    def add_node(self, node: Node) -> None:
        """Aggiunge un nodo al grafo."""
        if any(n.id == node.id for n in self._nodes):
            raise ValueError(f"Nodo duplicato: '{node.id}'")
        self._nodes.append(node)
        self._adj[node.id] = []
        self._radj[node.id] = []

    def add_edge(self, edge: Edge) -> None:
        """Aggiunge un arco al grafo. I nodi devono esistere."""
        if not any(n.id == edge.source for n in self._nodes) or \
           not any(n.id == edge.target for n in self._nodes):
            raise KeyError(f"Nodi non esistenti. {edge.source}→{edge.target}: ")
        self._edges.append(edge)
        self._adj[edge.source].append(edge)
        self._radj[edge.target].append(edge)

    def remove_edge(self, source: str, target: str) -> None:
        """Rimuove il primo arco tra source e target."""
        edge = self.get_edge(source, target)
        if edge is None:
            raise KeyError(f"Arco {source}→{target} non trovato.")
        
        self._edges.remove(edge)
        self._adj[source].remove(edge)
        self._radj[target].remove(edge)

    def get_node(self, node_id: str) -> Node:
        """Ritorna il nodo con l'id specificato, o None."""
        for node in self._nodes:
            if node.id == node_id:
                return node
        return None

    def get_edge(self, source: str, target: str) -> Edge:
        """Ritorna il primo arco tra source e target, o None."""
        for edge in self._adj.get(source, []):
            if edge.target == target:
                return edge
        return None

    @property
    def nodes(self) -> list[Node]:
        """Lista di tutti i nodi."""
        return list(self._nodes) #creo una copia

    @property
    def edges(self) -> list[Edge]:
        """Lista di tutti gli archi."""
        return list(self._edges)

    def get_adj(self, node_id: str) -> list[Edge]:
        """Archi uscenti dal nodo."""
        return self._adj.get(node_id, [])

    def get_radj(self, node_id: str) -> list[Edge]:
        """Archi entranti nel nodo."""
        return self._radj.get(node_id, [])

    def get_supply(self) -> list[Node]:
        """Nodi sorgenti"""
        return filter(lambda x: x.supply > 0, self._nodes)
    
    def get_demand(self) -> list[Node]:
        """Nodi pozzi"""
        return filter(lambda x: x.supply < 0, self._nodes)

    def __repr__(self) -> str:
        return f"Graph(nodes={len(self._nodes)}, edges={len(self._edges)})"