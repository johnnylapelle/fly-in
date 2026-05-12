SCALE = 200
RADIUS = SCALE // 2
MARGIN = 30


def get_color(color: str | None) -> str:
    if color is None:
        return "#1F1F1F"

    match color:
        case "red":
            return "#ff5245"
        case "blue":
            return "#10288C"
        case "green":
            return "#6EB867"
        case "darkred":
            return "#790732"
        case "brown":
            return "#A65D33"
        case "purple":
            return "#B42CC0"
        case "black":
            return "#242424"
        case "maroon":
            return "#9C3819"
        case _:
            return color
