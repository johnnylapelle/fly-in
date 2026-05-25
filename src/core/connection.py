from .zone import Zone


class Connection():
    """
    Represents a bidirectional connection between two zones.

    Tracks the maximum number of drones allowed to traverse it
    simultaneously and whether it leads to a restricted zone,
    which affects how the pathfinder handles transit states.
    """

    def __init__(
            self,
            key: str, zone_a: Zone, zone_b: Zone,
            max_capacity: int, is_restricted: bool) -> None:
        """
        Args:
            key: Unique identifier for this connection, formatted as
                'zone_a_name-zone_b_name' in alphabetical order.
            zone_a: One endpoint of the connection.
            zone_b: The other endpoint of the connection.
            max_capacity: Maximum number of drones allowed on this
                connection at the same turn.
            is_restricted: True if either connected zone is of type
                'restricted'. Used by the pathfinder to insert a
                transit state in the path.
        """

        self.key = key
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_capacity = max_capacity
        self.current_nb_drone = 0
        self.is_restricted = is_restricted

    def get_other(self, zone: Zone) -> Zone:
        """
        Returns the zone on the other end of the connection.

        Args:
            zone: One of the two connected zones.

        Returns:
            The other connected zone.
        """

        if zone == self.zone_a:
            return self.zone_b
        return self.zone_a

    def __repr__(self) -> str:
        return f"{self.zone_a.name}-{self.zone_b.name}"
