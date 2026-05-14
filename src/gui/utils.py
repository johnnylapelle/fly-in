import random
import typing

from PyQt6.QtWidgets import QApplication, QStyle

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
            return "#5B2515"
        case _:
            return color


def get_fish() -> str:
    fishes = [
        "fish.png",
        "fish2.png",
        "fish3.png"
    ]

    return "src/gui/assets/" + random.choice(fishes)


def get_style() -> QStyle:
    inst = typing.cast(QApplication, QApplication.instance())
    return typing.cast(QStyle, inst.style())
