class Zone():
    """
    Represents a node in the airspace graph.

    Zones are the locations drones can occupy. Each zone has a type
    that affects traversal cost and pathfinding behavior, and a maximum
    drone capacity enforced by the reservation table.
    """

    def __init__(self, name: str, x: int, y: int,
                 is_start: bool, is_end: bool,
                 color: str | None, zone_type: str,
                 max_drones: int) -> None:
        """
        Args:
            name: Unique identifier for this zone.
            x: Horizontal position in the grid.
            y: Vertical position in the grid.
            is_start: True if this is the departure zone.
            is_end: True if this is the destination zone.
            color: Display color name or hex string.
                None defaults to dark grey.
            zone_type: One of 'normal', 'priority', 'restricted', or 'blocked'.
            max_drones: Maximum number of drones allowed in this
                zone at the same turn.
        """

        self.name = name
        self.x = x
        self.y = y
        self.is_start = is_start
        self.is_end = is_end
        self.color = color
        self.type = zone_type
        self.max_drones = max_drones
        self.current_nb_drone = 0

    def __repr__(self) -> str:
        return f"{self.name}"
