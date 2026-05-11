class Zone():
    def __init__(self, name: str, x: int, y: int,
                 is_start: bool, is_end: bool,
                 color: str | None, zone_type: str,
                 max_drones: int) -> None:

        self.name = name
        self.x = x
        self.y = y
        self.is_start = is_start
        self.is_end = is_end
        self.color = color
        self.type = zone_type
        self.max_drones = max_drones
        self.current_nb_drone = 0

    def __repr__(self):
        return f"{self.name}"
