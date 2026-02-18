class Edge:
    source: str
    target: str
    capacity: int
    cost: int
    flow: int = 0
    label: str = ""

    def __post_init__(self):
        if self.capacity < 0:
            raise ValueError(f"Capacità negativa non ammessa ({self.capacity}).")
        if not (0 <= self.flow <= self.capacity):
            raise ValueError(f"Flusso {self.flow} fuori range [0, {self.capacity}].")
        
    @property
    def residual_capacity(self) -> int:
        return self.capacity - self.flow

    @property
    def is_saturated(self) -> bool:
        return self.residual_capacity == 0

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        tmp = cls()
        tmp.source=data["source"]
        tmp.target=data["target"]
        tmp.capacity=data["capacity"]
        tmp.cost=data["cost"]
        tmp.flow=data.get("flow", 0)
        tmp.label=data.get("label","")
        return tmp
        


    def __repr__(self):
        return (
            f"Edge({self.source!r} → {self.target!r}, "
            f"cap={self.capacity}, cost={self.cost}, flow={self.flow})"
        )

    # https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.source == other.source and self.target == other.target \
              and self.cost == other.cost and self.capacity == other.capacity
