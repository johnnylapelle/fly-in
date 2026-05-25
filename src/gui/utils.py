import random
import typing

from PyQt6.QtWidgets import QApplication, QStyle

SCALE = 200
RADIUS = SCALE // 2
MARGIN = 30


def get_color(color: str | None) -> str:
    """
    Resolves a color name to its hex value.

    Returns the hex value for known color names, the input unchanged
    if it is already a hex string, or a default dark color if None.

    Args:
        color: A color name, hex string, or None.

    Returns:
        A hex color string.
    """

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
            return "#5B2515"
        case _:
            return color


def get_fish() -> str:
    """
    Returns the path to a randomly selected fish asset.

    Returns:
        Path to one of the available fish PNG files.
    """

    fishes = [
        "fish.png",
        "fish2.png",
        "fish3.png"
    ]

    return "src/gui/assets/" + random.choice(fishes)


def get_style() -> QStyle:
    """
    Returns the path to a randomly selected fish asset.

    Returns:
        Path to one of the available fish PNG files.
    """

    inst = typing.cast(QApplication, QApplication.instance())
    return typing.cast(QStyle, inst.style())


def parse_name_map(map: str) -> str:
    """
    Extracts the filename without extension from a map path.

    Args:
        map: A file path such as 'maps/easy/01_linear_path.txt'.

    Returns:
        The filename without extension, e.g. '01_linear_path'.
    """

    name = map.split('/')
    name = name[-1].split('.')
    return name[0]
