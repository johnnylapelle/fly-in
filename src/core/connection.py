from .zone import Zone


class Connection():
    def __init__(
            self,
            key: str, zone_a: Zone, zone_b: Zone, max_capacity: int) -> None:
        self.key = key
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_capacity = max_capacity

    def get_other(self, zone: Zone) -> Zone:
        # get the neighbor zone connected to zone
        if zone == self.zone_a:
            return self.zone_b
        return self.zone_a

    def __repr__(self) -> str:
        return f"{self.zone_a.name}-{self.zone_b.name}"
