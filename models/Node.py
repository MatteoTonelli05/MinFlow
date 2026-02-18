class Node:
    id: str
    supply: int = 0
    label: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("L'id del nodo non può essere vuoto.")

    @property
    def is_source(self) -> bool:
        return self.supply > 0
    
    @property
    def is_target(self) -> bool:
        return self.supply < 0

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        tmp = cls()
        tmp.id=data["id"]
        tmp.supply=data.get("supply", 0)
        return tmp

    def __repr__(self):
        return f"Node(id={self.id}, supply={self.supply})"

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id == other.id


