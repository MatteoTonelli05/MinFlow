from dataclasses import dataclass

@dataclass
class Edge:
    source: str
    target: str
    capacity: int
    cost: int
    flow: int = 0
    label: str = ""

    def __post_init__(self):
        if self.capacity < 0:
            raise ValueError(f"Capacità negativa ({self.capacity}).")
        if not (0 <= self.flow <= self.capacity):
            raise ValueError(f"Flusso {self.flow} fuori range [0, {self.capacity}].")
        
    @property
    def residual_capacity(self) -> int:
        return self.capacity - self.flow

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        return cls(
            source=data["source"],
            target=data["target"],
            capacity=data["capacity"],
            cost=data["cost"],
            flow=data.get("flow", 0),
            label=data.get("label", "")
        )