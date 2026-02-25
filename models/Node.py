from dataclasses import dataclass

@dataclass
class Node:
    id: str
    supply: int = 0
    potential : int = 0

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("L'id del nodo non può essere vuoto.")

    @property
    def is_supply(self) -> bool:
        return self.supply > 0
    
    @property
    def is_demand(self) -> bool:
        return self.supply < 0

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        return cls(
            id=data["id"],
            supply=data.get("supply", 0)
        )

