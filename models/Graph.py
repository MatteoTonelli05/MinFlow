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
        """
        aggiunge nodo al grafo
        
        :param node: nodo da aggiungere
        """
        if node.id in self._nodes:
            raise ValueError(f"Nodo duplicato: '{node.id}'")
        self._nodes[node.id] = node
        self._adj[node.id] = []
        self._radj[node.id] = []

    def add_edge(self, edge: Edge) -> None:
        """
        aggiunge un arco al grafo.
        i nodi estremi devono esistere precendemente
        
        :param edge: arco da aggiungere
        """
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
        """
        ritorna un arco del grafo dati gli id degli estremi
        
        :param source: id del nodo source
        :param target: id del nodo target
        :return: l'arco se esiste, altrimenti None
        """
        for edge in self._adj.get(source, []):
            if edge.target == target:
                return edge
        return None
    
    def get_node(self, id : str) -> Node:
        """
        ritrorna l'oggetto nodo del grafo dato l'id
        
        :param id: id del nodo richiesto
        :return: il nodo se esiste, altrimenti None
        """
        return self._nodes.get(id, None)
    
    def augment_flow(self, path: list[Edge], delta: int):
        """
        aggiorna il flusso lungo un cammino aumentante e gestisce i relativi archi residui.

        :param path: lista di Edge che compongono il cammino da aggiornare
        :param delta: la quantità di flusso da aggiungere al cammino
        """
        for e in path:
            e.flow += delta
            
            rev_edge = self.get_edge(e.target, e.source)
            if not rev_edge:
                rev_edge = e.reverse()
                self.add_edge(rev_edge)
        rev_edge.capacity = delta

    def get_adj(self, node_id : str) -> list[Edge]:
        """
        recupera la lista di adiacenza per un nodo specifico.

        :param node_id: l'identificativo univoco del nodo.
        :return: lista di archi uscenti dal nodo specificato. Se il nodo non esiste, restituisce una lista vuota
        """
        return self._adj.get(node_id, [])

    def reconstruct_path(self, predecessors: dict, start_id: str, end_id: str) -> list[Edge]:
        """
        ricostruisce il percorso dal nodo avente id start_id a quello con end_id ritornando la lista di edge
        
        :param predecessors: dizionario {id_nodo : id_predecessore}
        :param start_id: id del nodo iniziale
        :param end_id: id del nodo finale
        :return: lista di archi che costruiscono il perscorso
        """
        path = []
        current = end_id
        while current != start_id:
            prev = predecessors.get(current)
            if prev is None:
                return [] # Cammino non trovato
            path.append(self.get_edge(prev, current))
            current = prev
        return path[::-1] # Inverte per avere l'ordine da sorgente a destinazione

    def __repr__(self) -> str:
        title = "--- Stampa Grafico ---\n\n"
        totalCost = 0
        nodesDes : list[str] = [title]
        for n in self._nodes:
            nodesDes.append(f"archi uscenti dal nodo {n}:\n")
            for e in self._adj.get(n, []):
                nodesDes.append(f"\t{e}\n")
                totalCost += e.cost if e.flow > 0 else 0
        nodesDes.append(f"il costo complessivo del flusso è {str(totalCost)}")
        return "".join(nodesDes)