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

    def __repr__(self):
        return f"{self.name}"
                # f"x y = {self.x} {self.y}\n"
                # f"start = {self.is_start}\n"
                # f"end = {self.is_end}\n"
                # f"color = {self.color}\n"
                # f"zone_type = {self.zone_type}\n"
                # f"max_drones = {self.max_drones}")
