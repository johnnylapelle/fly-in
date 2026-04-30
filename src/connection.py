from .zone import Zone


class Connection():
    def __init__(self, zone_a: Zone, zone_b: Zone, max_capacity: int) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_capacity = max_capacity

    def __repr__(self) -> str:
        return f"{self.zone_a.name}-{self.zone_b.name} {self.max_capacity}"
