from dataclasses import dataclass

@dataclass
class Edge:
    source: str
    target: str
    capacity: int
    cost: int
    flow: int = 0

    def __post_init__(self):
        if self.capacity < 0:
            raise ValueError(f"Capacità negativa ({self.capacity}).")
        if not (0 <= self.flow <= self.capacity):
            raise ValueError(f"Flusso {self.flow} fuori range [0, {self.capacity}].")

    @property
    def residual_capacity(self) -> int:
        """
        Calcola la capacità resiuda
        
        :return: capacità residua (capacità - flusso) come intero
        """
        return self.capacity - self.flow

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        """
        Crea un arco dato un dizionario
        
        :param data: dizionario con i seguenti valori --> source, target, capacity, cost, flow
        """
        return cls(
            source=data["source"],
            target=data["target"],
            capacity=data["capacity"],
            cost=data["cost"],
            flow=data.get("flow", 0)
        )
    
    def reverse(self) -> "Edge":
        """
        Metodo per avere l'arco inverso
        
        :return: arco con direzione inversa e costo negativo
        """
        return Edge(
            source=self.target,
            target=self.source,
            capacity=0,
            cost=-self.cost,
            flow=0
        )