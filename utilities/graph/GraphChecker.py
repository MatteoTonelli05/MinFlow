from models.Graph import Graph

class GraphChecker:

    _to_check : Graph = None

    def __init__(self, graph: Graph):
        self._to_check = graph

    def _is_directed(self) -> bool:
        """
        Controlla se almeno un arco ha un suo opposto identico, allora ritorna False
        """
        for edge in self._to_check.edges:
           reverse = self._to_check.get_edge(edge.target, edge.source)
           if reverse == edge :
               return False
        return True

    def _is_balanced(self) -> bool:
        """controlla Bilanciamento: Σ bi = 0"""
        supply = map(lambda x: x.supply, self._to_check.get_supply())
        demand = map(lambda x: x.supply, self._to_check.get_demand())
        return sum(supply) == -sum(demand)
        
    def _has_negative_costs(self) -> bool:
        """Controlla se esiste almeno un arco con costo negativo, allora torna True"""
        return any(edge.cost < 0 for edge in self._to_check.edges)
    
    def _has_zero_capacities(self) -> bool:
        """Controlla se esiste almeno un arco con capacità zero o negativa, allora torna True"""
        return any(edge.capacity <= 0 for edge in self._to_check.edges)


    def validateGraph(self) -> bool:
        """
            Validazione:
            1. Dati interi (costi, supply/demand, capacità) <== CONTROLLATO AUTOMATICAMENTE DALLA TRADUZIONE DA JSON
            2. Grafo direzionato
            3. Bilanciamento: Σ bi = 0
            4. Esistenza soluzione ammissibile <== in caso contrario la soluzione sarà uguale a zero)
            5. Connettività (cammino tra ogni coppia di nodi) <== in caso contrario la soluzione sarà uguale a zero)
            6. Costi non negativi e capacità positive 
        """
        
        return self._is_directed() and self._is_balanced() \
              and not self._has_negative_costs() and not self._has_zero_capacities()



